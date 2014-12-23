from itertools import izip


class Grid(object):
    """Simple list wrapper providing grid-like interaction"""
    def __init__(self, dimensions, null_value=None):
        self.width, self.height = dimensions
        self.maxX = self.width - 1
        self.maxY = self.height - 1
        self._array = [null_value] * (self.width * self.height)

    def __pointIndex(self, point):
        """Convert point coordinates to list index"""
        return point[0] + (self.width * point[1])

    def __getitem__(self, point):
        if not ((0 <= point[0] < self.width) and (0 <= point[1] < self.height)):
            raise ValueError("Point {} outside of range (0, 0) - {}".format(point, (self.maxX, self.maxY)))
        return self._array[self.__pointIndex(point)]

    def __setitem__(self, point, value):
        if not self.containsPoint(point):
            raise ValueError("Point {} outside of range (0, 0) - {}".format(point, (self.maxX, self.maxY)))
        self._array[self.__pointIndex(point)] = value

    def containsPoint(self, point):
        """Return True if point is contained within grid bounds."""
        return (0 <= point[0] < self.width) and (0 <= point[1] < self.height)

    def rows(self):
        """Return list of contents tuples grouped by row"""
        return list(izip(*([iter(self._array)] * self.width)))

    def columns(self):
        """Return list of contents tupkes grouped by column"""
        return list(izip(*self.rows()))


if __name__ == '__main__':
    test = Grid((2, 4))
    test[(0, 0)] = "Test"
    test[(1, 1)] = "Herp"
    test[(0, 2)] = "Foo"
    test[(test.maxX, test.maxY)] = "End"

    # print test[(0,0)]
    for row in test.rows():
        print row
    print
    for column in test.columns():
        print column
    print
    print test.rows()[0]

    # Test exception when assigning out of bounds
    # test[(4,5)] = "WRONG"