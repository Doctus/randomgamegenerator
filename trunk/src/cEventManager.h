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


#ifndef CEVENTMANAGER_H
#define CEVENTMANAGER_H

#include <map>
#include <iostream>

class cEventManager;

#include "Widgets/wGLWidget.h"

using namespace std;

class cEventManager
{
    private:
    map<int, int> keymaps;
    static cEventManager* instance;

    cEventManager();

    friend class wGLWidget;

    public:
    bool isKeyPressed(int key);
    static cEventManager* getInstance();

    private:
    void keyPress(int key);
    void keyRelease(int key);
};

#endif // CEVENTMANAGER_H
