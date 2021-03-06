import random
import math

# ToDo: Prevent branches growing into the ground
# ToDo: Decrease growth

class Branch(object):
    # Rotation parameters
    branch_rotation_min = 10
    branch_rotation_max = 45
    branch_wobble = 12  # Degrees trunk rotation can vary. This must be an int b/c of randrange.

    # Branching parameters
    min_branching_width = 0.75
    branch_rate_base = 0.01
    branch_rate_max = 0.175
    branch_rate_growth = 0.01  # Add to branching chance on unsuccessful branch

    # Growth parameters
    trunk_transfer = 0.5  # Percent of trunk width carried over when spawning new trunk segment
    growth_scale = 0.915  # Percent of growth rate to propogate to child segments
    length_rate = 5  # Length units to add per growth
    width_rate = 0.15  # Width units to add per growth

    def __init__(self, parent=None, root_location=None, rotation=None, width=None):

        self._root_location = root_location if root_location else (0, 0)

        self.parent = parent
        self.trunk = None
        self.child = None
        self.length = 0
        self.width = width if width is not None else 0
        self.age = 0
        self.branch_chance = self.branch_rate_base
        self.rotation = rotation if rotation is not None else -90

        self.grow()

    def grow(self, scale=1):
        """Incremental growth iteration"""
        self.width += self.width_rate * scale
        if self.trunk is None:
            self.length += self.length_rate * scale
            if self.width > self.min_branching_width:  # Don't start branching till min width reached
                if random.random() < self.branch_chance:
                    self.trunk = Branch(parent=self, width=self.width*self.trunk_transfer,
                                        rotation=random.randrange(-1 * self.branch_wobble, self.branch_wobble))
                    self.child = Branch(parent=self, rotation=math.copysign(random.randrange(self.branch_rotation_min,
                                                                                             self.branch_rotation_max),
                                                                            random.randrange(-1, 1)))
                else:
                    self.branch_chance += (self.branch_chance < self.branch_rate_max) * self.branch_rate_growth
        else:
            self.trunk.grow(scale=scale*self.growth_scale)
            self.child.grow(scale=scale*self.growth_scale)
        self.age += 1

    def angle(self):
        if self.parent is not None:
            return self.rotation + self.parent.angle()
        else:
            return self.rotation

    def startpoint(self):
        if self.parent:
            return self.parent.endpoint()
        else:
            return self._root_location

    def endpoint(self):
        x, y = self.startpoint()
        angle_rads = math.radians(self.angle())
        return x + math.cos(angle_rads) * self.length, y + math.sin(angle_rads) * self.length

    def segments(self):
        segments = []
        if not self.parent:
            segments.append(self)

        if self.trunk:
            segments.append(self.trunk)
            segments.extend(self.trunk.segments())
        if self.child:
            segments.append(self.child)
            segments.extend(self.child.segments())

        return segments


if __name__ == "__main__":
    from PIL import Image, ImageDraw

    img_dims = (700, 550)
    im = Image.new("RGB", img_dims)
    draw = ImageDraw.Draw(im)
    color = (102, 83, 71)

    test = Branch(root_location=(img_dims[0] / 2, img_dims[1]))
    test.rotation += math.copysign(random.randrange(-1 * (test.branch_wobble / 4), test.branch_wobble / 4),
                                   random.randrange(-1, 1))
    for i in range(100):
        test.grow()
    for seg in test.segments():
        print seg.angle()
        draw.line([seg.startpoint(), seg.endpoint()], width=int(seg.width), fill=color)
    im.save("tree.png")