'''
rggICChat - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Parse and execute chat commands.

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

import rggViews, rggRemote
from rggSystem import fake, translate
from rggViews import ICSay, announce

chatCommands = {}
chatCommandNames = []

defaultDocumentation = fake.translate('chat', 'No documentation found.')

def chat(*args, **kwargs):
    """Adds chat commands to the dict. (Decorator)"""
    def inner(func):
        assert(len(args) > 0)
        for arg in args:
            chatCommands[arg] = func
        if not kwargs.get('hidden'):
            chatCommandNames.append(args[0])
        func.documentation = defaultDocumentation
        return func
    return inner

def splitword(message):
    """Split into a pair: word, rest."""
    words = message.split(None, 1)
    if not words:
        return '', ''
    rest = words[1] if len(words) > 1 else ''
    return words[0], rest

def squish(message):
    """Squishes a message and converts it to lowercase."""
    return ''.join(message.split()).lower()

@chat('say', hidden=True)
def sayChat(message, chname, portrait):
    rggRemote.sendICSay(message, chname, portrait)
    
sayChat.documentation = fake.translate('chatdoc', 
    """/say: Say a chat message. You do not need to write this as a command.<dl>
    <dt>Example:</dt>
        <dd>Hello there!</dd>
        <dd>/say Hello there!</dd>
    </dl><br>
    """)

@chat('randomname')
def randomname(message, chname, portrait):
    if len(message) <= 0:
        ICSay(translate('chat',
            "Syntax: /randomname NAMETYPE. Caps and spaces "
            "are ignored. Some valid arguments are "
            "JAPANESEFEMALEFULL and DwArF M aLe"))
    else:
        rggViews.generateName(squish(message))

randomname.documentation = fake.translate('chatdoc', 
    """/randomname: Generate a random name.<dl>
    <dt>Syntax:</dt>
        <dd>/randomname NAMETYPE. Caps and spaces are ignored.</dd>

    <dt>Example:</dt>
        <dd>/randomname JAPANESEFEMALEFULL</dd>
        <dd>/randomname DwArF M aLe</dd>
    </dl><br>
    """)

@chat('techniquename', 'techname')
def techname(message, chname, portrait):
    rggViews.generateTechnique(message)

techname.documentation = fake.translate('chatdoc', 
    """/techniquename: Generate a technique name.<dl>
    <dt>Alternate spelling:</dt>
        <dd>/techname</dd>

    <dt>Syntax:</dt>
        <dd>/techniquename</dd>
        <dd>/techniquename arguments...</dd>
    
    <dt>Examples:</dt>
        <dd>/techniquename</dd>
        <dd>/techniquename ...</dd>
    </dl><br>
    """)

@chat('advice')
def advice(message, chname, portrait):
    rggViews.generateAdvice()

advice.documentation = fake.translate('chatdoc', 
    """/advice: Generate some random, probably nonsensical advice.<dl>

    <dt>Syntax:</dt>
        <dd>/advice</dd>
    </dl><br>
    """)

@chat('roll')
def roll(message, chname, portrait):
    if not message:
        dice = '2d6'
    else:
        dice = ' '.join(message.split())
    rggViews.rollDice(dice)

roll.documentation = fake.translate('chatdoc', 
    """/roll: Roll the dice. The dice can be in the form of macros or
    like 3d8, for 3 dice with 8 sides. You can also add dice.
    Specify no dice to roll 2d6.<dl>
    <dt>Examples:</dt>
        <dd>/roll</dd>
        <dd>/roll 10d2</dd>
        <dd>/roll mydicemacro</dd>
        <dd>/roll d2 + d6 + 10d2</dd>
    </dl><br>
    """)

@chat('emote', 'me')
def emote(message, chname, portrait):
    if not message:
        ICSay(translate('chat', "Syntax: /me DOES ACTION. Displays '[HANDLE] DOES "
                "ACTION' in italic font."))
    else:
        rggRemote.sendICEmote(message, chname, portrait)

emote.documentation = fake.translate('chatdoc',
    """Display an emote in italics.<dl>
    <dt>Alternate spelling:</dt>
        <dd>/techname</dd>
    
    <dt>Examples:</dt>
        <dd>/techiquename</dd>
        <dd>/techniquename ...</dd>
    </dl><br>
    """)

@chat('whisper', 'w', 't', 'tell', 'msg', 'message')
def whisper(message, chname, portrait):
    if not message:
        ICSay(translate('chat', "Syntax: /whisper HANDLE MESSAGE. Sends a message "
            "only to the specified user. Spaces MUST be correct."
            " Handle may be caps-sensitive."))
    else:
        target, rest = splitword(message)
        if target.lower() == rggViews.localuser().username:
            emote(translate('chat', "mutters something."))
        elif not rest:
            ICSay(translate('chat', "What do you want to tell {target}?").format(target=target))
        else:
            rggRemote.sendWhisper(target, rest)

whisper.documentation = fake.translate('chatdoc',
    """/whisper: Whisper a message to another user.<dl>
    <dt>Alternate spellings:</dt>
        <dd>/w, /tell, /t, /message, /msg</dd>
    
    <dt>Syntax:</dt>
        <dd>/whisper NAME message</dd>
    
    <dt>Example:</dt>
        <dd>/tell danny HEEL PLZ</dd>
    </dl><br>
    """)

def chat(st, chname, portrait):
    """Parses and executes chat commands."""
    st = unicode(st)
    
    if (len(st) <= 0):
        return
    if ('<' in st and '>' not in st) or ('<' in st and '>' in st and '<' in str(st)[str(st).rfind('>'):]):
        ICSay(translate('chat', "Please type &#38;#60; if you wish to include &#60; in your message."))
        return

    if st[0] != '/' or len(st) > 1 and st[1] == '/':
        if len(st) > 1 and st[1] == '/':
            st = st[1:]
        command = 'say'
        message = st.strip()
    else:
        command, message = splitword(st[1:])
        command = str(command).lower()
    #print command, message
    
    if command in chatCommands:
        chatCommands[command](message, chname, portrait)
    else:
        if command not in ('help', '?'):
            ICSay(translate('chatdoc', "Invalid command.", 'Unknown chat command name.'))
        elif message in chatCommands:
            ICSay(translate('chatdoc', chatCommands[message].documentation))
            return
        ICSay(translate('chatdoc', "Command Help:<br>"
            "Typing ordinary text and pressing 'enter' "
            "will display to all players. Other commands may be invoked "
            "with '/' plus the name of the command plus any arguments."
            "<dl><dt>Commands</dt><dd>{commandList}</dd></dl><br>").format(
                commandList=translate('chatdoc',
                    '</dd><dd>',
                    'Goes inbetween the commands in the commandList.').
                    join(chatCommandNames)))



