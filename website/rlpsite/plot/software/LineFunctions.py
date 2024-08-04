""""Supporting functions when working with lines and line equations."""

from shapely import LineString, intersection
import numpy as np


X,Y = 0,1
linep1idx, linep2idx = 0, 1



def checkVertical(c1, c2):
    """Returns True if points are on a vertical line.
    
    Vertical lines have different line equations and their normal lines are calculated differently.
    
    """

    (x1, y1) = c1
    (x2, y2) = c2
    if x2-x1 == 0:
        return True
    return False


def lineEQ(c1, c2):
    """Returns line equation for two points as a tuple (gradient, cvalue, isVertical).
    
    Line equations are used to find the normal line for two adjacent lines in an rlp,
    which allows houses to be placed considering both lines so valuable space isn't missed.
    
    Line equations are also used to continue to place houses padded from another house,
    rather than padded from a line, which maximises the rlp area used to place houses.
    
    """

    if checkVertical(c1, c2):
        # should raise an exception here rather than returning a False value.
        # PADDING WORKS DIFFERENTLY IN THIS CASE. THE NORMAL EQUATION IS JUST SOMETHING ELSE.
        return (0, 0, True)
    
    (x1, y1) = c1
    (x2, y2) = c2
    
    m = (y2-y1)/(x2-x1)
    c = y1-(m*x1)
    return (m, c, False)


def orderLine(line):
    """Returns line as a list. The coordinate with the smaller x-value is first."""

    line = [coord for coord in line]

    if line[linep1idx][X] > line[linep2idx][X]:
        temp = line[linep1idx]
        line[linep1idx] = line[linep2idx] 
        line[linep2idx] = temp 

    return line


def findAngle(line):
    """Returns the angle between one line and the horizontal, with error from use of pi.
    
    Due to pi error, equality comparisons of results of this function should use rounded values.

    """

    xs1, xe1 = line.xy[0]
    ys1, ye1 = line.xy[1]
    if xs1 == xe1:
        angle = np.pi/2
    else:
        angle = np.arctan((ye1-ys1)/(xe1-xs1))
    return angle


def isParallel(line1, line2):
    """"Returns true if two LineStrings have the same angle to 3 decimal places.
    
    This is to account for lines rotated using pi (like with radians).

    """

    angle1 = findAngle(line1)
    angle2 = findAngle(line2)

    if round(angle1, 3) == round(angle2, 3):
        return True
    else:
        return False
    

def leqtoline(leq, polygon):
        """Returns a line for a line equation. The returned line touches the edges of the polygon.
        
        The returned line is a LineString.
        
        """

        minxval = maxxval = polygon.exterior.coords[0][X]
        for coord in polygon.exterior.coords:
            if coord[X]<minxval:
                minxval=coord[X]
            if coord[X]>maxxval:
                maxxval=coord[X]

        verylongline = [(minxval, lineyval(leq, minxval)) , (maxxval, lineyval(leq, maxxval))]
        shorterline = intersection(polygon, LineString( verylongline ))

        return shorterline


def normalLineEQ(leq, point):
    """Returns equation for the normal of a given line as a tuple (gradient, cvalue, isVertical).
    
    The normal line goes through the given point and the given line, and is used to pad for new rows in the rlp.
    
    The given line is given as a tuple (gradient, cvalue, isVertical).

    Returns a special value if the given line is horizontal (returns (0,0,True)).
    
    """

    x, y = point[X], point[Y]
    m, c, isVertical = leq

    if isVertical : return (0, y, False)
    if m==0 : return (0, 0, True)
    
    normalm = -1 / m
    normalc = y - (normalm*x)

    return (normalm, normalc, False)


def lineyval(leq, x):
    """Returns the y value of a line equation given the x value."""
    
    m, c, isVertical = leq
    return (m*x + c)


def linexval(leq, y):
    """Returns the x value of a line equation given the y value."""
    
    m, c, isVertical = leq
    return ((y - c)/m)


def linecval(m, p):
    """Returns the c value of a line with gradient m that goes through point p."""
    
    x, y = p
    return y-(m*x)


def point_from_distance(leq, init_point, desired_distance, left_not_right=True):
    """Finds a new point using a line equation, desired distance, and initial point.

    Returns (x,y).

    TODO: Fix so that a point right of the init point can be chosen over left
    
    """

    x = init_point[X]
    y = lineyval(leq, x)

    measureLine = LineString( [(x,y), (x-1, lineyval(leq, x-1))] )

    if measureLine.length==0:
        print("initpoint:", init_point)
        print("desireddistance:", desired_distance)
        print("measureLine:", measureLine)
    else:
        factor = desired_distance / measureLine.length

    new_point = (x-factor, lineyval(leq, x-factor))
    
    return new_point