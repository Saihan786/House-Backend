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


# in order of housetypes
# make unit polygons for each housetype (even the ones that have frequency zero, because we may need to change the proportions of polygons)
# unit polygons can be adjusted around the rlp by adding to its x and y values by a set amount
def makeUnitPolygons(housetypes):
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



def isParallel(line, changeline):
    xs1, xe1 = line.xy[0]
    ys1, ye1 = line.xy[1]
    xs2, xe2 = changeline.xy[0]
    ys2, ye2 = changeline.xy[1]

    if xs1 == xe1:
        angle1 = np.pi/2
    else:
        angle1 = np.arctan((ye1-ys1)/(xe1-xs1))
    if xs2 == xe2:
        angle2 = np.pi/2
    else:
        angle2 = np.arctan((ye2-ys2)/(xe2-xs2))
    return True if round(angle1, 3) == round(angle2, 3) else False

def makeParallel(line, changeline, unitPolygon):
    def findAngle(l):
        xs1, xe1 = l.xy[0]
        ys1, ye1 = l.xy[1]
        if xs1 == xe1:
            angle = np.pi/2
        else:
            angle = np.arctan((ye1-ys1)/(xe1-xs1))
        return angle
    angle, changle = findAngle(line), findAngle(changeline)


    ax = geopandas.GeoSeries(line).plot()
    # print(line)
    # print(changeline)
    # print(angle-changle)
    geopandas.GeoSeries(unitPolygon).plot(ax=ax, color="red")
    unitPolygon = affinity.rotate(unitPolygon, angle-changle, origin="centroid", use_radians=True)
    upline = LineString([unitPolygon.exterior.coords[0], unitPolygon.exterior.coords[1]])
    geopandas.GeoSeries(unitPolygon).plot(ax=ax, color="green")
    plt.show()   
    
    print(changle, findAngle(upline), findAngle(line))
    print("The angle we need:", angle)
    print(isParallel(upline, line))


    return True if angle == changle else False


def initialisePlotting(unitPolygon):
    # select longest side
    b = rlppolygon.boundary.coords
    lines = [LineString(b[point:point+2]) for point in range(len(b)-1)]

    length = 0
    longestlineindex = 0
    for i in range(len(lines)):
        if lines[i].length>length:
            length=lines[i].length
            longestlineindex = i
    longestline = lines[longestlineindex].coords

    
    # reorientate unit polygon to be parallel to line
    upline = LineString([unitPolygon.exterior.coords[0], unitPolygon.exterior.coords[1]])
    # ax = geopandas.GeoSeries(upline).plot(color="red")
    # geopandas.GeoSeries(upline.centroid).plot(ax=ax, color="blue")
    
    longestline = [(x-534300, y-182500) for (x,y) in longestline]
    print(longestline)
    makeParallel(LineString(longestline), upline, unitPolygon)


    
    
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
    emptyrlp = True
    for htindex in range(len(housetypes)):
        ht = housetypes[htindex]
        freq = proportions[htindex]
        currUP = unitPolygons[htindex]

        for housecount in range(freq):
            if emptyrlp:
                initialisePlotting(currUP)
                emptyrlp = False
            else:
                pass





mht = ManageHouseTypes()
fillMHT(mht)
housetypes = mht.getHouseTypes()

unitPolygons = makeUnitPolygons(housetypes)

(proportions, profit) = generateBestTypes(mht.getHouseTypes(), maxsize=rlppolygon.area, showResults=False)
plotProportions(housetypes, unitPolygons, proportions)