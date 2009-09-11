'''
rggRPC - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Remote procedure calls.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import sys
from rggNet import JsonServer, JsonClient

# Base server and client implementations
client = JsonClient()
server = JsonServer(client)

# Table of rpc responses
clientResponses = {}
serverResponses = {}

# constant argument names
PARM_COMMAND = '-command'
PARM_ARGS = '-args'
PARM_MULT_USERS = 'users'
PARM_SINGLE_USER = 'user'

class invalidRPCError(Exception):
    """An error which indicates some malformatted RPC packet."""
    pass

def serverRPC(callable):
    """Decorates a callable to make it an RPC call from the server."""
    
    # Figure out signature of the callable
    command, minargs, argnames, hasArgs, hasKwargs = resolveRPCValues(callable)
    if PARM_MULT_USERS in argnames:
        raise RuntimeError("RPC command '{0}' is not allowed to have a '{1]' parameter.".format(command, PARM_MULT_USERS))
    
    def send(users, *args, **kwargs):
        # NOTE: Call validation that can be commented out for speed
        # probably ok to keep in final
        validateRPC(command, args, kwargs, minargs, argnames, hasArgs, hasKwargs)
        
        data = packRPCData(command, args, kwargs)
        
        if hasattr(users, 'username'):
            users = (users,)
        
        server.broadcast(data, users=[user.username for user in users])
    
    def receive(args, kwargs):
        # Might be redundant with python's checking, but gives more contextual error messages.
        validateRPC(command, args, kwargs, minargs, argnames, hasArgs, hasKwargs)
        
        # Ignore return value
        callable(*args, **kwargs)
    
    clientResponses[command] = receive
    send.command = command
    send.original = callable
    receive.command = command
    receive.original = callable
    return send

def clientRPC(callable):
    """Decorates a callable to make it an RPC call from the client."""
    
    # Figure out signature of the callable
    command, minargs, argnames, hasArgs, hasKwargs = resolveRPCValues(callable)
    if len(argnames) < 1 or PARM_SINGLE_USER != argnames[0]:
        raise RuntimeError("RPC command '{0}' must have a '{1}' parameter as the first parameter.".format(command, PARM_SINGLE_USER))
    
    minargs -= 1
    argnames = argnames[1:]
    
    def send(*args, **kwargs):
        # NOTE: Call validation that can be commented out for speed
        # probably ok to keep in final
        validateRPC(command, args, kwargs, minargs, argnames, hasArgs, hasKwargs)
        if PARM_SINGLE_USER in kwargs:
            raise invalidRPCError("RPC command '{0}' cannot be called with a '{1}' parameter.".format(command, PARM_SINGLE_USER))
        
        data = packRPCData(command, args, kwargs)
        
        # Send the data
        client.send(data)
    
    def receive(user, args, kwargs):
        # Might be redundant with python's checking, but gives more contextual error messages.
        validateRPC(command, args, kwargs, minargs, argnames, hasArgs, hasKwargs)
        if PARM_SINGLE_USER in kwargs:
            raise invalidRPCError("RPC command '{0}' cannot be called with a '{1}' parameter.".format(command, PARM_SINGLE_USER))
        
        # Ignore return value
        callable(user, *args, **kwargs)
    
    serverResponses[command] = receive
    send.command = command
    send.original = callable
    receive.command = command
    receive.original = callable
    return send

def resolveRPCValues(callable):
    """Figures out the signature of the callable."""
    
    assert(callable.__name__)
    assert(callable.func_code)
    
    # Grab some parameters from the function
    command = callable.__name__ # command name
    if command in clientResponses:
        raise RuntimeError("RPC command '{0}' has the same name as another command.".format(command))
    
    code = callable.func_code
    # min number of parameters
    if callable.func_defaults:
        minargs = code.co_argcount - len(callable.func_defaults)
    else:
        minargs = code.co_argcount
    
    argnames = code.co_varnames[:code.co_argcount] # the argument names
    hasArgs = ((code.co_flags & 0x04) != 0) # has an *args param
    hasKwargs = ((code.co_flags & 0x08) != 0) # has a **kwargs param
    code = None
    
    # Sanity check
    assert(minargs <= len(argnames))
    return command, minargs, argnames, hasArgs, hasKwargs
    
def validateRPC(command, args, kwargs, minargs, argnames, hasArgs, hasKwargs):
    
    # Mark off names of positional parameters
    names = set(argnames[:min(len(args), len(argnames))])
    
    # Keyword arguments
    for name in kwargs:
        # Duplicate with positional param
        if name in names:
            raise invalidRPCError("RPC call to '{0}' has duplicate '{1}' keyword argument.".format(command, name))
        # Normal keyword argument
        elif name in argnames:
            names.add(name)
        # Extra keyword argument when **kwargs not present
        elif not hasKwargs:
            raise invalidRPCError("RPC call to '{0}' has unexpected '{1}' keyword argument.".format(command, name))
    
    # Number of args > positional args and no *args param
    if len(args) > len(argnames):
        if not hasArgs:
            raise invalidRPCError("RPC call to '{0}' has too many positional arguments.".format(command))
    
    # Missing positional arguments not specified with keywords, not with default arguments
    elif len(args) < minargs:
        for name in argnames[len(args):minargs]:
            if name not in names:
                raise invalidRPCError("RPC call to '{0}' is missing '{1}' argument".format(command, name))

def packRPCData(command, args, kwargs):
    """Create a dictionary that can be sent over the wire."""
    # Might be better design to assign a name to each parameter rather than
    # sticking positional parameters in 'args'
    data = dict(**kwargs)
    data[PARM_COMMAND] = command
    if args:
        data[PARM_ARGS] = args
    return data

def unpackRPCData(data):
    """Create a dictionary from data sent over the wire."""
    kwargs = data.copy()

    command = data.get(PARM_COMMAND)
    if PARM_COMMAND not in data:
        raise invalidRPCError("RPC call is missing '{0}' metaargument.", PARM_COMMAND)
    del kwargs[PARM_COMMAND]
    
    if PARM_ARGS in data:
        args = data[PARM_ARGS]
        del kwargs[PARM_ARGS]
    else:
        args = []
    
    #print command, repr(args), repr(kwargs)
    # bugfix: need kwargs to be strings
    kwargs=dict((str(key), item) for key, item in kwargs.items())
    #print repr(kwargs)
    
    return command, args, kwargs

# Receipt of data

def receiveClientRPC(data):
    """Occurs when the client receives data.
    
    data -- a dictionary or list of serialized data
    
    """
    # NOTE: Except blocks sometimes block stack traces
    excepting = True
    try:
        command, args, kwargs = unpackRPCData(data)
        if not command in clientResponses:
            print "Client: attempt to run unknown command {command}".format(command=command)
            excepting = False
            return
        clientResponses[command](args, kwargs)
        excepting = False
    finally:
        if excepting:
            print "Client: error processing data: {0}; {1}".format(repr(data), sys.exc_info()[:2])

def receiveServerRPC(user, data):
    """Occurs when the server receives data.
    
    user -- the user sending data
    data - a dictionary or list of serialized data
    
    """
    # NOTE: Except blocks sometimes block stack traces
    excepting = True
    try:
        command, args, kwargs = unpackRPCData(data)
        if not command in serverResponses:
            print "Server: attempt to run unknown command from {user} {command}".format(user=user.username, command=command)
            excepting = False
            return
        serverResponses[command](user, args, kwargs)
        excepting = False
    finally:
        if excepting:
            print "Server: error processing data for user ({0}): {1}; {2}".format(id, repr(data), sys.exc_info()[:2])
