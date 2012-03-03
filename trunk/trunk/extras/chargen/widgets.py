from PyQt4.QtCore import *
from PyQt4.QtGui import *
import besmData

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
            self.buttons.append(QRadioButton(defect))
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
        for button in self.buttons:
            if button.isChecked():
                self.selectedDefect = button.text()
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
            self.buttons.append(QRadioButton(att))
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
        for button in self.buttons:
            if button.isChecked():
                self.selectedAttribute = button.text()
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
            self.buttons.append(QRadioButton(skill))
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
        for button in self.buttons:
            if button.isChecked():
                self.selectedSkill = button.text()
        self.accept()

class CharStatsWidget(QDockWidget):
    
    def __init__(self, mainWindow):
        super(QDockWidget, self).__init__(mainWindow)
        
        self.widg = QWidget(self)
        self.setWindowTitle("Stats")
        self.setObjectName("CharStatsWidget")
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        self.charPointsBox = QComboBox(self)
        for x in range(5, 105, 5):
            self.charPointsBox.addItem(str(x))
        
        self.skillCostsBox = QComboBox(self)
        for x in sorted(besmData.SKILL_COSTS.keys()):
            self.skillCostsBox.addItem(x)
        
        self.remainingPointsLabelLabel = QLabel("Unspent Points: ")
        self.remainingPointsLabel = QLabel("1")
        self.skillPointsLabel = QLabel("Unspent SP: 20")
        
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
        self.widg.setLayout(self.layout)
        self.setWidget(self.widg)
        
        self.updatePoints()
        
        for x in (self.charPointsBox, self.body, self.mind, self.soul, self.skillCostsBox):
            x.currentIndexChanged.connect(self.updatePoints)
        
        self.addSkillButton.clicked.connect(self.addSkill)
        self.removeSkillButton.clicked.connect(self.decreaseLevel)
        self.addAttButton.clicked.connect(self.addAttribute)
        self.removeAttButton.clicked.connect(self.decreaseAttLevel)
        self.addDefectButton.clicked.connect(self.addDefect)
        self.removeDefectButton.clicked.connect(self.decreaseDefectLevel)
        self.skillsScroll.itemActivated.connect(self.increaseLevel)
        self.attScroll.itemActivated.connect(self.increaseAttLevel)
        self.defectScroll.itemActivated.connect(self.increaseDefectLevel)
        mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)
        
    def updateDerivedValues(self):
        baseacv = ((self.body.currentIndex()+self.mind.currentIndex()+self.soul.currentIndex()+3)//3)+self.getAttributeCombatValueEffect()
        basedcv = baseacv - 2
        basehealth = ((self.body.currentIndex()+self.soul.currentIndex()+2)*5)+self.getAttributeHealthEffect()
        baseenergy = ((self.mind.currentIndex()+self.soul.currentIndex()+2)*5)+self.getAttributeEnergyEffect()
        
        self.acv.setText(str(baseacv))
        self.dcv.setText(str(basedcv))
        self.health.setText(str(basehealth))
        self.energy.setText(str(baseenergy))
        self.skillPointsLabel.setText("Unspent SP: " + str((20+self.getAttributeSkillEffect())-(self.getTotalSkillCosts())))
        
    def updatePoints(self, True=False):
        if self.body.currentIndex() == 11:
            self.mind.setCurrentIndex(min(self.mind.currentIndex(), 10))
            self.soul.setCurrentIndex(min(self.soul.currentIndex(), 10))
        if self.mind.currentIndex() == 11:
            self.soul.setCurrentIndex(min(self.soul.currentIndex(), 10))
        base = (self.charPointsBox.currentIndex()+1)*5
        result = base - (self.body.currentIndex()+self.mind.currentIndex()+self.soul.currentIndex()+3)
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
            self.skillsScroll.addItem(dial.selectedSkill + " 1")
            self.skillsScroll.sortItems()
        self.updatePoints()
        
    def addAttribute(self):
        possibleAttributes = dict(besmData.ATTRIBUTES)
        if self.attScroll.count() >= 1:
            for i in range(0, self.attScroll.count()):
                del possibleAttributes[str(self.attScroll.item(i).text())[0:-2]]
        dial = AddAttributeDialog(self, possibleAttributes)
        if dial.exec_():
            self.attScroll.addItem(dial.selectedAttribute + " 1")
            self.attScroll.sortItems()
        self.updatePoints()
        
    def addDefect(self):
        possibleDefects = dict(besmData.DEFECTS)
        if self.defectScroll.count() >= 1:
            for i in range(0, self.defectScroll.count()):
                del possibleDefects[str(self.defectScroll.item(i).text())[0:-2]]
        dial = AddDefectDialog(self, possibleDefects)
        if dial.exec_():
            self.defectScroll.addItem(dial.selectedDefect + " 1")
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
        if int(str(self.defectScroll.currentItem().text())[-1:]) < 2:
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

class CharBioWidget(QDockWidget):
    
    def __init__(self, mainWindow):
        super(QDockWidget, self).__init__(mainWindow)
        
        self.widg = QWidget(self)
        self.setWindowTitle("General Info")
        self.setObjectName("CharBioWidget")
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        self.nameWidget = QLineEdit(self)
        self.genderWidget = QLineEdit(self)
        self.ageWidget = QLineEdit(self)
        self.speciesWidget = QLineEdit(self)
        self.appearanceWidget = QTextEdit(self)
        self.personalityWidget = QTextEdit(self)
        self.backgroundWidget = QTextEdit(self)
        
        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Name"), 0, 0)
        self.layout.addWidget(self.nameWidget, 0, 1)
        self.layout.addWidget(QLabel("Age"), 1, 0)
        self.layout.addWidget(self.ageWidget, 1, 1)
        self.layout.addWidget(QLabel("Gender"), 0, 2)
        self.layout.addWidget(self.genderWidget, 0, 3)
        self.layout.addWidget(QLabel("Origin"), 1, 2)
        self.layout.addWidget(self.speciesWidget, 1, 3)
        self.layout.addWidget(QLabel("Appearance"), 2, 0, 1, 2)
        self.layout.addWidget(self.appearanceWidget, 3, 0, 1, 4)
        self.layout.addWidget(QLabel("Personality"), 4, 0, 1, 2)
        self.layout.addWidget(self.personalityWidget, 5, 0, 1, 4)
        self.layout.addWidget(QLabel("Background"), 6, 0, 1, 2)
        self.layout.addWidget(self.backgroundWidget, 7, 0, 1, 4)
        self.widg.setLayout(self.layout) 
        self.setWidget(self.widg)
        
        mainWindow.addDockWidget(Qt.LeftDockWidgetArea, self)

def initWidgets(mainWindow,  mainWindowReal):
    
    CharBioWidget(mainWindowReal)
    CharStatsWidget(mainWindowReal)
