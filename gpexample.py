import geopandas
from geodatasets import get_path
import geopandas.datasets
from matplotlib import pyplot as plt
import folium as folium
from folium.plugins import Draw
import webbrowser
import os

path_to_rlp = "C:/Users/Saihan Marshall/Documents/house stuff/house repo/House/data.geojson"
rlp = geopandas.read_file(path_to_rlp)
print(rlp)
rlp.plot()


# fmap = folium.Map()
# Draw(export=True).add_to(fmap)
# fmap.save('map.html')
# webbrowser.open('file://' + os.path.realpath('map.html'))
plt.show()