import os
from time import sleep


def clear():
    """Clear terminal view."""
    os.system('cls')
    
class Pixel(object):
    """A single picture element."""
    # Class gradient
    __gradient = " .:;+=xX$&"

    def __init__(self, value=0.0):
        self.__value = value
        
    def setValue(self, value):
        """Assign new pixel value."""
        # Clamp values to [0,1]
        self.__value = max(0, min(value, 1))
        
    def __str__(self):
        # Map __value to gradient.
        return self.__gradient[int(self.__value * (len(self.__gradient) - 1))]

class Screen(object):
    """A grid of picture elements."""
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        # Create 2D array of pixels
        # ToDo - rewrite as 1D array?
        self.__buffer = [[Pixel(0) for i in range(self.__width)] for i in range(self.__height)]
        
    def show(self):
        """Print buffer to console."""
        
        clear()        
        print " " + "-" * self.__width + " "
        
        for row in self.__buffer:
            rowData = "".join(str(i) for i in row)
            print "|" + rowData + "|"

        print " " + "-" * self.__width + " "
        self.clearBuffer()
        
    def getPixel(self):
        """Return pixel object at coordinates."""
        return self.__buffer[y][x]
    
    def setPixel(self, x, y, val):
        """Set new pixel value"""
        self.__buffer[y][x].setValue(val)
        
    def drawHorizLine(self, y, x1, x2, val):
        """Draw a line between (x1, y) and (x2, y)."""
        for x in range(x2 - x1):
            self.setPixel(x1 + x, y, val)
            
    def drawVertLine(self, x, y1, y2, val):
        """Draw a line between (x, y1) and (x, y2)."""
        for y in range(y2 - y1):
            self.setPixel(x, y1 + y, val)
            
    def clearBuffer(self):
        """Reset buffer to display nothing."""
        self.__buffer =[[Pixel() for i in range(self.__width)] for i in range(self.__height)]
        
    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
            
    
def main():
    # Set up screen
    # ToDo - Give screen configurable refresh rate
    framerate = 1.0 / 12
    testScreen = Screen(80, 20)
    
    testScreen.show()
    # Animate vertical line moving across screen
    for i in range(testScreen.width):
        testScreen.drawVertLine(i, 5, 10, 0.5)
        testScreen.show()
        sleep(framerate)
        
    
if __name__ == "__main__":
    main()