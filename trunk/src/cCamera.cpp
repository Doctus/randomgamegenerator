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


#include "cCamera.h"

cCamera::cCamera(int x, int y, int w, int h)
{
    this->x = x;
    this->y = y;
    this->w = w;
    this->h = h;
}

QPoint cCamera::getCam()
{
    return QPoint(x, y);
}

QPoint cCamera::getAbsoluteBounds(float zoom)
{
    return QPoint(int(w * (1/zoom)), int(h * (1/zoom)));
}

QPoint cCamera::getBounds(float zoom)
{
    return QPoint(int(x + w * (1/zoom)), int(y + h * (1/zoom)));
}

void cCamera::setCam(QPoint newCam)
{
    x = newCam.x();
    y = newCam.y();
}

void cCamera::adjustCam(QPoint adjust)
{
    x += adjust.x();
    y += adjust.y();
}

void cCamera::adjustCam(int x, int y)
{
    this->x += x;
    this->y += y;
}

void cCamera::setBounds(QPoint bounds)
{
    w = bounds.x();
    h = bounds.y();
}

void cCamera::setBounds(int w, int h)
{
    this->w = w;
    this->h = h;
}
