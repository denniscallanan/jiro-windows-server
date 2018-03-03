import math

class Angle:

    RADIANS = lambda x:x
    DEGREES = math.degrees

    @staticmethod
    def facing(vec1, vec2, mode=RADIANS):
        diff = vec2 - vec1
        if   diff.x >= 0 and diff.y >= 0: additional = 0
        elif diff.x >= 0 and diff.y <  0: additional = math.pi
        elif diff.x <  0 and diff.y <  0: additional = math.pi
        elif diff.x <  0 and diff.y >= 0: additional = 0
        return mode(math.atan(diff.x / float(diff.y)) + additional)

    @staticmethod
    def constrain(angle, a=0):
        while (angle < a): angle += a + 360
        while (angle >= a + 360): angle -= a + 360
        return angle