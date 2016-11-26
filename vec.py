import operator
import math
 
class Vector(object):
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Vector({}, {})'.format(self.x, self.y)

    @classmethod
    def polarVector(cls, angle, mag):
        return cls(math.cos(angle) * mag, math.sin(angle) * mag)

    @classmethod
    def magVector(cls, x, y, mag):
        a = mag / math.sqrt(x**2 + y**2)
        return cls(x * a, y * a)





x1=8
print x1
