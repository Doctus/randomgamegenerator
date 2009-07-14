#ifndef WACTION_H
#define WACTION_H

#include <QtGui/QAction>

class wAction : public QAction
{
    private:
    int id;

    public:
    wAction(QString &text, QObject *parent, int id);

    int getId();
};

#endif // WACTION_H
