"""
This is the main file that populates an RLP with Unit Polygons.

This file is used for both the website and the standalone software folder.
"""

import matplotlib.pyplot as plt
from matplotlib import use
website_call = False

try:
    from .HRGenerator import ManageBlockTypes, generateBestTypes, generateBasicTypes, indexweightrandom
    from .RedLinePlot import get_one_RLP, get_path_for_one_RLP, get_RLPs_from_directory_path, getPathForRoads
    from ..software import PolygonFunctions, LineFunctions, BlockFunctions, InputBlocks
    from .PlotOptimals import plot_proportions_in_region
    use('agg')

    website_call = True

except ImportError:
    print("ignore previous import errors - Main.py")
    from HRGenerator import ManageBlockTypes, generateBestTypes, generateBasicTypes, indexweightrandom
    from RedLinePlot import get_one_RLP, get_path_for_one_RLP, get_RLPs_from_directory_path, getPathForRoads
    import PlotOptimals
    import PolygonFunctions, LineFunctions, BlockFunctions, InputBlocks



# for now, will set these to useless values until all other gdf functionality is checked
mht = ManageBlockTypes()
# bestproportions, profit = generateBestTypes(blocktypes, maxsize=rlppolygon.area, showResults=True)
mht.addNewBlockType("gdf1", 100000, 0, 25, 30)
bestproportions = [100]
mht.addProportions(bestproportions)
blocktypes = mht.getBlockTypes()


if not website_call:

    gdfs = [ get_one_RLP(get_path_for_one_RLP()) ]
    gdfs = get_RLPs_from_directory_path(getPathForRoads())

    fig, ax = plt.subplots()
    for rlp in gdfs:
        rlp = rlp.to_crs(epsg=27700)
        rlppolygon = rlp.geometry[0]

        (dxfblock, gardens, parking, house) = InputBlocks.readDXF()

        upgdf = BlockFunctions.UnitPolygon(type="gdf", item_to_plot=dxfblock)
        unitPolygons = [upgdf]

        PlotOptimals.plot_proportions_in_region(blocktypes, unitPolygons, bestproportions, rlppolygon, ax=ax)
        break
    plt.show()


def startplot(rlp, showCloseToOrigin=True):
    rlp = rlp.to_crs(epsg=27700)
    rlppolygon = rlp.geometry[0]
    if showCloseToOrigin:
        rlppolygon = PolygonFunctions.moveToOrigin(rlppolygon)
    


    # unitPolygons = makeUnitPolygons(blocktypes)
    (dxfblock, gardens, parking, house) = InputBlocks.readDXF()
    upgdf = BlockFunctions.UnitPolygon(type="gdf", item_to_plot=dxfblock)
    unitPolygons = [upgdf]


    # PlotOptimals.fillMHT(mht)
    # blocktypes = mht.getBlockTypes()
    # bestproportions, profit = generateBestTypes(blocktypes, maxsize=rlppolygon.area, showResults=False)
    # mht.addProportions(bestproportions)

    fig, ax = plt.subplots()
    plot_proportions_in_region(blocktypes, unitPolygons, bestproportions, rlppolygon, ax=ax)
    return fig
