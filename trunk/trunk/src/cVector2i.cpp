#include "cVector2i.h"

cVector2i::cVector2i()
{
    X = 0;
    Y = 0;
}

cVector2i::cVector2i(int x, int y)
{
    X = x;
    Y = y;
}

double cVector2i::length()
{
    return sqrt(abs(X) + abs(Y));
}

cVector2i& cVector2i::operator+=(const cVector2i& rhs)
{
    X += rhs.X;
    Y += rhs.Y;
    return *this;
}

const cVector2i cVector2i::operator+(const cVector2i& rhs)
{
    return cVector2i(*this)+=rhs;
}

cVector2i& cVector2i::operator-=(const cVector2i& rhs)
{
    X -= rhs.X;
    Y -= rhs.Y;
    return *this;
}

const cVector2i cVector2i::operator-(const cVector2i& rhs)
{
    return cVector2i(*this)-=rhs;
}

cVector2i& cVector2i::operator*=(const cVector2i& rhs)
{
    X *= rhs.X;
    Y *= rhs.Y;
    return *this;
}

const cVector2i cVector2i::operator*(const cVector2i& rhs)
{
    return cVector2i(*this)*=rhs;
}

cVector2i& cVector2i::operator/=(const cVector2i& rhs)
{
    X /= rhs.X;
    Y /= rhs.Y;
    return *this;
}

const cVector2i cVector2i::operator/(const cVector2i& rhs)
{
    return cVector2i(*this)/=rhs;
}

const bool cVector2i::operator==(const cVector2i& rhs)
{
    return (rhs.X == X && rhs.Y == Y);
}

const bool cVector2i::operator!=(const cVector2i& rhs)
{
    return !(*this == rhs);
}

bool cVector2i::operator>=(cVector2i& rhs)
{
    return (length() >= rhs.length());
}

bool cVector2i::operator<=(cVector2i& rhs)
{
    return (length() <= rhs.length());
}

bool cVector2i::operator>(cVector2i& rhs)
{
    return (length() > rhs.length());
}

bool cVector2i::operator<(cVector2i& rhs)
{
    return (length() < rhs.length());
}
