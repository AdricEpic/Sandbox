from PIL import Image, ImageDraw
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

wd = 500
ht = 500
im = Image.new('RGB', (wd, ht))

def lerp(p1, p2, scale):
    """
    :param Point p1:
    :param Point p2:
    :param float scale:
    :return: Point linearly interpolated between p1 and p2
    :rtype : Point
    """
    return Point(p1.x + ((p2.x - p1.x) * scale),
                 p1.y + ((p2.y - p1.y) * scale))

draw = ImageDraw.Draw(im)

p1 = Point(0,0)
p2 = Point(wd-1, ht-1)
c1 = Point(wd*2, 0)
c2 = Point(-wd, ht)

points = []

for w in range(0, wd):
    scl = float(w) / wd
    a1 = lerp(p1, c1, scl)
    a2 = lerp(c1, c2, scl)
    a3 = lerp(c2, p2, scl)

    b1 = lerp(a1, a2, scl)
    b2 = lerp(a2, a3, scl)

    points.append(lerp(b1, b2, scl))

draw.line(points, fill=(255,0,0), width=1)

im.save("bezier.png")