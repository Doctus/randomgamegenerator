from rggSystem import injectMain, SAVE_DIR
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
from rggJson import loadString, jsonload
from rggConstants import *
import os

if __name__ == '__main__':
    fieldtemp = ["English"]
    app = QApplication(['RGG in Space'])

    try:
        js = jsonload(os.path.join(SAVE_DIR, "lang_settings.rgs"))
        fieldtemp[0] = loadString('lang.language', js.get('language'))
    except:
        print("no language settings detected")

    if fieldtemp[0] != "English":
        transfile = ""
        if fieldtemp[0] == "Japanese":
            transfile = "rgg_py_ja"
        if fieldtemp[0] == "Dutch":
            transfile = "rgg_py_nl"
        if fieldtemp[0] == "German":
            transfile = "rgg_py_de"

        trans = QTranslator()
        if not trans.load(transfile):
            print(transfile + " not found")
        app.installTranslator(trans)

    qgf = QGLFormat.defaultFormat()
    qgf.setSampleBuffers(True)
    QGLFormat.setDefaultFormat(qgf)

    main = injectMain()
    
    import rggRPC, rggViews
    from rggSignalConfig import connectEvents
    
    # Initialize view state.
    s = rggViews._state
    s.initialize(app)
    
    server = rggRPC.server
    client = rggRPC.client
    
    connectEvents(client, server, s.menu, s.cwidget, s.icwidget, s.dwidget, s.uwidget, main.glwidget)
    
    # Start execution
    try:
        main.show()
        app.exec_()
    finally:
        rggViews.autosaveSession()
        client.close()
