# don't consider budget or road costs
# might be easier to work with one housetype for now

from HRGenerator import ManageHouseTypes, generateBestTypes
import matplotlib.pyplot as plt
import numpy as np
import geopandas
from RedLinePlot import getRLP, getPath
from shapely import Polygon

# rlp = getRLP(getPath())
# rlp = rlp.to_crs(epsg=27700)
# rlp["name"] = ["rlp"]
# rlppolygon = rlp.geometry[0]

NAME, REVENUE, COST, WIDTH, LENGTH, SIZE = 0, 1, 2, 3, 4, 5

def fillMHT(mht):
    mht.addNewHouseType("ht1", 100000, 0, 5, 16)
    mht.addNewHouseType("ht2", 150000, 0, 5, 17)
    mht.addNewHouseType("ht3", 175000, 0, 5, 18)
    mht.addNewHouseType("ht4", 200000, 0, 97, 1)
    mht.addNewHouseType("ht5", 215000, 0, 1, 101)


mht = ManageHouseTypes()
fillMHT(mht)
housetypes = mht.getHouseTypes()


# in order of housetypes
# make unit polygons for each housetype (even the ones that have frequency zero, because we may need to change the proportions of polygons)
# unit polygons can be adjusted around the rlp by adding to its x and y values by a set amount
def makeUnitPolygons():
    unitPolygons = []
    for ht in housetypes:
        # (name, revenue, cost, width, length, size)
        point1 = (0,0)
        point2 = (0+ht[WIDTH],0)
        point3 = (0,0+ht[LENGTH])
        point4 = (0+ht[WIDTH],0+ht[LENGTH])
        print(point1)
        print(point2)
        print(point3)
        print(point4)
        print()
        unitPolygons.append(Polygon([point1, point2, point4, point3, point1]))
        
    # geopandas.GeoSeries(unitPolygons).plot()
    for polygon in unitPolygons:
        plt.plot(*polygon.exterior.xy)
    plt.show()

    return unitPolygons

unitPolygons = makeUnitPolygons()










# sort out 
# names = []
# for housetype in housetypes:
#     names.append(housetype[NAME])

# (proportions, profit) = generateBestTypes(mht.getHouseTypes())

