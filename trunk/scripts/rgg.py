
import rggSystem, rggChat, rggMenuBar
from rggSystem import mainWindow, connectSignal, connectChat
from rggViews import mouseMoveResponse, mousePressResponse, mouseReleaseResponse

if __name__ == '__main__':
    rggMenuBar.setupMenuBar(mainWindow)
    
    connectSignal("mouseMoveSignal(int, int)", mouseMoveResponse)
    connectSignal("mousePressSignal(int, int, int)", mousePressResponse)
    connectSignal("mouseReleaseSignal(int, int, int)", mouseReleaseResponse)
    connectChat(rggChat.chat)

    rggSystem.start()
