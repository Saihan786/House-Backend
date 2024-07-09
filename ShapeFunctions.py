""""Supporting functions when trying to work with lines and polygons."""

from shapely import Polygon, LineString, affinity
import numpy as np
import geopandas
import matplotlib.pyplot as plt


X,Y = 0,1

def findLongestLine(polygon):
    """Returns longest line of the polygon."""
    b = polygon.boundary.coords
    lines = [LineString(b[point:point+2]) for point in range(len(b)-1)]

    length = 0
    longestlineindex = 0
    for i in range(len(lines)):
        if lines[i].length>length:
            length=lines[i].length
            longestlineindex = i

    return lines[longestlineindex].coords


def orderLine(line):
    """Returns line as a list. The coordinate with the smaller x-value is first."""
    
    linep1, linep2 = 0, 1

    line = [coord for coord in line]

    if line[linep1][X] > line[linep2][X]:
        temp = line[linep1]
        line[linep1] = line[linep2] 
        line[linep2] = temp 

    return line


def findAngle(line):
    """Returns the angle between two lines, with error from use of pi.
    
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
    """"Returns true if two lines have the same angle to 3 decimal places.
    
    This is to account for lines rotated using pi (like with radians).

    """

    angle1 = findAngle(line1)
    angle2 = findAngle(line2)

    if round(angle1, 3) == round(angle2, 3):
        return True
    else:
        return False
    
    
def rotatePolygon(resultLine, polygon, showRotation=False):
    """"Rotates the polygon until it is parallel to the line.
    
    Prints meta information about the rotation and displays it if boolean is set to True.
        NOTE: In order to effectively display the rotation, the resultLine and polygon must be relatively close to each other.
    
    Returns the rotated polygon.
    
    """

    oldPolygon = polygon
    polygonLine = LineString([polygon.exterior.coords[0], polygon.exterior.coords[1]])

    resultAngle, changeAngle = findAngle(resultLine), findAngle(polygonLine)
    polygon = affinity.rotate(polygon, resultAngle-changeAngle, origin="centroid", use_radians=True)
    polygonLine = LineString([polygon.exterior.coords[0], polygon.exterior.coords[1]])
    

    if showRotation:
        ax = geopandas.GeoSeries(resultLine).plot()
        geopandas.GeoSeries(oldPolygon).plot(ax=ax, color="red")
        geopandas.GeoSeries(polygon).plot(ax=ax, color="green")
        plt.show()

        print("Original angle of polygonLine is", changeAngle)
        print("The rotated angle of polygonLine should be", resultAngle)
        print("The actual rotated angle is", findAngle(polygonLine))
        if isParallel(polygonLine, resultLine):
            print("Successful rotation")
        else:
            print("Unsuccessful rotation")
    
    return polygon


def moveToOrigin(polygon, showTranslation=False):
    """Moves the polygon until two of its vertices touch the axis lines.

    Exists the option to show the translation, which is only effective if the distance translated is not too large.
    
    Returns the moved polygon.
    
    """

    X,Y = 0,1
    leftmost = polygon.exterior.coords[0][X]
    bottom = polygon.exterior.coords[0][Y]
    for coord in polygon.exterior.coords[1:-1]:
        if coord[X] < leftmost : leftmost=coord[X]
        if coord[Y] < bottom : bottom=coord[Y]
    
    shiftcoords = [(coord[X]-leftmost, coord[Y]-bottom) for coord in polygon.exterior.coords[:-1]]

    if showTranslation:
        ax = geopandas.GeoSeries(Polygon(shiftcoords).exterior).plot(color="green")
        geopandas.GeoSeries(polygon.exterior).plot(ax=ax, color="red")
        plt.show()
    
    return Polygon(shiftcoords)
    

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


def normalLineEQ(leq, point):
    """Returns equation for the normal of a given line as a tuple (gradient, cvalue, isVertical).
    
    The normal line meets the given line and the given point, and is used to pad for new rows in the rlp.
    
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