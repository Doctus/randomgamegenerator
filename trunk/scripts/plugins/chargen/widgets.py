from PyQt4.QtCore import *
from PyQt4.QtGui import *
import besmWidgets

def promptButtonSelection(prompt, text=[], defaultButton = 0, mainWindow=None):
    convertedText = ()
    if text is not tuple: #lists/dictionaries make this function a sad panda :(
        convertedText = (text)
    else:
        convertedText = text

    if(len(convertedText) == 0):
        return -1

    buttons = []

    from PyQt4.QtGui import QMessageBox
    questionDialog = QMessageBox(mainWindow);
    questionDialog.setText(prompt);

    j = len(convertedText) - 1
    while(j >= 0):
        newButton = questionDialog.addButton(convertedText[j], QMessageBox.AcceptRole);
        buttons.insert(0, newButton);
        if(j == defaultButton):
            questionDialog.setDefaultButton(newButton)
        j -= 1

    questionDialog.exec_()

    i = 0
    for button in buttons:
        if(questionDialog.clickedButton() == button):
            return i
        i += 1

    return -1

def initWidgets(mainWindow, mainWindowReal):
    #selection = promptButtonSelection("Select a game.", ("Nobilis", "BESM"), mainWindow)
    #if selection == 0:
    #    nobilisWidgets.initWidgets(mainWindow, mainWindowReal)
    #elif selection == 1:
    besmWidgets.initWidgets(mainWindow, mainWindowReal)

