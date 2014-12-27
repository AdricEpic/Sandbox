from itertools import izip


class Grid(object):
    """Simple list wrapper providing grid-like interaction"""
    def __init__(self, dimensions, null_value=None):

        if len(dimensions) == 2:
            self.width, self.height = dimensions
        else:
            raise ValueError("Incorrect number of dimensions provided")

        if not (isinstance(self.width, int) and isinstance(self.height, int)):
            raise ValueError("Grid dimensions must be integers.")
        elif (self.width <= 0) or (self.height <= 0):
            raise ValueError("Grid dimensions must be non-zero and positive.")

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
