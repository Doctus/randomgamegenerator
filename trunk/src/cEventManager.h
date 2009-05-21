#ifndef CEVENTMANAGER_H
#define CEVENTMANAGER_H

#include <map>
#include <iostream>

class cEventManager;

#include "Widgets/GLWidget.h"

using namespace std;

class cEventManager
{
    private:
    map<int, int> keymaps;
    static cEventManager* instance;

    cEventManager();

    friend class GLWidget;

    public:
    bool isKeyPressed(int key);
    static cEventManager* getInstance();

    private:
    void keyPress(int key);
    void keyRelease(int key);
};

#endif // CEVENTMANAGER_H
