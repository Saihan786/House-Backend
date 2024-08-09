"""This file converts user-inputted blocks representing houses and their gardens and parking to unitPolygons used in PlotOptimals.py"""

import geopandas
import matplotlib.pyplot as plt
from shapely.ops import unary_union

try:
    from ..software import PolygonFunctions
except ImportError:
    import PolygonFunctions


dxfblock = None
gardens = None
parking = None
house = None


def set_up_colors(dxfblock):
    """Adds a colors column to dxfblock which can be passed to the plot() method.
    
    This must be adjusted if the name of the expected layers change.
    
    """

    colors = []

    for l in dxfblock['Layer']:
        match l:
            case 'GARDEN':
                colors.append("green")
            case 'HOUSE NEW':
                colors.append("blue")
            case 'PARKING':
                colors.append("grey")
    
    if len(colors)<3:
        print("error with setting up colors for the dxfblock.")
    
    dxfblock['colors']= colors


def readDXF():
    """Reads dxf file to get the user-drawn block and cleans the data.
    
    Returns (dxfblock, gardens, parking, house)
    
    """


    dxfblock = geopandas.read_file("C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/House_plotting_example.dxf")
    dxfblock['geom_type']= dxfblock.geometry.type
    dxfblock = dxfblock.loc[dxfblock.geom_type == 'Polygon']
    set_up_colors(dxfblock=dxfblock)

    gardens = dxfblock.loc[dxfblock.Layer == 'GARDEN'].geometry
    parking = dxfblock.loc[dxfblock.Layer == 'PARKING'].geometry
    house = dxfblock.loc[dxfblock.Layer == 'HOUSE NEW'].geometry

    if gardens.size==1 and parking.size==1:
        flex_regions = [gardens, parking]
        flex_polygon = geopandas.GeoSeries(unary_union(flex_regions))

    return (dxfblock, gardens, parking, house)
(dxfblock, gardens, parking, house) = readDXF()


def dxf_parallel_to_ll(longestline=None):
    """Rotates the whole dxf so the house is parallel to the given longest line.
    
    Returns the updated dxf.

    *****THIS ASSUMES THE DXF IS AT THE ORIGIN*****
    
    """

    pass
dxf_parallel_to_ll()


def get_dxf_as_gdf():
    """Returns the combination of the garden, parking, and house as a GeoDataFrame.
    
    Returns none if no dxf file is available.
    
    """

    return dxfblock


def get_dxf_separate():
    """Returns each part of the DXF polygon separately"""

    return gardens, parking, house


def plotDXF(dxfblock, ax=None):
    """Plots the gardens, parking, and house from a single GeoDataFrame.
    
    Gardens, house, and parking may be plotted on separate axes if an axes is not
    provided AND no 'colors' column is present.
    
    """

    if 'colors' in dxfblock.columns:
        dxfblock.plot(ax=ax, color=dxfblock['colors'])
    else:
        geopandas.GeoSeries(gardens).plot(ax=ax, color="green")
        geopandas.GeoSeries(house).plot(ax=ax, color="blue")
        geopandas.GeoSeries(parking).plot(ax=ax, color="grey")



# from shapely import LineString
# def getOne(polygon): return LineString([ (0,0), (1,1) ])
# dxfblock.geometry = dxfblock.geometry.apply(getOne)
# print( dxfblock )

plotDXF(dxfblock=dxfblock)
plt.show()