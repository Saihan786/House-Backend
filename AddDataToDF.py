from RedLinePlot import getRLP
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LinearRing
import geopandas



# @param coord1 and coord2 are both tuples of x and y coordinate values
# @return coordinate that is:
#       halfway between the two coords with a slightly smaller y value
#       fraction of the distance away from the line between coord1 and coord2
# returned coord does not always form a proper polygon with the rest of the coordinates (may reach past a different line of polygon)
def createExternalCoord(coord1, coord2):
    x1,y1 = coord1
    x2,y2 = coord2
    xdifference, ydifference = abs(x2-x1), abs(y2-y1)

    x = 0.5*(x1+x2) - 0.2*(xdifference)
    y = 0.5*(y1+y2) - 0.2*(ydifference)

    return (x,y)



# get the rlp (geodataframe containing geometry column which is just a dictionary with a mapping to the Polygon)
path_to_rlp = "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/data.geojson"
rlp = getRLP(path_to_rlp)
rlp = rlp.rename_geometry("old shaded rlp")



# for accurate measurements in metres
rlp = rlp.to_crs(epsg=27700)



# grab coordinates which are rlp boundaries, and append new coordinate
polygon_metres = rlp.geometry[0]
oldcoords = polygon_metres.exterior.coords[:-1]
rlpboundarycoords = oldcoords.copy()
rlpboundarycoords.append(createExternalCoord(rlpboundarycoords[0], rlpboundarycoords[-1]))


# make new geoseries containing linearring (for rlpboundary) and points as separate entries
# (maybe eventually put into gdf, I don't see the benefit of this now besides showing the rlp in context, possibly could label the shapes like boundary, house1, road1, etc.)
rlpboundary = LinearRing(rlpboundarycoords)
house1 = Polygon([(524924.2,194488.9), (524924.2, 194500), (524940.2, 194500), (524940.2, 194488.9), (524924.2,194488.9)])
rlp_with_house = geopandas.GeoSeries([rlpboundary])


squarecoords = [(5,5), (11,10), (12,8), (6,0)]
square = LinearRing(squarecoords)
# geopandas.GeoSeries(square).plot()



# after determining new points to add to polygon, this must recreate a new Polygon object and set this object as the rlp geometry
#   and then change it to the correct EPSG

# @return old coords
def coords():
    # return squarecoords
    return oldcoords

# @return old rlp as a LinearRing
def rlpAsRing():
    return LinearRing(oldcoords)

# rlp.plot()
# rlp_with_house.plot()
plt.show()