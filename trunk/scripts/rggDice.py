#rggDice - for the Random Game Generator project
# v. 0.01  
#
# NOTE: This returns a string because of the possible
#       complexity of output. So don't expect an int!
#       Conversely, no need to bother formatting it much.
#       (Handle + " rolls " + roll(input)) is fine.
#
#By Doctus (kirikayuumura.noir@gmail.com)
'''
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

import random

def _die(sides):
    return random.randrange(1, sides+1)

def isRollValid(dice):
    try:
        roll(dice)
        return True
    except:
        pass
    return False

def roll(inpstring):
    if inpstring.isdigit(): #just save time in this case...
        return "<b>" + inpstring + "</b> (" + inpstring + ")"
    else:
        if inpstring.find('dn') != -1: #for Darkest Night by Jeremy Lennert
            dicenum = int(inpstring[0:inpstring.index('dn')])
            target = int(inpstring[inpstring.index('dn')+2:])
            #TO-DO: The original plan was to support modifications to the rolls,
            #but the rule that you can apply things in the order most beneficial
            #to you, combined with not knowing all the powers etc., makes
            #that difficult at present. Let's improve it later.
            results = []
            successes = 0
            for x in range(0, dicenum):
                results.append(_die(6))
            for number in results:
                if number >= target:
                    successes += 1
            if successes == 1:
                return "".join(["<b>", str(results), "</b> against ", str(target), 
                        " (", str(successes), " unmodified success)"])
            return "".join(["<b>", str(results), "</b> against ", str(target), 
                        " (", str(successes), " unmodified successes)"])
        elif inpstring.find('k') != -1:
            keepnum = int(inpstring[inpstring.index('k')+1:])
            total = 0
            results = []
            highs = []
            for die in range(0, int(inpstring[0:inpstring.index('k')])):
                results.append(0)
                currentroll = 0
                while currentroll == 0 or currentroll == 10:
                    currentroll = _die(10)
                    results[die] += currentroll
            for itm in results:
                highs.append(itm)
            highs.sort(None, None, True)
            highs = highs[0:keepnum]
            for addend in highs:
                total += addend
            return ("<b>" + str(total) + "</b> (" + inpstring +
                    ": " + str(results) + ")")
        elif inpstring.find('h') != -1:
            raise NotImplementedError()
        elif inpstring.find('l') != -1:
            raise NotImplementedError()
        elif inpstring.find('o') != -1:
            raise NotImplementedError()
        elif inpstring.find('u') != -1:
            raise NotImplementedError()
        else:
            results = []
            grandTotal = 0
            segmentsAdd = inpstring.split("+")
            for itr in range(0, len(segmentsAdd)):
                segmentsAdd[itr] = segmentsAdd[itr].strip()
            for addend in range(0, len(segmentsAdd)):
                segmentsSubtract = segmentsAdd[addend].split("-")
                if len(segmentsSubtract) > 1:
                    for subtrahend in range(0, len(segmentsSubtract)):
                        if segmentsSubtract[subtrahend].find('d') != -1:
                            tmptotal = 0
                            if segmentsSubtract[subtrahend].find('d') != 0:
                                for itr in range(0, int(segmentsSubtract[subtrahend][0:segmentsSubtract[subtrahend].find('d')])):
                                    currentroll = _die(int(segmentsSubtract[subtrahend][segmentsSubtract[subtrahend].find('d')+1:]))
                                    results.append(currentroll)
                                    tmptotal += currentroll
                            else:
                                currentroll = _die(int(segmentsSubtract[subtrahend][segmentsSubtract[subtrahend].find('d')+1:]))
                                results.append(currentroll)
                                tmptotal += currentroll
                            segmentsSubtract[subtrahend] = tmptotal
                    total = int(segmentsSubtract[0])
                    for indx in range(1, len(segmentsSubtract)):
                        total -= int(segmentsSubtract[indx])
                    segmentsAdd[addend] = total
                else:
                    if segmentsAdd[addend].find('d') != -1:
                        tmptotal = 0
                        for itr in range(0, int(segmentsAdd[addend][0:segmentsAdd[addend].find('d')])):
                            currentroll = _die(int(segmentsAdd[addend][segmentsAdd[addend].find('d')+1:]))
                            results.append(currentroll)
                            tmptotal += currentroll
                        segmentsAdd[addend] = tmptotal
            for itr in segmentsAdd:
                grandTotal += int(itr)
            return "<b>" + str(grandTotal) + "</b> (" + inpstring + ": " + str(results) + ")"
