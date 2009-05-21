#ifndef CAMERA_GUARD
#define CAMERA_GUARD

class cCamera;

#include <QtCore/QPoint>

#include "cMap.h"

class cCamera
{
    private:
    QPoint cam;
    QPoint bounds;

    friend class cMap;

    cCamera(int x, int y, int w, int h);

    public:
    QPoint getCam();
    QPoint getBounds();
    void setCam(QPoint newCam);
    void adjustCam(QPoint adjust);
};

#endif
