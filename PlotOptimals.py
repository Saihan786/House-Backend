# don't consider budget or road costs
# might be easier to work with one housetype for now

from HRGenerator import ManageHouseTypes, generateBestTypes
import matplotlib.pyplot as plt
from RedLinePlot import getRLP, getPath
from shapely import Polygon, LineString, affinity
from AddDataToDF import coords
import geopandas
import numpy as np


NAME, REVENUE, COST, WIDTH, LENGTH, SIZE = 0, 1, 2, 3, 4, 5

rlp = getRLP(getPath())
rlp = rlp.to_crs(epsg=27700)
rlp["name"] = ["rlp"]
rlppolygon = rlp.geometry[0]
oldrlpcoords = coords()

def fillMHT(mht):
    mht.addNewHouseType("ht1", 100000, 0, 25, 30)
    mht.addNewHouseType("ht2", 150000, 0, 50, 50)


def makeUnitPolygons(housetypes):
    """
    Returns a list of unit polygons for each housetype
    
    Unit polygons can be adjusted around the rlp by adding to its x and y values.
    """

    unitPolygons = []
    for ht in housetypes:
        # (name, revenue, cost, width, length, size)
        point1 = (0,0)
        point2 = (0+ht[WIDTH],0)
        point3 = (0,0+ht[LENGTH])
        point4 = (0+ht[WIDTH],0+ht[LENGTH])
        unitPolygons.append(Polygon([point1, point2, point4, point3, point1]))
        
    # geopandas.GeoSeries(unitPolygons).plot()
    # for polygon in unitPolygons:
    #     plt.plot(*polygon.exterior.xy)
    # plt.show()

    return unitPolygons



def findAngle(line):
    """
    Returns the angle between two lines, with error from use of pi.
    
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
    """"
    Returns true if two lines have the same angle to 3 decimal places.
    
    This is to account for lines rotated using pi (like with radians).
    """

    angle1 = findAngle(line1)
    angle2 = findAngle(line2)

    if round(angle1, 3) == round(angle2, 3):
        return True
    else:
        return False
    

def rotatePolygon(resultLine, polygon, showRotation=False):
    """"
    Rotates the polygon until it is parallel to the line.
    
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

def moveToOrigin(polygon):
    """
    Moves the polygon until two of its vertices touch the axis lines.
    
    Returns the moved polygon.
    """

    X,Y = 0,1
    leftmost = polygon.exterior.coords[0][X]
    bottom = polygon.exterior.coords[0][Y]
    for coord in polygon.exterior.coords[1:-1]:
        if coord[X] < leftmost : leftmost=coord[X]
        if coord[Y] < bottom : bottom=coord[Y]
    
    shiftcoords = [(coord[X]-leftmost, coord[Y]-bottom) for coord in polygon.exterior.coords[:-1]]
    return Polygon(shiftcoords)


def initialisePlotting(unitPolygon):
    """Places a unitPolygon parallel to the longest edge of the rlp."""

    def showRotation(longestline, unitPolygon):
        visibleLine = [(x-534300, y-182500) for (x,y) in longestline]
        rotatePolygon(LineString(visibleLine), unitPolygon, showRotation=True)

    
    longestline = findLongestLine(rlppolygon)
    rotatedUP = rotatePolygon(LineString(longestline), unitPolygon, showRotation=False)
    rotatedUP = moveToOrigin(rotatedUP)





    
    # select direction parallel to side while making housecoords
    # make house Polygon
    
    firstcoord = oldrlpcoords[2]
    xpadding, ypadding = 5, 5
    X, Y = 0, 1
    
    housecoords = [(up[X]+firstcoord[X]+xpadding, up[Y]+firstcoord[Y]+ypadding) for up in unitPolygon.exterior.coords]
    house =  Polygon(housecoords)

    # print(oldrlpcoords)
    # print(housecoords)

    ax = rlp.plot(facecolor="grey")
    gs = geopandas.GeoSeries(house)
    gs.plot(ax=ax, facecolor="red")
    gs.plot(facecolor="red")

    # plt.show()
    

def plotProportions(housetypes, unitPolygons, proportions):
    """
    Plots all housetypes on the rlp.
    
    The number of houses of each ht depends on its proportion in proportions.
    
    Unit polygons are copied and moved around the rlp to create new houses.
    """

    emptyrlp = True
    for htindex in range(len(housetypes)):
        ht = housetypes[htindex]
        freq = proportions[htindex]
        unitPolygon = unitPolygons[htindex]

        for housecount in range(freq):
            if emptyrlp:
                initialisePlotting(unitPolygon)
                emptyrlp = False
            else:
                pass





mht = ManageHouseTypes()
fillMHT(mht)
housetypes = mht.getHouseTypes()

unitPolygons = makeUnitPolygons(housetypes)

(proportions, profit) = generateBestTypes(mht.getHouseTypes(), maxsize=rlppolygon.area, showResults=False)
plotProportions(housetypes, unitPolygons, proportions)