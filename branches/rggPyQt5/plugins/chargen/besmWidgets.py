from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from . import besmData
import os, json, gzip
from rggSystem import CHARSHEETS_DIR, checkFileExtension
from rggViews import sendCharacterSheet

def jsondump(obj, filename):
    """Dump object to file."""
    try:
        with gzip.open(filename, 'wb') as file:
            json.dump(obj, file, sort_keys=True, indent=4)
    except AttributeError: #support for Python <2.7
        with open(filename, 'wb') as file:
            json.dump(obj, file, sort_keys=True, indent=4)

def jsonload(filename):
    """Loads the object from a file. May throw."""
    try:
        with gzip.open(filename, 'rb') as file:
            obj = json.load(file)
    except: #might be an old uncompressed save
        with open(filename, 'rb') as file:
            obj = json.load(file)
    assert(isinstance(obj, list) or isinstance(obj, dict))
    return obj
    
def jsonappend(obj, filename):
    """Dump object to file. Merges with existing file if present."""
    try:
        dat = jsonload(filename)
        newdat = dict(list(dat.items()) + list(obj.items()))
        jsondump(newdat, filename)
    except:
        jsondump(obj, filename)

class AddDefectDialog(QDialog):
    
    def __init__(self, mainWindow, defectCosts):
        super(QDialog, self).__init__(mainWindow)
        
        self.scrollArea = QScrollArea()
        self.mainLayout = QGridLayout()
        self.mainnLayout = QGridLayout()
        self.setWindowTitle("Add Defect")
        self.setMinimumWidth(300)

        self.buttons = []        
        for i, defect in enumerate(sorted(defectCosts.keys())):
            self.buttons.append(QCheckBox(defect))
            self.mainLayout.addWidget(self.buttons[-1], i, 0)
            self.mainLayout.addWidget(QLabel(str(defectCosts[defect])), i, 1, 1, 1, Qt.AlignRight)
            
        self.OKButton = QPushButton("Add", self)
        
        self.scrollAreaInternal = QWidget()
        self.scrollAreaInternal.setLayout(self.mainLayout)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollAreaInternal)
        
        self.OKButton.clicked.connect(self.okay)
        
        self.mainnLayout.addWidget(QLabel("Defect"), 0, 0)
        self.mainnLayout.addWidget(QLabel("Cost             "), 0, 1, 1, 1, Qt.AlignRight)
        self.mainnLayout.addWidget(self.scrollArea, 1, 0, 1, 2)
        self.mainnLayout.addWidget(self.OKButton, 2, 0, 1, 2)

        self.setLayout(self.mainnLayout)
        
    def okay(self):
        self.selectedDefects = []
        for button in self.buttons:
            if button.isChecked():
                self.selectedDefects.append(button.text())
        self.accept()

class AddAttributeDialog(QDialog):
    
    def __init__(self, mainWindow, attCosts):
        super(QDialog, self).__init__(mainWindow)
        
        self.scrollArea = QScrollArea()
        self.mainLayout = QGridLayout()
        self.mainnLayout = QGridLayout()
        self.setWindowTitle("Add Attribute")
        self.setMinimumWidth(375)

        self.buttons = []        
        for i, att in enumerate(sorted(attCosts.keys())):
            self.buttons.append(QCheckBox(att))
            self.mainLayout.addWidget(self.buttons[-1], i, 0)
            self.mainLayout.addWidget(QLabel(str(attCosts[att])), i, 1, 1, 1, Qt.AlignRight)
            
        self.OKButton = QPushButton("Add", self)
        
        self.scrollAreaInternal = QWidget()
        self.scrollAreaInternal.setLayout(self.mainLayout)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollAreaInternal)
        
        self.OKButton.clicked.connect(self.okay)
        
        self.mainnLayout.addWidget(QLabel("Attribute"), 0, 0)
        self.mainnLayout.addWidget(QLabel("Cost             "), 0, 1, 1, 1, Qt.AlignRight)
        self.mainnLayout.addWidget(self.scrollArea, 1, 0, 1, 2)
        self.mainnLayout.addWidget(self.OKButton, 2, 0, 1, 2)

        self.setLayout(self.mainnLayout)
        
    def okay(self):
        self.selectedAttributes = []
        for button in self.buttons:
            if button.isChecked():
                self.selectedAttributes.append(button.text())
        self.accept()

class AddSkillDialog(QDialog):
    
    def __init__(self, mainWindow, skillCosts):
        super(QDialog, self).__init__(mainWindow)
        
        self.scrollArea = QScrollArea()
        self.mainLayout = QGridLayout()
        self.mainnLayout = QGridLayout()
        self.setWindowTitle("Add Skill")
        self.setMinimumWidth(250)

        self.buttons = []        
        for i, skill in enumerate(sorted(skillCosts.keys())):
            self.buttons.append(QCheckBox(skill))
            self.mainLayout.addWidget(self.buttons[-1], i, 0)
            self.mainLayout.addWidget(QLabel(str(skillCosts[skill])), i, 1, 1, 1, Qt.AlignRight)
            
        self.OKButton = QPushButton("Add", self)
        
        self.scrollAreaInternal = QWidget()
        self.scrollAreaInternal.setLayout(self.mainLayout)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollAreaInternal)
        
        self.OKButton.clicked.connect(self.okay)
        
        self.mainnLayout.addWidget(QLabel("Skill"), 0, 0)
        self.mainnLayout.addWidget(QLabel("Cost             "), 0, 1, 1, 1, Qt.AlignRight)
        self.mainnLayout.addWidget(self.scrollArea, 1, 0, 1, 2)
        self.mainnLayout.addWidget(self.OKButton, 2, 0, 1, 2)

        self.setLayout(self.mainnLayout)
        
    def okay(self):
        self.selectedSkills = []
        for button in self.buttons:
            if button.isChecked():
                self.selectedSkills.append(button.text())
        self.accept()

class CharStatsWidget(QWidget):
    
    def __init__(self, mainWindow):
        super(CharStatsWidget, self).__init__(mainWindow)
        
        self.charPointsBox = QComboBox(self)
        for x in range(5, 105, 5):
            self.charPointsBox.addItem(str(x))
        
        self.skillCostsBox = QComboBox(self)
        for x in sorted(besmData.SKILL_COSTS.keys()):
            self.skillCostsBox.addItem(x)
        
        self.remainingPointsLabelLabel = QLabel("Unspent Points: ")
        self.remainingPointsLabel = QLabel("1")
        self.skillPointsLabel = QLabel("Unspent SP: 20")
        
        self.mechMode = QCheckBox("Mecha Mode")
        
        self.body = QComboBox(self)
        self.mind = QComboBox(self)
        self.soul = QComboBox(self)
        for x in range(1, 13):
            for y in (self.body, self.mind, self.soul):
                y.addItem(str(x))
                
        self.acv = QLabel("1")
        self.dcv = QLabel("1")
        self.health = QLabel("1")
        self.energy = QLabel("1")
        
        self.skillsScroll = QListWidget(self)
        self.attScroll = QListWidget(self)
        self.defectScroll = QListWidget(self)
        
        self.addSkillButton = QPushButton("Add", self)
        self.removeSkillButton = QPushButton("Decrease Level", self)
        
        self.addAttButton = QPushButton("Add", self)
        self.removeAttButton = QPushButton("Decrease Level", self)
        
        self.addDefectButton = QPushButton("Add", self)
        self.removeDefectButton = QPushButton("Decrease Level", self)
        
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Character Points: "), 0, 0)
        self.layout.addWidget(self.charPointsBox, 0, 1)
        self.layout.addWidget(QLabel("Skill Costs: "), 0, 2)
        self.layout.addWidget(self.skillCostsBox, 0, 3)
        self.layout.addWidget(self.remainingPointsLabelLabel, 1, 0)
        self.layout.addWidget(self.remainingPointsLabel, 1, 1)
        self.layout.addWidget(self.mechMode, 1, 2)
        self.layout.addWidget(QLabel("Body: "), 2, 0)
        self.layout.addWidget(self.body, 2, 1)
        self.layout.addWidget(QLabel("Mind: "), 3, 0)
        self.layout.addWidget(self.mind, 3, 1)
        self.layout.addWidget(QLabel("Soul: "), 4, 0)
        self.layout.addWidget(self.soul, 4, 1)
        self.layout.addWidget(QLabel("Health: "), 5, 0)
        self.layout.addWidget(self.health, 5, 1)
        self.layout.addWidget(QLabel("Energy: "), 6, 0)
        self.layout.addWidget(self.energy, 6, 1)
        self.layout.addWidget(QLabel("ACV: "), 7, 0)
        self.layout.addWidget(self.acv, 7, 1)
        self.layout.addWidget(QLabel("DCV: "), 8, 0)
        self.layout.addWidget(self.dcv, 8, 1)
        self.layout.addWidget(QLabel("Skills"), 2, 2)
        self.layout.addWidget(self.skillPointsLabel, 2, 3, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.skillsScroll, 3, 2, 5, 2)
        self.layout.addWidget(self.addSkillButton, 8, 2)
        self.layout.addWidget(self.removeSkillButton, 8, 3)
        self.layout.addWidget(QLabel("Attributes"), 9, 2, 1, 2)
        self.layout.addWidget(self.attScroll, 10, 2, 5, 2)
        self.layout.addWidget(self.addAttButton, 15, 2)
        self.layout.addWidget(self.removeAttButton, 15, 3)
        self.layout.addWidget(QLabel("Defects"), 9, 0, 1, 2)
        self.layout.addWidget(self.defectScroll, 10, 0, 5, 2)
        self.layout.addWidget(self.addDefectButton, 15, 0)
        self.layout.addWidget(self.removeDefectButton, 15, 1)
        self.setLayout(self.layout)
        
        self.updatePoints()
        
        for x in (self.charPointsBox, self.body, self.mind, self.soul, self.skillCostsBox):
            x.currentIndexChanged.connect(self.updatePoints)
            
        self.mechMode.stateChanged.connect(self.updatePoints)
        
        self.addSkillButton.clicked.connect(self.addSkill)
        self.removeSkillButton.clicked.connect(self.decreaseLevel)
        self.addAttButton.clicked.connect(self.addAttribute)
        self.removeAttButton.clicked.connect(self.decreaseAttLevel)
        self.addDefectButton.clicked.connect(self.addDefect)
        self.removeDefectButton.clicked.connect(self.decreaseDefectLevel)
        self.skillsScroll.itemActivated.connect(self.increaseLevel)
        self.attScroll.itemActivated.connect(self.increaseAttLevel)
        self.defectScroll.itemActivated.connect(self.increaseDefectLevel)
        
    def updateDerivedValues(self):
        if not self.mechMode.isChecked():
            baseacv = ((self.body.currentIndex()+self.mind.currentIndex()+self.soul.currentIndex()+3)//3)+self.getAttributeCombatValueEffect()
            basedcv = baseacv - 2
        else:
            baseacv = 0
            basedcv = 0
        if not self.mechMode.isChecked():
            basehealth = ((self.body.currentIndex()+self.soul.currentIndex()+2)*5)+self.getAttributeHealthEffect()
        else:
            basehealth = (40+self.getAttributeHealthEffect())
        if not self.mechMode.isChecked():
            baseenergy = ((self.mind.currentIndex()+self.soul.currentIndex()+2)*5)+self.getAttributeEnergyEffect()
        else:
            baseenergy = 0
        
        self.acv.setText(str(baseacv))
        self.dcv.setText(str(basedcv))
        self.health.setText(str(basehealth))
        self.energy.setText(str(baseenergy))
        if not self.mechMode.isChecked():
            self.skillPointsLabel.setText("Unspent SP: " + str((20+self.getAttributeSkillEffect())-(self.getTotalSkillCosts())))
        else:
            self.skillPointsLabel.setText("Unspent SP: 0")
        
    def updatePoints(self, True=False):
        if self.body.currentIndex() == 11:
            self.mind.setCurrentIndex(min(self.mind.currentIndex(), 10))
            self.soul.setCurrentIndex(min(self.soul.currentIndex(), 10))
        if self.mind.currentIndex() == 11:
            self.soul.setCurrentIndex(min(self.soul.currentIndex(), 10))
        base = (self.charPointsBox.currentIndex()+1)*5
        if not self.mechMode.isChecked():
            result = base - (self.body.currentIndex()+self.mind.currentIndex()+self.soul.currentIndex()+3)
        else:
            result = base
        result -= self.getTotalAttributeCosts()
        self.remainingPointsLabel.setText(str(result))
        self.updateDerivedValues()
        
    def addSkill(self):
        possibleSkills = dict(besmData.SKILL_COSTS[str(self.skillCostsBox.currentText())])
        if self.skillsScroll.count() >= 1:
            for i in range(0, self.skillsScroll.count()):
                del possibleSkills[str(self.skillsScroll.item(i).text())[0:-2]]
        dial = AddSkillDialog(self, possibleSkills)
        if dial.exec_():
            for skill in dial.selectedSkills:
                self.skillsScroll.addItem(skill + " 1")
                self.skillsScroll.sortItems()
        self.updatePoints()
        
    def addAttribute(self):
        possibleAttributes = dict(besmData.ATTRIBUTES)
        if self.mechMode.isChecked():
            possibleAttributes.update(dict(besmData.MECH_ATTRIBUTES))
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                del possibleAttributes[str(self.attScroll.item(i).text())[0:-2]]
        dial = AddAttributeDialog(self, possibleAttributes)
        if dial.exec_():
            for att in dial.selectedAttributes:
                self.attScroll.addItem(att + " 1")
                self.attScroll.sortItems()
        self.updatePoints()
        
    def addDefect(self):
        possibleDefects = dict(besmData.DEFECTS)
        if self.mechMode.isChecked():
            possibleDefects.update(dict(besmData.MECH_DEFECTS))
        if self.defectScroll.count() >= 1:
            for i in range(0, self.defectScroll.count()):
                del possibleDefects[str(self.defectScroll.item(i).text())[0:-2]]
        dial = AddDefectDialog(self, possibleDefects)
        if dial.exec_():
            for defect in dial.selectedDefects:
                self.defectScroll.addItem(defect + " 1")
                self.defectScroll.sortItems()
        self.updatePoints()
        
    def increaseLevel(self):
        if self.skillsScroll.count() == 0: return
        if int(str(self.skillsScroll.currentItem().text())[-1:]) < 6:
            self.skillsScroll.currentItem().setText(self.skillsScroll.currentItem().text()[0:-1] + str(int(str(self.skillsScroll.currentItem().text())[-1:])+1))
        self.updatePoints()
        
    def increaseAttLevel(self):
        if self.attScroll.count() == 0: return
        if int(str(self.attScroll.currentItem().text())[-1:]) < 6:
            self.attScroll.currentItem().setText(self.attScroll.currentItem().text()[0:-1] + str(int(str(self.attScroll.currentItem().text())[-1:])+1))
        self.updatePoints()
        
    def increaseDefectLevel(self):
        if self.defectScroll.count() == 0: return
        if int(str(self.defectScroll.currentItem().text())[-1:]) < 2 or ((besmData.SIX_LEVEL_DEFECTS[0] in str(self.defectScroll.currentItem().text()) or besmData.SIX_LEVEL_DEFECTS[1] in str(self.defectScroll.currentItem().text())) and int(str(self.defectScroll.currentItem().text())[-1:]) < 6):
            self.defectScroll.currentItem().setText(self.defectScroll.currentItem().text()[0:-1] + str(int(str(self.defectScroll.currentItem().text())[-1:])+1))
        self.updatePoints()
        
    def decreaseDefectLevel(self):
        if self.defectScroll.count() == 0: return
        if int(str(self.defectScroll.currentItem().text())[-1:]) > 1:
            self.defectScroll.currentItem().setText(self.defectScroll.currentItem().text()[0:-1] + str(int(str(self.defectScroll.currentItem().text())[-1:])-1))
        else:
            self.defectScroll.takeItem(self.defectScroll.currentRow())
        self.updatePoints()
            
    def decreaseAttLevel(self):
        if self.attScroll.count() == 0: return
        if int(str(self.attScroll.currentItem().text())[-1:]) > 1:
            self.attScroll.currentItem().setText(self.attScroll.currentItem().text()[0:-1] + str(int(str(self.attScroll.currentItem().text())[-1:])-1))
        else:
            self.attScroll.takeItem(self.attScroll.currentRow())
        self.updatePoints()
    
    def decreaseLevel(self):
        if self.skillsScroll.count() == 0: return
        if int(str(self.skillsScroll.currentItem().text())[-1:]) > 1:
            self.skillsScroll.currentItem().setText(self.skillsScroll.currentItem().text()[0:-1] + str(int(str(self.skillsScroll.currentItem().text())[-1:])-1))
        else:
            self.skillsScroll.takeItem(self.skillsScroll.currentRow())
        self.updatePoints()
        
    def getTotalSkillCosts(self):
        total = 0
        for skill in self.getProcessedSkills():
            total += skill[2]
        return total
        
    def getTotalAttributeCosts(self):
        total = 0
        for att in self.getProcessedAttributes():
            total += att[2]
        for defect in self.getProcessedDefects():
            total -= defect[2]
        return total
        
    def getProcessedSkills(self):
        result = []
        possibleSkills = dict(besmData.SKILL_COSTS[str(self.skillCostsBox.currentText())])
        if self.skillsScroll.count() >= 1:
            for i in range(0, self.skillsScroll.count()):
                skillName = str(self.skillsScroll.item(i).text())[0:-2]
                skillRank = int(str(self.skillsScroll.item(i).text())[-1:])
                skillCost = possibleSkills[skillName]*skillRank
                result.append((skillName, skillRank, skillCost))
        return result
        
    def getProcessedAttributes(self):
        result = []
        possibleAttributes = dict(besmData.ATTRIBUTES)
        if self.mechMode.isChecked():
            possibleAttributes.update(dict(besmData.MECH_ATTRIBUTES))
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                attName = str(self.attScroll.item(i).text())[0:-2]
                attRank = int(str(self.attScroll.item(i).text())[-1:])
                attCost = possibleAttributes[attName]*attRank
                result.append((attName, attRank, attCost))
        return result
        
    def getProcessedDefects(self):
        result = []
        possibleDefects = dict(besmData.DEFECTS)
        if self.mechMode.isChecked():
            possibleDefects.update(dict(besmData.MECH_DEFECTS))
        if self.defectScroll.count() >= 1:
            for i in range(0, self.defectScroll.count()):
                defectName = str(self.defectScroll.item(i).text())[0:-2]
                defectRank = int(str(self.defectScroll.item(i).text())[-1:])
                defectCost = possibleDefects[defectName]*defectRank
                result.append((defectName, defectRank, defectCost))
        return result
        
    def getAttributeHealthEffect(self):
        result = 0
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                attName = str(self.attScroll.item(i).text())[0:-2]
                if attName == besmData.HEALTH_ATT:
                    attRank = int(str(self.attScroll.item(i).text())[-1:])
                    result += attRank*10
                elif attName == besmData.MECH_HEALTH_ATT:
                    attRank = int(str(self.attScroll.item(i).text())[-1:])
                    result += attRank*20
        if self.defectScroll.count() >= 1:
            for i in range(0, self.defectScroll.count()):
                defectName = str(self.defectScroll.item(i).text())[0:-2]
                if defectName == besmData.HEALTH_DEFECT:
                    defectRank = int(str(self.defectScroll.item(i).text())[-1:])
                    result -= defectRank*10
        return result
            
    def getAttributeEnergyEffect(self):
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                attName = str(self.attScroll.item(i).text())[0:-2]
                if attName == besmData.ENERGY_ATT:
                    attRank = int(str(self.attScroll.item(i).text())[-1:])
                    return attRank*10
        return 0
        
    def getAttributeSkillEffect(self):
        result = 0
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                attName = str(self.attScroll.item(i).text())[0:-2]
                if attName == besmData.SKILL_ATT:
                    attRank = int(str(self.attScroll.item(i).text())[-1:])
                    result += attRank*10
        if self.defectScroll.count() >= 1:
            for i in range(0, self.defectScroll.count()):
                defectName = str(self.defectScroll.item(i).text())[0:-2]
                if defectName == besmData.SKILL_DEFECT:
                    defectRank = int(str(self.defectScroll.item(i).text())[-1:])
                    result -= defectRank*10
        return result
        
    def getAttributeCombatValueEffect(self):
        result = 0
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                attName = str(self.attScroll.item(i).text())[0:-2]
                if attName == besmData.COMBAT_ATT:
                    attRank = int(str(self.attScroll.item(i).text())[-1:])
                    result += attRank
        if self.defectScroll.count() >= 1:
            for i in range(0, self.defectScroll.count()):
                defectName = str(self.defectScroll.item(i).text())[0:-2]
                if defectName == besmData.COMBAT_DEFECT:
                    defectRank = int(str(self.defectScroll.item(i).text())[-1:])
                    result -= defectRank
        return result
        
    def hasSpecialMechAttribute(self):
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                attName = str(self.attScroll.item(i).text())[0:-2]
                if attName == besmData.MECH_STAT_ATT:
                    return True
        return False
        
    def getExportableData(self):
        fields = {}
        fields["body"] = str(self.body.currentIndex()+1)
        fields["mind"] = str(self.mind.currentIndex()+1)
        fields["soul"] = str(self.soul.currentIndex()+1)
        fields["health"] = str(self.health.text())
        fields["energy"] = str(self.energy.text())
        fields["acv"] = str(self.acv.text())
        fields["dcv"] = str(self.dcv.text())
        fields["skills"] = self.getProcessedSkills()
        fields["attributes"] = self.getProcessedAttributes()
        fields["defects"] = self.getProcessedDefects()
        fields["points"] = str((self.charPointsBox.currentIndex()+1)*5)
        fields["rempoints"] = str(self.remainingPointsLabel.text())
        fields["remskillpoints"] = str((20+self.getAttributeSkillEffect())-(self.getTotalSkillCosts()))
        fields["skillcosts"] = str(self.skillCostsBox.currentIndex())
        return fields
        
    def importData(self, data):
        self.body.setCurrentIndex(int(data["body"])-1)
        self.mind.setCurrentIndex(int(data["mind"])-1)
        self.soul.setCurrentIndex(int(data["soul"])-1)
        self.skillCostsBox.setCurrentIndex(int(data["skillcosts"]))
        self.charPointsBox.setCurrentIndex((int(data["points"])/5)-1)
        for item in data["attributes"]:
            self.attScroll.addItem(item[0] + " " + str(item[1]))
        for item in data["defects"]:
            self.defectScroll.addItem(item[0] + " " + str(item[1]))
        for item in data["skills"]:
            self.skillsScroll.addItem(item[0] + " " + str(item[1]))
        self.attScroll.sortItems()
        self.defectScroll.sortItems()
        self.skillsScroll.sortItems()
        self.updatePoints()

class CharBioWidget(QWidget):
    
    def __init__(self, mainWindow):
        super(CharBioWidget, self).__init__(mainWindow)
        
        self.layout = QGridLayout()
        
        self.widgetz = {}
        self.lineFields = ("name", "age", "gender", "origin")
        self.editFields = ("appearance", "personality", "background")
        for i, field in enumerate(self.lineFields):
            self.widgetz[field] = QLineEdit(self)
            self.layout.addWidget(QLabel(field.capitalize()), i%2, i/2*2)
            self.layout.addWidget(self.widgetz[field], i%2, i/2*2+1)
        for i, field in enumerate(self.editFields):
            self.widgetz[field] = QTextEdit(self)
            self.layout.addWidget(QLabel(field.capitalize()), len(self.lineFields)/2+i*2, 0, 1, 2)
            self.layout.addWidget(self.widgetz[field], len(self.lineFields)/2+i*2+1, 0, 1, 4)
        self.setLayout(self.layout)
        
    def getExportableData(self):
        fields = {}
        for field in self.lineFields:
            fields[field] = str(self.widgetz[field].text())
        for field in self.editFields:
            fields[field] = str(self.widgetz[field].toPlainText())
        return fields
        
    def importData(self, data):
        for field in self.lineFields+self.editFields:
            self.widgetz[field].setText(data[field])

class OhNoesALazyGlobalClass:
    
    def __init__(self, mainWindow, mainWindowReal, layout):
        self.bio = CharBioWidget(mainWindowReal)
        self.stats = CharStatsWidget(mainWindowReal)
        self.menubar = QMenuBar(mainWindowReal)
        self.charsave = QAction("Save Character Sheet...", mainWindowReal)
        self.charload = QAction("Load Character Sheet...", mainWindowReal)
        self.charexport = QAction("Export to Forum Code...", mainWindowReal)
        self.charexportalt = QAction("Export to HTML Page...", mainWindowReal)
        self.chartransfer = QAction("Transfer to connected players...", mainWindowReal)
        self.fileMenu = QMenu("&File")
        self.fileMenu.addAction(self.charsave)
        self.fileMenu.addAction(self.charload)
        self.fileMenu.addAction(self.charexport)
        self.fileMenu.addAction(self.charexportalt)
        self.fileMenu.addAction(self.chartransfer)
        self.menubar.addMenu(self.fileMenu)
        self.mainwin = mainWindow
        #mainWindowReal.setMenuBar(self.menubar)
        layout.addWidget(self.menubar, 0, 0, 1, 2)
        layout.addWidget(self.bio, 1, 0)
        layout.addWidget(self.stats, 1, 1)
        self.charsave.triggered.connect(self.jsonExport)
        self.charload.triggered.connect(self.jsonImport)
        self.charexport.triggered.connect(self.forumExport)
        self.charexportalt.triggered.connect(self.htmlExport)
        self.chartransfer.triggered.connect(self.send)
    
    def send(self):
        title, ok = QInputDialog.getText(self.mainwin, "Filename", "Filename for character sheet:")
        if title and ok:
            title = checkFileExtension(title, ".rcs")
            sendCharacterSheet(self.export(), str(title))
    
    def jsonImport(self):
        filename = str(QFileDialog.getOpenFileName(self.mainwin, "Load Character Sheet...", os.path.join(os.getcwd(), CHARSHEETS_DIR), "RGG Character Sheets (*.rcs)"))
        if not filename:
            return None
        
        data = jsonload(filename)
        self.bio.importData(data)
        self.stats.importData(data)
        
    def export(self):
        fields = self.bio.getExportableData()
        fields.update(self.stats.getExportableData())
        return fields
        
    def jsonExport(self):
        filename = str(QFileDialog.getSaveFileName(self.mainwin, "Save Character Sheet As...", os.path.join(os.getcwd(), CHARSHEETS_DIR, "untitled.rcs"), "RGG Character Sheets (*.rcs)"))
        if not filename:
            return None
        
        jsondump(self.export(), filename)
        
    def realExport(self, outputTemplate, outputFilter, linebreaker, outputType=".txt"):
        fields = self.export()
        rawattributes = []
        for att in fields["attributes"]:
            rawattributes.append(" ".join((att[0], "level", str(att[1]))))
        attributes = linebreaker.join(rawattributes)
        rawdefects = []
        for defect in fields["defects"]:
            rawdefects.append(" ".join((defect[0], "level", str(defect[1]))))
        defects = linebreaker.join(rawdefects)
        rawskills = []
        for skill in fields["skills"]:
            rawskills.append(" ".join((skill[0], "level", str(skill[1]))))
        skills = linebreaker.join(rawskills)
        
        output = outputTemplate.replace("%N", fields["name"]).replace("%A", fields["age"]).replace("%G", fields["gender"]).\
        replace("%O", fields["origin"]).replace("%T", attributes).replace("%D", defects).replace("%S", skills).replace("%R", fields["appearance"]).\
        replace("%P", fields["personality"]).replace("%B", fields["background"]).replace("%Y", fields["body"]).replace("%M", fields["mind"]).\
        replace("%L", fields["soul"]).replace("%H", fields["health"]).replace("%E", fields["energy"]).replace("%C", fields["acv"]).replace("%V", fields["dcv"])
        
        filename = str(QFileDialog.getSaveFileName(self.mainwin, "Export Character Sheet As...", os.path.join(os.getcwd(), CHARSHEETS_DIR, "untitled"+outputType), outputFilter))
        if not filename:
            return None
        
        with open(filename, "w") as f:
            f.write(output)
        
    def htmlExport(self):
        outputTemplate = \
"""<html lang="en-US"><head><title>Character Sheet for %N</title></head>

<body>
<p><h2>%N</h2></p>

<p>Age: %A<br>
Gender: %G<br>
Origin: %O</p>

<p>Body: %Y<br>
Mind: %M<br>
Soul: %L</p>

<p>Health: %H<br>
Energy: %E<br>
ACV: %C<br>
DCV: %V</p>

<p><h3>Attributes</h3></p>
<p>%T</p>

<p><h3>Defects</h3></p>
<p>%D</p>

<p><h3>Skills</h3></p>
<p>%S</p>

<p><h3>Appearance</h3></p>
<p>%R</p>

<p><h3>Personality</h3></p>
<p>%P</p>

<p><h3>Background</h3></p>
<p>%B</p>"""
        self.realExport(outputTemplate, "HTML files (*.html)", "<br>",".html")
        
    def forumExport(self):
        outputTemplate = \
"""[b]%N[/b]

Age: %A
Gender: %G
Origin: %O

Body: %Y
Mind: %M
Soul: %L

Health: %H
Energy: %E
ACV: %C
DCV: %V

[u]Attributes[/u]
%T

[u]Defects[/u]
%D

[u]Skills[/u]
%S

[i]Appearance[/i]
%R

[i]Personality[/i]
%P

[i]Background[/i]
%B"""
        self.realExport(outputTemplate, "Text files (*.txt)", "\n")

def initWidgets(mainWindow, mainWindowReal, layout):            
    global g 
    g = OhNoesALazyGlobalClass(mainWindow, mainWindowReal, layout)
