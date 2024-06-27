import matplotlib.pyplot as plt
import numpy as np
import geopandas
from RedLinePlot import getRLP, getPath
from shapely import Polygon

rlp = getRLP(getPath())
rlp = rlp.to_crs(epsg=27700)
rlp["name"] = ["rlp"]
rlppolygon = rlp.geometry[0]

oblong = Polygon( [(524989,194467), (524995,194467), (524989,194430), (524989,194467)] )

ax = rlp.plot(facecolor="grey")
geopandas.GeoSeries(oblong).plot(ax=ax, facecolor="red")

# print(oblong.within(rlppolygon))
# print(rlppolygon.contains(oblong))







# for plotting purposes only - cannot check if a point or polygon is within a ring
rlpRing = rlp.exterior


plt.show()