import geopandas
from geodatasets import get_path
import geopandas.datasets
from matplotlib import pyplot as plt
import webbrowser
import os


path_to_data = get_path("nybb")
world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
gdf = geopandas.read_file(path_to_data)

gdf = gdf.set_index("BoroName")
gdf["boundary"] = gdf.boundary
gdf["centroid"] = gdf.centroid
gdf["distance"] = gdf["centroid"].distance(gdf["centroid"].iloc[0])
gdf["area"] = gdf.area


fmap = gdf.explore("area", legend=True)
fmap.save('map.html')
webbrowser.open('file://' + os.path.realpath('map.html'))
plt.show()