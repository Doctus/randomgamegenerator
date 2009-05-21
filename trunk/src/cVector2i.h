#ifndef VECTOR2I_H_
#define VECTOR2I_H_

#include <ostream>
#include <cmath>
#include <cstdlib>

class cVector2i
{
    public:
    int X, Y;

    cVector2i();
    cVector2i(int x, int y);

    double length();

    cVector2i& operator+=(const cVector2i& rhs);
    const cVector2i operator+(const cVector2i& rhs);
    cVector2i& operator-=(const cVector2i& rhs);
    const cVector2i operator-(const cVector2i& rhs);
    cVector2i& operator*=(const cVector2i& rhs);
    const cVector2i operator*(const cVector2i& rhs);
    cVector2i& operator/=(const cVector2i& rhs);
    const cVector2i operator/(const cVector2i& rhs);

    const bool operator==(const cVector2i& rhs);
    const bool operator!=(const cVector2i& rhs);
    bool operator>=(cVector2i& rhs);
    bool operator<=(cVector2i& rhs);
    bool operator>(cVector2i& rhs);
    bool operator<(cVector2i& rhs);

    friend std::ostream& operator<<(std::ostream& ostr, const cVector2i& vect)
    {
        ostr << "(" << vect.X << ", " << vect.Y << ")";
        return ostr;
    }
};

#endif
