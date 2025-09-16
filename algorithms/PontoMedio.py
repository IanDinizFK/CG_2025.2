def drowLine(start, end) -> list:
    if abs(end.x - start.x) > abs(end.y - start.y): 
        return drowLineH(start, end)
    else:
        return drowLineV(start, end)

def drowLineH(start, end) -> list:
    result = []

    dx = end.x - start.x
    dy = end.y - start.y

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x, y = start.x, start.y

    result.append([x, y])
    while x < end.x:
        if d <= 0:
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1
        result.append([x, y])
    return result

def drowLineV(start, end):
    result = []

    dx = end.x - start.x
    dy = end.y - start.y

    d = 2 * dx - dy
    incE = 2 * dx
    incNE = 2 * (dx - dy)

    x, y = start.x, start.y

    result.append([x, y])
    while y < end.y:
        if d <= 0:
            d += incE
            y += 1
        else:
            d += incNE
            y += 1
            x += 1
        result.append([x, y])
    return result