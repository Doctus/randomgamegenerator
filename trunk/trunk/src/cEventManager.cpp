#include "cEventManager.h"

cEventManager *cEventManager::instance;

cEventManager::cEventManager()
{
}

cEventManager* cEventManager::getInstance()
{
    if(instance == NULL)
        instance = new cEventManager();

    return instance;
}


bool cEventManager::isKeyPressed(int key)
{
    if(keymaps.find(key) != keymaps.end())
        return true;

    return false;
}


void cEventManager::keyPress(int key)
{
    keymaps.insert(pair<int, int>(key, 1));
}

void cEventManager::keyRelease(int key)
{
    keymaps.erase(key);
}
