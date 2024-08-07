"""This file converts user-inputted blocks representing houses and their gardens and parking to unitPolygons used in PlotOptimals.py"""

import geopandas
import matplotlib.pyplot as plt
from shapely.ops import unary_union



data = geopandas.read_file("C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/House_plotting_example.dxf")
data['geom_type']= data.geometry.type

# remove line boundaries for now - polygons are enough to indicate regions
data = data.loc[data.geom_type == 'Polygon']
# print(data)

gardens = data.loc[data.Layer == 'GARDEN'].geometry
parking = data.loc[data.Layer == 'PARKING'].geometry
house = data.loc[data.Layer == 'HOUSE NEW'].geometry



if gardens.size==1 and parking.size==1:
    flex_regions = [gardens, parking]
    flex_polygon = geopandas.GeoSeries(unary_union(flex_regions))

up = unary_union([gardens, parking, house])

def getUP():
    return up

def plotDXF(ax=None):
    """Plots the gardens, parking, and house from a single DXF file."""

    if ax:
        geopandas.GeoSeries(gardens).plot(ax=ax, color="green")
        geopandas.GeoSeries(house).plot(ax=ax, color="blue")
        geopandas.GeoSeries(parking).plot(ax=ax, color="grey")

    else:
        fig, ax = plt.subplots()

        geopandas.GeoSeries(gardens).plot(ax=ax, color="green")
        geopandas.GeoSeries(house).plot(ax=ax, color="blue")
        geopandas.GeoSeries(parking).plot(ax=ax, color="grey")