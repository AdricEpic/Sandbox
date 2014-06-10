import os
from time import sleep


def clear():
    #os.system('cls')
    print "\n" * 100
    
class Pixel(object):
    """A single picture element."""
    def __init__(self, value):
        self.__value = value
        
    def setValue(self, value):
        """Assign new pixel value."""
        # Clamp values to [0,1]
        self.__value = max(0, min(value, 1))

class Screen(object):
    """A grid of picture elements."""
    def __init__(self, width, height):
        self._width = width
        self._height = height
        
        self._buffer = [[" " for i in range(self._width)] for i in range(self._height)]
        
    def show(self):
        clear()
        print " " + "-" * self._width + " "
        for row in self._buffer:
            rowData = ""
            for i in row:
                rowData += str(i)
            print "|" + rowData + "|"
        print " " + "-" * self._width + " "
        self.clearBuffer()
        
    def getPixel(self):
        return self._buffer[y][x]
    
    def setPixel(self, x, y, val):
        if isinstance(val, (basestring, list, tuple)):
            val = val[0]
        self._buffer[y][x] = val
        
    def drawHorizLine(self, y, x1, x2, val):
        for x in range(x2 - x1):
            self.setPixel(x1 + x, y, val)
            
    def drawVertLine(self, x, y1, y2, val):
        for y in range(y2 - y1):
            self.setPixel(x, y1 + y, val)
            
    def clearBuffer(self):
        self._buffer =[[" " for i in range(self._width)] for i in range(self._height)]
            
    
def main():
    baseFR = 12
    framerate = 1.0 / 12
    testScreen = Screen(80, 20)
    testScreen.show()
    for i in range(testScreen._width):
        testScreen.drawVertLine(i, 5, 10, "V")
        #clear()
        testScreen.show()
        sleep(framerate)
        
    
if __name__ == "__main__":
    main()