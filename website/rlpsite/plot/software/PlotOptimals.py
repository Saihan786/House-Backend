# don't consider budget or road costs
# might be easier to work with one housetype for now

import geopandas.geoseries
from HRGenerator import ManageHouseTypes, generateBestTypes, generateBasicTypes
import matplotlib.pyplot as plt
from RedLinePlot import getRLP, getPath
from shapely import Polygon, LineString, affinity, Point, intersection
import geopandas
import numpy as np
import PolygonFunctions as PolygonFunctions
import LineFunctions as LineFunctions    


X, Y = 0, 1
linep1idx, linep2idx = 0, 1

rlp = getRLP(getPath())
rlp = rlp.to_crs(epsg=27700)
rlp["name"] = ["rlp"]
rlppolygon = rlp.geometry[0]

def fillMHT(mht):
    mht.addNewHouseType("ht1", 100000, 0, 25, 30)
    mht.addNewHouseType("ht2", 150000, 0, 50, 50)


def makeUnitPolygons(housetypes):
    """Returns a list of unit polygons for each housetype
    
    Unit polygons can be adjusted around the rlp by adding to its x and y values.

    """

    unitPolygons = []
    for ht in housetypes:
        point1 = (0,0)
        point2 = (0+ht.WIDTH,0)
        point3 = (0,0+ht.LENGTH)
        point4 = (0+ht.WIDTH,0+ht.LENGTH)
        unitPolygons.append(Polygon([point1, point2, point4, point3, point1]))

    return unitPolygons


def findPadding(unitPolygons, longestline):
    """Returns housepadding and rowpadding.
    
    Housepadding is the largest parallel length of all unit polygons with a bit added.
    Rowpadding is the largest perpendicular length of all unit polygons with a bit added.

    Padding is calculated iteratively.
    
    """

    def calculateDistance(leq, padding=0, increment=10, showDistance=False):
        """Returns the (slightly increased) distance across the largest polygon, with respect to the
        given line equation.
        
        """
        
        originalx = 0
        originaly = LineFunctions.lineyval(leq, originalx)

        allups = []

        for up in unitPolygons:
            up1 = up2 = Polygon( [(c[X]+originalx,c[Y]+originaly) for c in list(up.exterior.coords)] )

            x=0
            while up1.intersects(up2):
                x += increment
                y = LineFunctions.lineyval(leq, x)
                up2 = Polygon( [(c[X]+x,c[Y]+y) for c in list(up.exterior.coords)] )
            
            distance = np.sqrt(np.square(x-originalx) + np.square(y-originaly))
            if padding<distance : padding = distance

            allups.append(up1)
            allups.append(up2)
        
        if showDistance:
            geopandas.GeoSeries([up.exterior for up in allups]).plot()
            plt.show()

        return padding

    leq = LineFunctions.lineEQ(longestline[linep1idx], longestline[linep2idx])
    housepadding = calculateDistance(leq, showDistance=False)

    nleq = LineFunctions.normalLineEQ(leq, longestline[linep1idx])
    rowpadding = calculateDistance(nleq, showDistance=False)

    return (housepadding, rowpadding)


def houselines(path, distance, pathIsHorizontal, ax=None, longestline=None):
    """Returns a list of all new lines, each from a point on the lines of the given path.

    The points are equidistant from each other at a given distance.
    
    The new lines have the given gradient m.
    
    """

    lines = []
    p1 = path[0][linep1idx]

    lleq = LineFunctions.lineEQ(longestline[linep1idx], longestline[linep2idx])
    nleq = LineFunctions.normalLineEQ(lleq, p1)

    if pathIsHorizontal:
        x = p1[X]

        points = []
        while x < path[ -1+len(path) ][linep2idx][X]:
            y = LineFunctions.lineyval(lleq, x)
            points.append( (x,y) )
            point = (x,y)
            
            nleq = LineFunctions.normalLineEQ(lleq, point)
            newline = LineFunctions.leqtoline(nleq, rlppolygon)
            lines.append(newline)
            
            x+=distance

    else:
        y = p1[Y]

        points = []
        while y > path[ -1+len(path) ][linep2idx][Y]:
            x = LineFunctions.linexval(nleq, y)
            points.append( (x,y) )
            point = (x,y)

            lleq = LineFunctions.normalLineEQ(nleq, point)
            newline = LineFunctions.leqtoline(lleq, rlppolygon)
            lines.append(newline)

            y-=distance

    return lines


def plotHouses(housepoints, unitPolygon, ax):
    """Plots houses using housepoints as locations for houses.

    need to change because only uses one unitpolygon for now
    
    """

    houses = []

    for housepoint in housepoints:
        corners = []
        for corner in unitPolygon.exterior.coords[:-1]:
            corners.append( (corner[X]+housepoint.coords[0][X] , corner[Y]+housepoint.coords[0][Y]) )
        houses.append(Polygon(corners))
    
    houses = [house for house in houses if rlppolygon.contains(house)]

    distincthouses = []
    for i in range(-1+len(houses)):
        keepHouse = True
        for j in range(i+1, len(houses)):
            if houses[i].intersects(houses[j]):
                keepHouse = False
        if keepHouse:
            distincthouses.append(houses[i])

    print("number of houses on plot:", len(distincthouses))
    geopandas.GeoSeries([house.exterior for house in distincthouses]).plot(ax=ax, color="green")
    

def plotProportions(housetypes, unitPolygons, proportions):
    """Plots all housetypes on the rlp.
    
    The number of houses of each ht depends on its proportion in proportions.
    
    Unit polygons are copied and moved around the rlp to create new houses.

    Housepadding is for perp lines, while Rowpadding is for parallel lines.
    
    """

    longestline = PolygonFunctions.findLongestLine(rlppolygon)

    unitPolygons = [PolygonFunctions.rotatePolygon(LineString(longestline), uP, showRotation=False) for uP in unitPolygons]
    unitPolygons = [PolygonFunctions.moveToOrigin(uP, showTranslation=False) for uP in unitPolygons]

    horizontal_has_longest, (linePathX, mX), (linePathY, mY) = PolygonFunctions.findLinePaths(rlppolygon, showPaths=False)

    housepadding, rowpadding = findPadding(unitPolygons, longestline)
    housepadding, rowpadding = 30, 50

    fig, ax = plt.subplots()
    geopandas.GeoSeries(rlppolygon.exterior).plot(ax=ax, color="blue")

    if horizontal_has_longest:
        perpLines = houselines(linePathX, housepadding, pathIsHorizontal=True, ax=ax, longestline=longestline)
        parallelLines = houselines(linePathY, rowpadding, pathIsHorizontal=False, ax=ax, longestline=longestline)            
    else:
        perpLines = houselines(linePathX, rowpadding, pathIsHorizontal=True, ax=ax)
        parallelLines = houselines(linePathY, housepadding, pathIsHorizontal=False, ax=ax, longestline=longestline)            
    
    housepoints = []
    for l1 in perpLines:
        for l2 in parallelLines:
            housepoint = intersection(l1, l2)
            if not housepoint.is_empty:
                housepoints.append(housepoint)

    plotHouses(housepoints, unitPolygons[0], ax=ax)
    plt.show()


mht = ManageHouseTypes()
fillMHT(mht)
housetypes = mht.getHouseTypes()

unitPolygons = makeUnitPolygons(housetypes)

basicproportions = generateBasicTypes(mht.getHouseTypes(), maxsize=rlppolygon.area, showResults=False)
mht.addProportions(basicproportions)
plotProportions(housetypes, unitPolygons, basicproportions)