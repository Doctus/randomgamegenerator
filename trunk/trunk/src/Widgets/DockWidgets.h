#ifndef DOCKWIDGETS_H
#define DOCKWIDGETS_H

#include <QtGui/QMainWindow>
#include <QtGui/QTextBrowser>
#include <QtGui/QLineEdit>
#include <QtGui/QDockWidget>
#include <QtGui/QVBoxLayout>
#include <QtCore/QObject>

class cDockWidgets : public QObject
{
    Q_OBJECT;

    private:
    QTextBrowser *dockWidgetEditor;
    QLineEdit *dockWidgetLineInput;
    QDockWidget *dockWidget;

    public:
    cDockWidgets(QMainWindow *mainWindow);

    void showTextDockWidgets();

    private slots:
    void processInput();
};

#endif // DOCKWIDGETS_H
