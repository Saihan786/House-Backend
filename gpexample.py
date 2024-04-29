import geopandas
from geodatasets import get_path
import geopandas.datasets
from matplotlib import pyplot as plt

path_to_data = get_path("nybb")
world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
gdf = geopandas.read_file(path_to_data)