#include "wAction.h"

wAction::wAction(QString &text, QObject *parent, int id) : QAction(text, parent)
{
    this->id = id;
}

int wAction::getId()
{
    return id;
}
