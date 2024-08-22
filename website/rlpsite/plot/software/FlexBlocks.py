"""The functions here are used to support the stretching of regions in gdfs which will be used to fill up remaining space."""

from shapely import Polygon
import matplotlib.pyplot as plt
import geopandas


fig, ax = plt.subplots()

def stretch_one_vertex(p, vindex, dir):
    """Stretches a polygon by one of its vertices.
    
    'dir' will be used to determine the direction. The direction will be
    parallel to one of the adjacent sides of the vertex, and will only cause
    an increase in size.
    
    """
    
    
    box_for_reference = Polygon([ (1,1),(1,10),(10,10),(10,1),(1,1) ])
    p = Polygon([ (5,5),(5,8),(8,8),(8,5),(5,5) ])
    vindex = 3



    
    
    
    geopandas.GeoSeries(box_for_reference.exterior).plot(ax=ax, color="red")
    geopandas.GeoSeries(p.exterior).plot(ax=ax, color="green")
    plt.show()


def stretch(dxf):
    """Stretches a dxfblock by its flex regions"""

    from InputBlocks import readDXF
    dxf, gardens, parking, house = readDXF()
    print(dxf)

    flex_dxf = dxf.loc[ dxf['Flex']==True ]
    stretch_one_vertex(None, None, None)
    
stretch(None)