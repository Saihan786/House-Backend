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
import ShapeFunctions


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
        ShapeFunctions.rotatePolygon(LineString(visibleLine), unitPolygon, showRotation=True)


    # rotate unit polygon
    
    longestline = ShapeFunctions.findLongestLine(rlppolygon)
    longestline = ShapeFunctions.orderLine(longestline)

    
    rotatedUP = ShapeFunctions.rotatePolygon(LineString(longestline), unitPolygon)
    rotatedUP = ShapeFunctions.moveToOrigin(rotatedUP, showTranslation=False)


    # find normal lines and set initial house padded from longestline and adjacent line with GIVEN padding to place houses in new row
    #       (so this method should only plot initial houses at each row of GIVEN padding using perpendicular lines)




def plotRow():
    """Plots a whole row, given the parallel eq for the longest line AND the initial house coordinates for this row.
    
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


    longestline, adjacentline, corner = ShapeFunctions.lines(rlppolygon)
    lleq, aleq = ShapeFunctions.leqs(longestline), ShapeFunctions.leqs(adjacentline)



    
    llpaddedpoint = (corner[0], ShapeFunctions.lineyval(lleq, (corner[0])))
    alpaddedpoint = (corner[0], ShapeFunctions.lineyval(aleq, (corner[0])))
    
    nlleq = ShapeFunctions.normalLineEQ(lleq, llpaddedpoint)

    
    newRow = True
    for htindex in range(len(housetypes)):
        ht = housetypes[htindex]
        freq = proportions[htindex]
        unitPolygon = unitPolygons[htindex]

        geopandas.GeoSeries(rlppolygon.exterior).plot(ax=ax, color="blue")

        for housecount in range(freq):
            if newRow:
                # use perpendicular line to begin house placement on a new row
                # (llpadding and?) naleq should change for every new row
                # 
                initNewRow(unitPolygon)
                newRow = False

                if rlppolygon.contains(Point(alpaddedpoint)):
                    print(alpaddedpoint[X])
                    geopandas.GeoSeries( Point(alpaddedpoint) ).plot(ax=ax, color="red")

                alpaddedpoint = (alpaddedpoint[X]-alpadding, ShapeFunctions.lineyval(aleq, (alpaddedpoint[X]-alpadding)))

            else:
                # use parallel line (parallel to longestline) to continue house placement from initial house
                # housepadding should never change
                # llpaddedpoint = (llpaddedpoint[X]-5, ShapeFunctions.lineyval(lleq, (llpaddedpoint[X]-5))) # to be moved to plotRow()
                # while rlppolygon.contains(Point(llpaddedpoint)):
                for i in range(1):
                    plotRow()

                    nlleq = ShapeFunctions.normalLineEQ(lleq, llpaddedpoint)
                    nlline = ShapeFunctions.leqtoline(nlleq, rlppolygon)
                    
                    if rlppolygon.contains(Point(llpaddedpoint)):
                        geopandas.GeoSeries( Point(llpaddedpoint) ).plot(ax=ax, color="red")
                        geopandas.GeoSeries( nlline ).plot(ax=ax, color="green")
                        # pass

                    llpaddedpoint = (llpaddedpoint[X]+llpadding, ShapeFunctions.lineyval(lleq, (llpaddedpoint[X]+llpadding))) # to be moved to plotRow()
                newRow = True
            
    # plt.show()




mht = ManageHouseTypes()
fillMHT(mht)
housetypes = mht.getHouseTypes()

unitPolygons = makeUnitPolygons(housetypes)

(proportions, profit) = generateBestTypes(mht.getHouseTypes(), maxsize=rlppolygon.area, showResults=False)
plotProportions(housetypes, unitPolygons, proportions)




# ISSUES:
#       fix the +- when calculating padded points, rlp doesn't know which direction to go sometimes
#       sometimes points aren't detected with rlp.contains(Point)
