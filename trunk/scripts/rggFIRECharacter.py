from PyQt4.QtCore import *

class FIRECharacter(object):
    
    def __init__(self):
        self.stats = {'lust':3,
                      'gluttony':3,
                      'greed':3,
                      'sloth':3,
                      'wrath':3,
                      'envy':3,
                      'pride':3}
        self.vice = 21
        self.name = ''
        self.skills = {}
        self.peculiarities = {}
        
    def initFromDump(self, name, l, g, gr, s, w, e, p):
        self.name = name
        self.stats = {'lust':l,
                      'gluttony':g,
                      'greed':gr,
                      'sloth':s,
                      'wrath':w,
                      'envy':e,
                      'pride':p}
        
    def setName(self, new):
        self.name = new
        
    def getName(self):
        return self.name
    
    def getStat(self, stat):
        return self.stats[stat]
    
    def getAllStats(self):
        return self.stats
    
    def setStat(self, stat, new):
        self.stats[stat] = new
        
    def getVice(self):
        return self.vice
    
    def getCurrentVice(self):
        total = 0
        for vice in self.stats.values():
            total += vice
        return total