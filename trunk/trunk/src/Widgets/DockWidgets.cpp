#include "DockWidgets.h"

cDockWidgets::cDockWidgets(QMainWindow *mainWindow) : QObject(mainWindow)
{
    dockWidgetEditor = new QTextBrowser(mainWindow);
    dockWidgetLineInput = new QLineEdit(mainWindow);
    dockWidget = new QDockWidget(QObject::tr("Dock Widget"), mainWindow);

    QWidget *dockWidgetContents = new QWidget(mainWindow);
    QVBoxLayout *layout = new QVBoxLayout(dockWidgetContents);

    layout->addWidget(dockWidgetEditor);
    layout->addWidget(dockWidgetLineInput);

    dockWidget->show();
    dockWidget->setAllowedAreas(Qt::LeftDockWidgetArea |
                                 Qt::BottomDockWidgetArea);
    dockWidget->setWidget(dockWidgetContents);
    mainWindow->addDockWidget(Qt::LeftDockWidgetArea, dockWidget);

    QObject::connect((QObject*)dockWidgetLineInput, SIGNAL(returnPressed()), (QObject*)this, SLOT(processInput()));
}

void cDockWidgets::showTextDockWidgets()
{
    dockWidget->show();
}

void cDockWidgets::processInput()
{

    QString str = dockWidgetLineInput->text();

    dockWidgetEditor->insertHtml("<div style=\"background-color: #00ff00\">" + str + "</div><br />");
    dockWidgetLineInput->clear();
}
