def drowLineDDA(x1: float, y1: float, x2: float, y2: float) -> list:
    if abs(x2 - x1) > abs(y2 - y1): 
        return drowLineDDAH(x1, y1, x2, y2)
    else:
        return drowLineDDAV(x1, y1, x2, y2)

def drowLineDDAH(x1: float, y1: float, x2: float, y2: float):
    result = []

    lenght = abs(x2 - x1)

    if (abs(x2 - x1) > lenght):
        lenght = abs(y2 - y1)

    xinc = (x2 - x1) / lenght
    yinc = (y2 - y1) / lenght

    x = x1
    y = y1

    result.append([round(x), round(y)])

    while(x < x2):
        x = x + xinc
        y = y + yinc

        result.append([round(x), round(y)])
    
    return result

def drowLineDDAV(x1: float, y1: float, x2: float, y2: float):
    result = []

    lenght = abs(y2 - y1)

    if (abs(y2 - y1) > lenght):
        lenght = abs(x2 - x1)

    xinc = (x2 - x1) / lenght
    yinc = (y2 - y1) / lenght

    x = x1
    y = y1

    result.append([round(x), round(y)])

    while(y < y2):
        x = x + xinc
        y = y + yinc

        result.append([round(x), round(y)])
    
    return result

