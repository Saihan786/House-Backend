from RedLinePlot import getRLP
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, mapping

# get the rlp (geodataframe containing geometry column which is just a dictionary with a mapping to the Polygon)
path_to_rlp = "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/data.geojson"
rlp = getRLP(path_to_rlp)

# for accurate measurements in metres
rlp = rlp.to_crs(epsg=27700)


# grab coordinates which are rlp boundaries
polygon_metres = rlp.geometry[0]
coords = polygon_metres.exterior.coords[:-1]
coords.append((1,1))
for x,y in coords:
    print(x,y)





coords = [(1,1), (2,2), (3,3), (4,4)]
newpoly = Polygon(coords)


rlp["newgeo"] = newpoly
print(rlp)
rlp.set_geometry("newgeo")


rlp.plot(column="newgeo")









# after determining new points to add to polygon, this must recreate a new Polygon object and set this object as the rlp geometry
#   and then change it to the correct EPSG







plt.show()