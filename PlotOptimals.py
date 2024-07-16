# don't consider budget or road costs
# might be easier to work with one housetype for now

import geopandas.geoseries
from HRGenerator import ManageHouseTypes, generateBestTypes
import matplotlib.pyplot as plt
from RedLinePlot import getRLP, getPath
from shapely import Polygon, LineString, affinity, Point, intersection
from AddDataToDF import coords
import geopandas
import numpy as np
import PolygonFunctions
import LineFunctions    


NAME, REVENUE, COST, WIDTH, LENGTH, SIZE = 0, 1, 2, 3, 4, 5
X, Y = 0, 1

rlp = getRLP(getPath())
rlp = rlp.to_crs(epsg=27700)
rlp["name"] = ["rlp"]
rlppolygon = rlp.geometry[0]
oldrlpcoords = coords()

def fillMHT(mht):
    mht.addNewHouseType("ht1", 100000, 0, 25, 30)
    mht.addNewHouseType("ht2", 150000, 0, 50, 50)


def makeUnitPolygons(housetypes):
    """Returns a list of unit polygons for each housetype
    
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


def initNewRow(unitPolygon, lleq=None, padding=5):
    """Places a unitPolygon parallel to the longest edge of the rlp.
    
    The unit polygon is rotated to be aligned with the longest edge and padded from the longest and adjacent lines
    to start a new row.

    This method receives the two normal line equations and padding and uses these to place the new initial house.
    
    """

    linep1, linep2 = 0, 1

    def showRotation(longestline, unitPolygon):
        visibleLine = [(x-534300, y-182500) for (x,y) in longestline]
        PolygonFunctions.rotatePolygon(LineString(visibleLine), unitPolygon, showRotation=True)


    # rotate unit polygon
    
    longestline = PolygonFunctions.findLongestLine(rlppolygon)
    longestline = LineFunctions.orderLine(longestline)

    
    rotatedUP = PolygonFunctions.rotatePolygon(LineString(longestline), unitPolygon)
    rotatedUP = PolygonFunctions.moveToOrigin(rotatedUP, showTranslation=False)


    # find normal lines and set initial house padded from longestline and adjacent line with GIVEN padding to place houses in new row
    #       (so this method should only plot initial houses at each row of GIVEN padding using perpendicular lines)




def plotRow():
    """ Continues to plot this row, using the correct unitPolygon.
    
    Plots a whole row, given the parallel eq for the longest line AND the initial house coordinates for this row.
    
    An initialised row has an initial house padded correctly, so this method doesn't need to worry about perpendicular padding. All this
    function does is pads new houses from the previous (starting at initial) house parallel to the longest line.
    
    If obstacles are present, the best solution may be to plot from two adjacent lines and see when currCoords overlap to see if
    an obstacle is reached or if the end of the rlp is reached.
    
    """

    pass
    

def plotProportions(housetypes, unitPolygons, proportions):
    """Plots all housetypes on the rlp.
    
    The number of houses of each ht depends on its proportion in proportions.
    
    Unit polygons are copied and moved around the rlp to create new houses.
    
    """

    fig, ax = plt.subplots()
    linep1idx, linep2idx = 0, 1
    llpadding, alpadding = 5, 5

    # change to be housepadding and rowpadding afterwards
    # also the values here should start out as width and height of the unitpolygon plus a bit
    xpadding, ypadding = 30, 50


    longestline = PolygonFunctions.findLongestLine(rlppolygon)

    (linePathX, mX, isPerp), (linePathY, mY) = PolygonFunctions.findLinePaths(rlppolygon, showPaths=False)


    geopandas.GeoSeries(rlppolygon.exterior).plot(ax=ax, color="blue")
    xlines = []
    for xline in linePathX:
        xleq = LineFunctions.lineEQ(xline[linep1idx], xline[linep2idx])
        p1 = xline[linep1idx]
        p2 = xline[linep2idx]

        x = p1[X]
        while x<p2[X]:
            y = LineFunctions.lineyval(xleq, x)
            
            point = (x,y)
            c = LineFunctions.linecval(mX, point)
            leq = (mX, c, False)
            line = LineFunctions.leqtoline(leq, rlppolygon)
            xlines.append(line)
            # geopandas.GeoSeries( line ).plot(ax=ax, color="red")
            
            x+=xpadding
            
    housepoints = []
    for yline in linePathY:
        yleq = LineFunctions.lineEQ(yline[linep1idx], yline[linep2idx])
        p1 = yline[linep1idx]
        p2 = yline[linep2idx]

        y = p1[Y]
        while y>p2[Y]:
            x = LineFunctions.linexval(yleq, y)
            
            point = (x,y)
            c = LineFunctions.linecval(mY, point)
            leq = (mY, c, False)
            line = LineFunctions.leqtoline(leq, rlppolygon)
            
            # geopandas.GeoSeries( line ).plot(ax=ax, color="green")

            for xl in xlines:
                housepoint = intersection(line, xl)
                if not housepoint.is_empty:
                    housepoints.append(housepoint)
                    # geopandas.GeoSeries( housepoint ).plot(ax=ax, color="green")
            
            y-=ypadding
    

    
    houses = []
    rotatedUP = PolygonFunctions.rotatePolygon(LineString(longestline), unitPolygons[0])
    rotatedUP = PolygonFunctions.moveToOrigin(rotatedUP, showTranslation=False)

    for housepoint in housepoints:
        corners = []
        for corner in rotatedUP.exterior.coords[:-1]:
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

    print(len(distincthouses))
    geopandas.GeoSeries([house.exterior for house in distincthouses]).plot(ax=ax, color="green")
    plt.show()


    # newRow = True
    # for htindex in range(len(housetypes)):
    #     geopandas.GeoSeries(rlppolygon.exterior).plot(ax=ax, color="blue")

    #     ht = housetypes[htindex]
    #     freq = proportions[htindex]
    #     unitPolygon = unitPolygons[htindex]



    #     for housecount in range(freq):
    #         if newRow:
    #             newRow = False

    #         else:
    #             newRow = True
        
    #     break




mht = ManageHouseTypes()
fillMHT(mht)
housetypes = mht.getHouseTypes()

unitPolygons = makeUnitPolygons(housetypes)

(proportions, profit) = generateBestTypes(mht.getHouseTypes(), maxsize=rlppolygon.area, showResults=False)
plotProportions(housetypes, unitPolygons, proportions)




# ISSUES:
#       fix the +- when calculating padded points, rlp doesn't know which direction to go sometimes
#       sometimes points aren't detected with rlp.contains(Point)
