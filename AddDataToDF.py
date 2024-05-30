from RedLinePlot import getRLP
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LinearRing
import geopandas

# get the rlp (geodataframe containing geometry column which is just a dictionary with a mapping to the Polygon)
path_to_rlp = "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/data.geojson"
rlp = getRLP(path_to_rlp)

# for accurate measurements in metres
rlp = rlp.to_crs(epsg=27700)




# grab coordinates which are rlp boundaries

rlp.plot()
polygon_metres = rlp.geometry[0]
oldcoords = polygon_metres.exterior.coords[:-1]
print(oldcoords)

newcoords = oldcoords
newcoords.append((525000,194470))
linearRing1 = LinearRing(newcoords)
rlp["newgeo"] = linearRing1
rlp = rlp.set_geometry("newgeo")
rlp.plot()
print(newcoords)

plt.show()
# newcoords = [(0,5),(1,1),(3,0)]
# print(rlp)










# after determining new points to add to polygon, this must recreate a new Polygon object and set this object as the rlp geometry
#   and then change it to the correct EPSG







plt.show()