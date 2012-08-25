import random

def _getBirthday():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for x in range(0,12):
        mchoose = random.choice(months)

        if mchoose == 'April' or 'June' or 'September' or 'November':
            days = range(1,31)
        elif mchoose == 'February':
            days = range(1,30)
        else:
            days = range(1,32)

        dchoose = random.choice(days)
        
    stringTime = str(mchoose) + " " + str(dchoose)

    return stringTime

def getName(args):
    return _getBirthday()
