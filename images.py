from PIL import Image, ImageDraw
import profile
from random import randint

# def lerp(im, xy, xy0, xy1):
#     """Interpolate linearly"""
#     x,y = xy
#     x0, y0 = xy0
#     x1, y1 = xy1
#
#     if not (x == x0 == x1) or (y == y0 == y1):
#         raise ValueError("Only vertical or horizontal lines supported")
#     elif (x == x0 == x1):  # Vertical

def cubicInterpolate(p, x):
    # WTF OO CLUSTERPOOP
    return p[1] + 0.5 * x * ( p[2] - p[0] + x * (2.0 * p[0] - 5.0 * p[1] + 4.0 * p[2] - p[3] + x * (3.0 * (p[1] - p[2]) + p[3] - p[0])))

def bicubicInterpolate(p, x, y):
    # p = 2d array
    return cubicInterpolate([cubicInterpolate(i, y) for i in p], x)

def bilerp(im, xy, xy0, xy1, tlc, trc, blc, brc):
    """Return bilinear interpolated color for coordinate tuple xy.
    xy0, xy1 = rectangle corner coordinate tuples
    tlc, trc, blc, brc = RGB color tuples for corners"""
    x, y = xy
    x0, y0 = xy0
    x1, y1 = xy1

    # Swap values so smallest is always first
    x0, x1 = (x1, x0) if x0 > x1 else (x0, x1)
    y0, y1 = (y1, y0) if y0 > y1 else (y0, y1)

    if not (x0 <= x <= x1) or not (y0 <= y <= y1):
        raise ValueError("XY not within bounding box!")

    # (x0,y0)- - -(x1,y0)
    #    |   (x,y)   |
    # (x0,y1)- - -(x1,y1)

    # Total area
    area = (x1 - x0) * (y1 - y0)

    # Distances from vert/horiz edges
    v0 = x - x0
    v1 = x1 - x
    h0 = y - y0
    h1 = y1 - y

    # Quadrant percentages
    p0 = (1.0 * v1 * h1) / area  # top left
    p1 = (1.0 * v0 * h1) / area  # top right
    p2 = (1.0 * v1 * h0) / area  # bottom left
    p3 = (1.0 * v0 * h0) / area  # bottom right

    c0 = [color * p0 for color in tlc]
    c1 = [color * p1 for color in trc]
    c2 = [color * p2 for color in blc]
    c3 = [color * p3 for color in brc]

    return (int(c0[0] + c1[0] + c2[0] + c3[0]),
            int(c0[1] + c1[1] + c2[1] + c3[1]),
            int(c0[2] + c1[2] + c2[2] + c3[2]))


width = 100
height = 100
size = (height, width)
im = Image.new('RGB', size)

draw = ImageDraw.Draw(im)

tlc = (0, 0, 0)
trc = (255, 0, 0)
cnc = (255, 255, 255)
blc = (0, 255, 0)
brc = (0, 0, 255)

draw.point((0, 0), tlc)
draw.point((width - 1, 0), trc)
draw.point((width / 2, height / 2), cnc)
draw.point((0, height - 1), blc)
draw.point((width - 1, height - 1), brc)

def bilerpQuad(xy0, xy1):
    xmin, ymin = xy0
    xmax, ymax = xy1
    c0 = im.getpixel((xmin, ymin))
    c1 = im.getpixel((xmax, ymin))
    c2 = im.getpixel((xmin, ymax))
    c3 = im.getpixel((xmax, ymax))
    # FixMe: Why does this need a +! to get full range?
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            c = bilerp(im, (x, y), (xmin, ymin), (xmax, ymax), c0, c1, c2, c3)
            draw.point((x,y), c)


def processImg(tlc, trc, blc, brc):
    # tlc = im.getpixel((0, 0))
    # trc = im.getpixel((width - 1, 0))
    # blc = im.getpixel((0, height - 1))
    # brc = im.getpixel((width - 1, height - 1))
    for x in range(0, width):
        for y in range(0, height):
            c = bilerp(im, (x, y), (0, 0), (width, height),
                       tlc, trc, blc, brc)
            draw.point((x, y), c)

for coords in [((0,0),(width/2,height/2)),
               ((width/2,0),(width-1,height/2)),
               ((0, height/2), (width/2, height-1)),
               ((width/2,height/2),(width-1,height-1))]:
    xy0, xy1 = coords
    bilerpQuad(xy0, xy1)

# processImg(tlc, trc, blc, brc)
# profile.run("processImg(tlc, trc, blc, brc)")
im.save('test.png')

