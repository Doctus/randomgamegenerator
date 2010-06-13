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


#ifndef CAMERA_H
#define CAMERA_H

#include <QtCore/QPoint>

class cCamera
{
    private:
    int x, y, w, h;

    public:
    cCamera(int x, int y, int w, int h);

    QPoint getCam();
    QPoint getAbsoluteBounds(float zoom);
    QPoint getBounds(float zoom);
    void setCam(QPoint newCam);
    void adjustCam(QPoint adjust);
    void adjustCam(int x, int y);
    void setBounds(QPoint bounds);
    void setBounds(int w, int h);
};

#endif
