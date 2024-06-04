from RedLinePlot import getRLP
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LinearRing
import geopandas


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
rlpboundarycoords.append((525000,194470))


# make new geoseries containing linearring (for rlpboundary) and points as separate entries
# (maybe eventually put into gdf, I don't see the benefit of this now besides showing the rlp in context, possibly could label the shapes like boundary, house1, road1, etc.)
rlpboundary = LinearRing(rlpboundarycoords)
house1 = Polygon([(524924.2,194488.9), (524924.2, 194500), (524940.2, 194500), (524940.2, 194488.9), (524924.2,194488.9)])
rlp_with_house = geopandas.GeoSeries([rlpboundary, house1])


# @return old coords
def coords():
    return oldcoords

# @return old rlp as a LinearRing
def rlpAsRing():
    return LinearRing(oldcoords)





# after determining new points to add to polygon, this must recreate a new Polygon object and set this object as the rlp geometry
#   and then change it to the correct EPSG