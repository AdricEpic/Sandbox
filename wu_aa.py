# Adapted from http://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm

from math import floor


def ipart(x):
    return int(x)


def round_(x):
    return ipart(x + 0.5)


def fpart(x):
    if x < 0:
        return 1 - (x - floor(x))
    return x - floor(x)


def rfpart(x):
    return 1 - fpart(x)


def f2c(f):
    """
    Convert float to grey color tuple
    :param float f: Fractional grey value
    :return: Gray color tuple
    :rtype : (int, int, int)
    """
    return (int(f * 255),) * 3


def draw_line_aa(x0, y0, x1, y1, draw):
    """
    Draw anti-aliased line from (x0,y0) to (x1,y1)
    :param float x0: First point's x-value
    :param float y0: First point's y-value
    :param float x1: Second point's x-value
    :param float y1: Second point's y-value
    :param ImageDraw.Draw draw: Surface to draw on
    """

    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)

    dy = y1 - y0
    dx = x1 - x0

    grad = dy / dx

    # First endpoint
    x_end = round_(x0)
    y_end = y0 + grad * (x_end - x0)
    x_gap = fpart(x0 + 0.5)
    xpx11 = x_end
    ypx11 = ipart(y_end)

    if steep:
        draw.point((ypx11, xpx11), f2c(rfpart(y_end) * x_gap))
        draw.point((ypx11 + 1, xpx11), f2c(fpart(y_end) * x_gap))
    else:
        draw.point((xpx11, ypx11), f2c(rfpart(y_end) * x_gap))
        draw.point((xpx11, ypx11 + 1), f2c(fpart(y_end) * x_gap))
    inter_y = y_end + grad  # first y intersection

    # Second endpoint
    x_end = round_(x1)
    y_end = y1 + grad * (x_end - x1)
    x_gap = fpart(x1 + 0.5)
    xpx12 = x_end
    ypx12 = ipart(y_end)

    if steep:
        draw.point((ypx12, xpx12), f2c(rfpart(y_end) * x_gap))
        draw.point((ypx12 + 1, xpx12), f2c(fpart(y_end) * x_gap))
    else:
        draw.point((xpx12, ypx12), f2c(rfpart(y_end) * x_gap))
        draw.point((xpx12, ypx12 + 1), f2c(fpart(y_end) * x_gap))

    for x in xrange(xpx11 + 1, xpx12 - 1):
        if steep:
            ax = ipart(inter_y)
            ay = x
            bx = ax + 1
            by = x
        else:
            ax = x
            ay = ipart(inter_y)
            bx = x
            by = ay + 1
        draw.point((ax, ay), f2c(rfpart(inter_y)))
        draw.point((bx, by), f2c(fpart(inter_y)))
        inter_y += grad  # first y intersection
