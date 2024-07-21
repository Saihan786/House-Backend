import geopandas
from matplotlib import pyplot as plt
import folium as folium
from folium.plugins import Draw
import webbrowser
import os

# returns path to datageojson file
def getPath():
    return "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/data.geojson"

# returns red line plot as geopandas dataframe using given path
def getRLP(path_to_rlp):
    return geopandas.read_file(path_to_rlp)

# opens a graph using given path
def openRLP(path_to_rlp):
    rlp = geopandas.read_file(path_to_rlp)
    rlp.plot()
    plt.show()

# makes an empty world map to draw the red line plot on
def makeEmptyMap():
    fmap = folium.Map(location=(51.5,0.127))
    Draw(export=True).add_to(fmap)
    fmap.save('map.html')
    webbrowser.open('file://' + os.path.realpath('map.html'))


def main():
    path_to_rlp = "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/data.geojson"
    # openRLP(path_to_rlp)
    # makeEmptyMap()
main()