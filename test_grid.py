from unittest import TestCase
import grid


class TestGrid(TestCase):
    def test_zeroDimensions(self):
        """Grid dimensions can not be zero."""
        self.assertRaises(ValueError, grid.Grid, (0, 0))

    def test_negativeDimensions(self):
        """Grid dimensions must be positive."""
        self.assertRaises(ValueError, grid.Grid, (-1, 1))
        self.assertRaises(ValueError, grid.Grid, (1, -1))
        self.assertRaises(ValueError, grid.Grid, (-1, -1))

    def test_floatDimensions(self):
        """Float dimensions are not accepted."""
        self.assertRaises(ValueError, grid.Grid, (1.1, 1))
        self.assertRaises(ValueError, grid.Grid, (1, 1.1))
        self.assertRaises(ValueError, grid.Grid, (1.1, 1.1))

        self.assertRaises(ValueError, grid.Grid, (1.0, 1))
        self.assertRaises(ValueError, grid.Grid, (1, 1.0))
        self.assertRaises(ValueError, grid.Grid, (1.0, 1.0))

    def test_incorrectNumberOfDimensions(self):
        """Only two dimensions are supported."""
        self.assertRaises(ValueError, grid.Grid, (1,))
        self.assertRaises(ValueError, grid.Grid, (1, 2, 3))

    def test_containsPoint(self):
        """
        Returns true for points within grid range, returns false for points
        outside of grid range.
        """
        self.grid = grid.Grid((5, 5))
        for x in xrange(-1, self.grid.width):
            for y in xrange(-1, self.grid.height):
                if (0 <= x < self.grid.width) and (0 <= y < self.grid.height):
                    self.assertTrue(self.grid.containsPoint((x, y)))
                else:
                    self.assertFalse(self.grid.containsPoint((x, y)))

    def test_rows(self):
        """Grid rows split correctly."""
        test_grid = grid.Grid((2, 2))
        expected_rows = [(0, 1), (2, 3)]
        grid_value = 0
        for y in range(test_grid.height):
            for x in range(test_grid.width):
                test_grid[(x, y)] = grid_value
                grid_value += 1
        self.assertTrue(test_grid.rows() == expected_rows)

    def test_columns(self):
        """Grid columns split correctly"""
        test_grid = grid.Grid((2, 2))
        expected_columns = [(0, 2), (1, 3)]
        grid_value = 0
        for y in range(test_grid.height):
            for x in range(test_grid.width):
                test_grid[(x, y)] = grid_value
                grid_value += 1
        self.assertTrue(test_grid.columns() == expected_columns)