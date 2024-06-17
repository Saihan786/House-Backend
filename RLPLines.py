import matplotlib.pyplot as plt
import numpy as np
import geopandas
from AddDataToDF import coords
from RedLinePlot import getRLP, getPath
from shapely import Polygon

oldcoords = coords()

def findLineFromTuples(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    if not (x2-x1)==0:
        m = (y2-y1) / (x2-x1)
        c = y1-(m*x1)
    else:
        # add edge case for x2-x1==0
        # for now, causes error as m and c haven't been initialised so cannot be returned
        pass    
    return (m, c)



rlp = getRLP(getPath())
rlp = rlp.to_crs(epsg=27700)
rlp["name"] = ["rlp"]
rlppolygon = rlp.geometry[0]

oblong = Polygon( [(510000,180000), (510100,185100), (510150, 185050), (510000,185000)] )

ax = rlp.plot(facecolor="grey")
geopandas.GeoSeries(oblong).plot(ax=ax, facecolor="red")

print(oblong.within(rlppolygon))




# for plotting purposes only - cannot check if a point or polygon is within a ring
rlpRing = rlp.exterior





plt.show()