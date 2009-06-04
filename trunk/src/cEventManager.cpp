/*
Random Game Generator - The generation of time transcending tabletop games!
Copyright (C) 2009 Michael de Lang

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/

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

QString cEventManager::requestInfo()
{
    QString str = "message: {type: " + QString(REQUEST_INFO) + ";};";
    return str;
}

QString cEventManager::sendMessage(QString message)
{
    QString str = "message: {type: " + QString(MESSAGE) + "; content: \"" + message + "\";};";
    return str;
}

void cEventManager::handleMessage(QString message)
{
}


void cEventManager::keyPress(int key)
{
    keymaps.insert(pair<int, int>(key, 1));
}

void cEventManager::keyRelease(int key)
{
    keymaps.erase(key);
}
