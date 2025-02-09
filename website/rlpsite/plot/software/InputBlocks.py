"""
This file converts user-inputted blocks representing houses and their gardens and parking to unitPolygons used in PlotOptimals.py

func:
- centerDXFAtOrigin
- set_up_colors
- readDXF
- plotDXF
- dxf_parallel_to_ll
- rotateNinety
- calc_front
- rotateNinety
- update_dxf_front
- get_dxf_as_gdf
- get_dxf_separate
"""

import geopandas
import shapely
from shapely.ops import unary_union

try:
    from ..software import LineFunctions
except ImportError:
    print("ignore previous import errors - InputBlocks.py")
    import LineFunctions

GDF_NAME_FOR_HOUSE_SECTION = "HOUSE NEW"
GDF_NAME_FOR_GARDEN_SECTION = "GARDEN"
GDF_NAME_FOR_PARKING_SECTION = "PARKING"

DXF_FILE_STRING = "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/dxf_files/triangle.dxf"
# DXF_FILE_STRING = "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/House_plotting_example.dxf"

dxfblock = None
gardens = None
parking = None
house = None

X,Y = 0,1


def centerDXFAtOrigin(dxf):
    """Moves the dxf until the origin is the mean of all of its points.

    *****ONLY WORKS FOR GDFs*****
    
    """

    center = unary_union(dxf.geometry).centroid
    def move(polygon):
        if polygon==None: return None
        shiftcoords = [(coord[X]-center.x, coord[Y]-center.y) for coord in polygon.exterior.coords[:-1]]
        return shapely.Polygon(shiftcoords)
    dxf.geometry = dxf.geometry.apply(move)


def set_up_colors(dxfblock):
    """
    Adds a colors column to your provided GeoDataFrame
        - This must be adjusted if the name of the expected layers change.
        - Enables you to pass your dxfblock to the "plotDXF" can be passed to the plot() method.
        - Does nothing if no colors could be added.

    Your GDF must contain at least one of the Layer names corresponding to this file's global GDF Section names.

    Args:
        dxfblock (GeoDataFrame)
    """

    colors = []
    for l in dxfblock['Layer']:
        if l == GDF_NAME_FOR_HOUSE_SECTION:
            colors.append("blue")
        elif l is GDF_NAME_FOR_GARDEN_SECTION:
            colors.append("green")
        elif l is GDF_NAME_FOR_PARKING_SECTION:
            colors.append("grey")
    
    if not colors:
        print("error with setting up colors for the dxfblock.")
    else:
        dxfblock['colors']= colors


def readDXF(file_string_to_dxf: str = DXF_FILE_STRING, convert_to_polygon: bool = True) -> tuple[geopandas.GeoDataFrame, geopandas.GeoDataFrame, geopandas.GeoDataFrame]:
    """
    Reads dxf file to get the user-drawn block and cleans the data.
        - Adds extra info to the dxf for plotting purposes (like 'Front'), and removes some info.

    Args:
        file_string_to_dxf (str): String containing the absolute path to the dxf file which represents your house file.
        convert_to_polygon (bool): Converts the shapes in the dxf geometry to polygons if True, does nothing otherwise.
    
    Returns
        (dxfblock, gardens, parking, house): Tuple containing GeoDataFrames for the overall block to be plotted, and its composite parts.
    """
    
    dxfblock = geopandas.read_file(file_string_to_dxf)

    if convert_to_polygon:
        geometry_shapes = list(dxfblock.geometry)
        new_geoms = []
        for shape in geometry_shapes:
            polygon = shapely.get_geometry(shapely.polygonize( [shape] ), 0)
            new_geoms.append(polygon)

        dxfblock = dxfblock.set_geometry(col=new_geoms, drop=True)
    
    dxfblock['geom_type']= dxfblock.geometry.type
    dxfblock = dxfblock.loc[dxfblock.geom_type == 'Polygon']
    set_up_colors(dxfblock=dxfblock)
    centerDXFAtOrigin(dxf=dxfblock)

    dxfblock = dxfblock.rename(columns={'geometry': 'MainPlot'})
    dxfblock = dxfblock.set_geometry('MainPlot')
    dxfblock = dxfblock.drop('PaperSpace', axis=1)
    dxfblock = dxfblock.drop('SubClasses', axis=1)
    dxfblock = dxfblock.drop('Linetype', axis=1)
    dxfblock = dxfblock.drop('EntityHandle', axis=1)
    dxfblock = dxfblock.drop('Text', axis=1)
    dxfblock = dxfblock.drop('geom_type', axis=1)

    gardens = dxfblock.loc[dxfblock.Layer == GDF_NAME_FOR_GARDEN_SECTION].geometry
    parking = dxfblock.loc[dxfblock.Layer == GDF_NAME_FOR_PARKING_SECTION].geometry
    house = dxfblock.loc[dxfblock.Layer == GDF_NAME_FOR_HOUSE_SECTION].geometry

    dxfblock = dxfblock.rename(columns={'Layer': 'Section'})
    dxfblock['Front'] = None
    dxfblock['Flex'] = False
    flex_regions = (dxfblock['Section']==GDF_NAME_FOR_GARDEN_SECTION) | (dxfblock['Section']==GDF_NAME_FOR_PARKING_SECTION)
    dxfblock.loc[ flex_regions, 'Flex' ] = True

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


def dxf_parallel_to_ll(dxf, center_at_origin=True, point_about_rotation=None, resultline=None):
    """Rotates the gdf until the house is parallel to the resultLine.

    The rotation is about the given point or the origin if it is not given.
    
    Returns the updated dxf.

    Normally moves the dxf to the origin after the operation.

    *****THIS ASSUMES THE DXF IS AT THE ORIGIN*****
    
    """

    if point_about_rotation is None:
        point_about_rotation=(0,0)

    house = dxf.loc[dxf.Section == GDF_NAME_FOR_HOUSE_SECTION].geometry
    if len(house) == 1:
        for actual_polygon in house:
            house = actual_polygon
    else:
        print("error when making dxf parallel to ll")

    polygonLine = shapely.LineString([house.exterior.coords[0], house.exterior.coords[1]])
    resultAngle, changeAngle = LineFunctions.findAngle(resultline), LineFunctions.findAngle(polygonLine)

    dxf.geometry = dxf.rotate(resultAngle-changeAngle, point_about_rotation, use_radians=True)

    if center_at_origin:
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


def calc_front(house_polygon):
    """Returns the Front value for the house.
    
    The Front value is the average of two vertices of an edge of the house as a Point object.
    
    The dxfblocks cannot be combined or merged yet for this method to work.
    
    """
    
    house_coords = house_polygon.exterior.coords
    front_x = (house_coords[2][X]+house_coords[3][X]) / 2
    front_y = (house_coords[2][Y]+house_coords[3][Y]) / 2
    front_coords = ( front_x, front_y )
    return shapely.Point(front_coords)


def update_dxf_front(dxf):
    """Updates the 'Front' column for the houses in the dxf."""

    houses = dxf.loc[dxf['Section'] == GDF_NAME_FOR_HOUSE_SECTION]
    front_values = houses['MainPlot'].apply(calc_front)
    # print("fv =", front_values)
    dxf.loc[dxf['Section'] == GDF_NAME_FOR_HOUSE_SECTION, 'Front'] = front_values
    

def get_dxf_as_gdf():
    """Returns the combination of the garden, parking, and house as a GeoDataFrame.
    
    Returns none if no dxf file is available.
    
    """

    return dxfblock


def get_dxf_separate():
    """Returns each part of the DXF polygon separately"""

    return gardens, parking, house