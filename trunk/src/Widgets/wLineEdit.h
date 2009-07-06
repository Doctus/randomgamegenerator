#ifndef WLINEEDIT_H
#define WLINEEDIT_H

#include <QtGui/QLineEdit>
#include <QtGui/QWidget>
#include <QtGui/QKeyEvent>
#include <QtCore/QVector>
#include <QtCore/QString>

class wLineEdit : public QLineEdit
{
    private:
    QVector<QString> messageHistory;
    QString lastInput;
    int position;

    public:
    wLineEdit(QWidget *parent);

    void keyPressEvent(QKeyEvent *event);
    void addMessage(QString message);
};

#endif // WLINEEDIT_H
