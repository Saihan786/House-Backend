"""This is the main file that generates a visualisation of a region with
houses."""

import matplotlib.pyplot as plt

import blockfiles.BlockFunctions as BlockFunctions
import blockfiles.HRGenerator as HRGenerator
import blockfiles.InputBlocks as InputBlocks
import PlotOptimals
import PolygonFunctions
import RedLinePlot


mht = HRGenerator.ManageBlockTypes()

gdfs = [RedLinePlot.get_one_RLP(RedLinePlot.get_path_for_one_RLP())]
# print(gdfs)
# gdfs = get_RLPs_from_directory_path(getPathForRoads())
print(gdfs)

fig, ax = plt.subplots()
for rlp in gdfs:
    rlp = rlp.to_crs(epsg=27700)
    rlppolygon = rlp.geometry[0]

    (dxfblock, gardens, parking, house) = InputBlocks.readDXF()
    upgdf = BlockFunctions.UnitPolygon(type="gdf", item_to_plot=dxfblock)
    unitPolygons = [upgdf]

    # for now, will set these to useless values until all other gdf
    # functionality is checked.
    # bestproportions, profit = generateBestTypes(
    #   blocktypes, maxsize=rlppolygon.area, showResults=True
    # )
    mht.addNewBlockType("gdf1", 100000, 0, 25, 30)
    bestproportions = [100]
    mht.setProportions(bestproportions)
    blocktypes = mht.getBlockTypes()
    mht.printBlockTypes()

    PlotOptimals.plot_proportions_in_region(
        blocktypes, unitPolygons, bestproportions, rlppolygon, ax=ax
    )
plt.show()


def startplot(rlp, showCloseToOrigin=True):
    mht = HRGenerator.ManageBlockTypes()

    rlp = rlp.to_crs(epsg=27700)
    rlppolygon = rlp.geometry[0]
    if showCloseToOrigin:
        rlppolygon = PolygonFunctions.moveToOrigin(rlppolygon)

    # unitPolygons = makeUnitPolygons(blocktypes)
    (dxfblock, gardens, parking, house) = InputBlocks.readDXF()
    upgdf = BlockFunctions.UnitPolygon(type="gdf", item_to_plot=dxfblock)
    unitPolygons = [upgdf]

    # fillMHT(mht)
    # blocktypes = mht.getBlockTypes()
    # bestproportions, profit = generateBestTypes(
    #   blocktypes, maxsize=rlppolygon.area, showResults=False
    # )
    # mht.setProportions(bestproportions)

    # for now, will set these to useless values until all other gdf
    # functionality is checked
    mht.addNewBlockType("gdf1", 100000, 0, 25, 30)
    bestproportions = [100]
    mht.setProportions(bestproportions)
    blocktypes = mht.getBlockTypes()

    fig, ax = plt.subplots()
    PlotOptimals.plot_proportions_in_region(
        blocktypes, unitPolygons, bestproportions, rlppolygon, ax=ax
    )
    return fig
