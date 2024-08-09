"""This file converts user-inputted blocks representing houses and their gardens and parking to unitPolygons used in PlotOptimals.py"""

import geopandas
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely import LineString, Polygon

try:
    from ..software import LineFunctions
except ImportError:
    import LineFunctions


dxfblock = None
gardens = None
parking = None
house = None

X,Y = 0,1


def centerDXFAtOrigin(dxf):
    """Moves the dxf until the origin is the mean of all of its points.

    Exists the option to show the translation, which is only effective if the distance translated is not too large.
    
    This assumes that the garden
    
    *****ONLY WORKS FOR GDFs*****
    
    """

    center = unary_union(dxf.geometry).centroid
    def move(polygon):
        shiftcoords = [(coord[X]-center.x, coord[Y]-center.y) for coord in polygon.exterior.coords[:-1]]
        return Polygon(shiftcoords)
    dxf.geometry = dxf.geometry.apply(move)


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
    centerDXFAtOrigin(dxf=dxfblock)

    gardens = dxfblock.loc[dxfblock.Layer == 'GARDEN'].geometry
    parking = dxfblock.loc[dxfblock.Layer == 'PARKING'].geometry
    house = dxfblock.loc[dxfblock.Layer == 'HOUSE NEW'].geometry

    if gardens.size==1 and parking.size==1:
        flex_regions = [gardens, parking]
        flex_polygon = geopandas.GeoSeries(unary_union(flex_regions))

    return (dxfblock, gardens, parking, house)
(dxfblock, gardens, parking, house) = readDXF()


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


def dxf_parallel_to_ll(dxf, origin=True, point_about_rotation=None, longestline=None):
    """Rotates the gdf until the house is parallel to the resultLine.

    The rotation is about the given point or the origin if it is not given.
    
    Returns the updated dxf.

    Normally moves the dxf to the origin after the operation.

    *****THIS ASSUMES THE DXF IS AT THE ORIGIN*****
    
    """

    if point_about_rotation is None:
        point_about_rotation=(0,0)

    house = dxf.loc[dxf.Layer == 'HOUSE NEW'].geometry
    if len(house) == 1:
        for actual_polygon in house:
            house = actual_polygon
    else:
        print("error when making dxf parallel to ll")

    polygonLine = LineString([house.exterior.coords[0], house.exterior.coords[1]])
    resultAngle, changeAngle = LineFunctions.findAngle(longestline), LineFunctions.findAngle(polygonLine)

    dxf.geometry = dxf.rotate(resultAngle-changeAngle, point_about_rotation, use_radians=True)

    if origin:
        centerDXFAtOrigin(dxf=dxf)


def rotateNinety(dxf, origin=True, point_about_rotation=None):
    """Rotates the given dxf 90 degrees.
    
    To be used after the dxf is parallel to the longest line, to make sure
    it is facing the road.

    Normally moves the dxf to the origin after the operation.
    
    """

    if point_about_rotation is None:
            point_about_rotation=(0,0)

    dxf.geometry = dxf.rotate(90, point_about_rotation, use_radians=False)

    if origin:
        centerDXFAtOrigin(dxf=dxf)
    

def get_dxf_as_gdf():
    """Returns the combination of the garden, parking, and house as a GeoDataFrame.
    
    Returns none if no dxf file is available.
    
    """

    return dxfblock


def get_dxf_separate():
    """Returns each part of the DXF polygon separately"""

    return gardens, parking, house