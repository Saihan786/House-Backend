import geopandas
from matplotlib import pyplot as plt
import folium as folium
from folium.plugins import Draw
import webbrowser
import os


def getPathForRoads():
    """Returns paths to a directory containing all dgj files with roads."""

    return "../House/geojsons/gjs_with_roads"


def get_path_for_one_RLP():
    """Returns path to datageojson file."""

    return "../House/geojsons/1/data.geojson"


def get_one_RLP(path_to_rlp):
    """Returns red line plot as geopandas dataframe using given path."""

    return geopandas.read_file(path_to_rlp)


def openRLP(directory_path):
    """Opens graphs for all datageojson files in the given directory path."""
    
    for dgj in os.listdir( directory_path ):
        rlp_path = directory_path+'/'+dgj
        rlp = geopandas.read_file(rlp_path)
        rlp.plot()
    plt.show()


def get_RLPs_from_directory_path(directory_path):
    """Returns a list of gdfs for each datageojson file in the given directory."""

    gdfs = []
    
    for dgj in os.listdir( directory_path ):
        rlp_path = directory_path+'/'+dgj
        rlp = geopandas.read_file(rlp_path)
        gdfs.append(rlp)
    return gdfs


def makeEmptyMap():
    """Makes an empty world map to draw the red line plot on."""

    fmap = folium.Map(location=(51.5,0.127))
    Draw(export=True).add_to(fmap)
    fmap.save('map.html')
    webbrowser.open('file://' + os.path.realpath('map.html'))


def main():
    path_to_rlp = "../House/geojsons/gjs_with_roads"
    path_to_rlp = "../House/geojsons/1"
    openRLP(path_to_rlp)
    # makeEmptyMap()
# main()