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

#include "cShapeManager.h"
#include <cmath>

bool SegmentIntersectRectangle(double a_rectangleMinX,
                               double a_rectangleMinY,
                               double a_rectangleMaxX,
                               double a_rectangleMaxY,
                               double a_p1x,
                               double a_p1y,
                               double a_p2x,
                               double a_p2y)
{
    // Find min and max X for the segment

    double minX = a_p1x;
    double maxX = a_p2x;

    if(a_p1x > a_p2x)
    {
        minX = a_p2x;
        maxX = a_p1x;
    }

    // Find the intersection of the segment's and rectangle's x-projections

    if(maxX > a_rectangleMaxX)
        maxX = a_rectangleMaxX;

    if(minX < a_rectangleMinX)
        minX = a_rectangleMinX;

    if(minX > maxX) // If their projections do not intersect return false
        return false;

    // Find corresponding min and max Y for min and max X we found before

    double minY = a_p1y;
    double maxY = a_p2y;

    double dx = a_p2x - a_p1x;

    if(abs(dx) > 0.0000001)
    {
        double a = (a_p2y - a_p1y) / dx;
        double b = a_p1y - a * a_p1x;
        minY = a * minX + b;
        maxY = a * maxX + b;
    }

    if(minY > maxY)
    {
        double tmp = maxY;
        maxY = minY;
        minY = tmp;
    }

    // Find the intersection of the segment's and rectangle's y-projections

    if(maxY > a_rectangleMaxY)
        maxY = a_rectangleMaxY;

    if(minY < a_rectangleMinY)
        minY = a_rectangleMinY;

    if(minY > maxY) // If Y-projections do not intersect return false
        return false;

    return true;
}

cShapeManager::cShapeManager()
{
    lines.resize(3);
}


void cShapeManager::addLine(int x, int y, int w, int h, int thickness)
{
    if(thickness < 1)
        thickness = 1;
    if(thickness > 3)
        thickness = 3;
    thickness--;
    lines[thickness].push_back(QRect(x, y, w, h));
}

void cShapeManager::removeLine(int x, int y, int w, int h, int thickness)
{
    int i = 0;
    if (thickness == -1)
    {
        for(thickness = 0; thickness < 3; thickness++)
        {
            while(i < lines[thickness].size()) //I think that deleting an item from QVector makes the next item take the place of the deleted item, and thus having its place decremented by one.
            {

                if(SegmentIntersectRectangle(x, y, w, h, lines[thickness][i].x(), lines[thickness][i].y(), lines[thickness][i].width(), lines[thickness][i].height()))
                    lines[thickness].remove(i);
                else
                    i++;
            }
        }
    }
    else
    {
        if(thickness < 1)
            thickness = 1;
        if(thickness > 3)
            thickness = 3;
        thickness--;
        while(i < lines[thickness].size()) //I think that deleting an item from QVector makes the next item take the place of the deleted item, and thus having its place decremented by one.
        {

            if(SegmentIntersectRectangle(x, y, w, h, lines[thickness][i].x(), lines[thickness][i].y(), lines[thickness][i].width(), lines[thickness][i].height()))
                lines[thickness].remove(i);
            else
                i++;
        }
    }
}

void cShapeManager::clearLines()
{
    for(int i = 0; i < lines.size(); i++)
    {
        lines[i].clear();
    }
}

QVector< QVector<QRect> > cShapeManager::getLines()
{
    return lines;
}
