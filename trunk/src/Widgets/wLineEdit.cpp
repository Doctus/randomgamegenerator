#include "wLineEdit.h"

wLineEdit::wLineEdit(QWidget *parent) : QLineEdit(parent)
{
    position = 0;
}

void wLineEdit::keyPressEvent(QKeyEvent *event)
{
    if(event->key() == Qt::Key_Up && position > 0)
    {
        if(position == messageHistory.size())
            lastInput = text();
        setText(messageHistory.at(--position));
    }
    else if(event->key() == Qt::Key_Down && position < messageHistory.size() - 1)
    {
        setText(messageHistory.at(++position));
    }
    else if(event->key() == Qt::Key_Down && position == messageHistory.size() - 1)
    {
        setText(lastInput);
        position++;
    }
    QLineEdit::keyPressEvent(event);
}

void wLineEdit::addMessage(QString message)
{
    messageHistory.append(message);
    position = messageHistory.size();
}
