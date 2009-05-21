#include "cCamera.h"

cCamera::cCamera(int x, int y, int w, int h)
{
    cam.setX(x);
    cam.setY(y);
    bounds.setX(w);
    bounds.setY(h);
}

QPoint cCamera::getCam()
{
    return cam;
}

QPoint cCamera::getBounds()
{
    return bounds;
}

void cCamera::setCam(QPoint newCam)
{
    cam = newCam;
}

void cCamera::adjustCam(QPoint adjust)
{
    cam += adjust;
}
