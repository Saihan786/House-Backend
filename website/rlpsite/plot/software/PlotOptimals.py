# don't consider budget or road costs
# might be easier to work with one blocktype for now

import matplotlib
import geopandas.geoseries
import matplotlib.pyplot as plt
import geopandas
import numpy as np

from shapely import Polygon, LineString, affinity, Point, intersection
from shapely import distance as dist

website_call = False


try:
    from .HRGenerator import ManageBlockTypes, generateBestTypes, generateBasicTypes, indexweightrandom
    from .RedLinePlot import getRLP, getPath
    from ..software import PolygonFunctions, LineFunctions, BlockFunctions, InputBlocks
    matplotlib.use('agg')

    website_call = True

except ImportError:
    from HRGenerator import ManageBlockTypes, generateBestTypes, generateBasicTypes, indexweightrandom
    from RedLinePlot import getRLP, getPath
    import PolygonFunctions, LineFunctions, BlockFunctions, InputBlocks


X, Y = 0, 1
linep1idx, linep2idx = 0, 1

def fillMHT(mht):
    mht.addNewBlockType("ht1", 100000, 0, 25, 30)
    mht.addNewBlockType("ht2", 150000, 0, 50, 50)


def makeUnitPolygons(blocktypes):
    """Returns a list of unit polygons for each blocktype
    
    Unit polygons can be adjusted around the rlp by adding to its x and y values.

    """

    unitPolygons = []
    for bt in blocktypes:
        point1 = (0,0)
        point2 = (0+bt.WIDTH,0)
        point3 = (0,0+bt.LENGTH)
        point4 = (0+bt.WIDTH,0+bt.LENGTH)
        unitPolygons.append(Polygon([point1, point2, point4, point3, point1]))

    return unitPolygons


def findPadding(unitPolygons, longestline):
    """Returns blockpadding and rowpadding.
    
    Blockpadding is the largest parallel length of all unit polygons with a bit added.
    Rowpadding is the largest perpendicular length of all unit polygons with a bit added.

    Padding is calculated iteratively.
    
    """

    def calculateDistance(leq, padding=0, increment=10, showDistance=False):
        """Returns the (slightly increased) distance across the largest polygon, with respect to the
        given line equation.
        
        """
        
        originalx = 0
        originaly = LineFunctions.lineyval(leq, originalx)

        allups = []

        for up in unitPolygons:
            up1 = up2 = Polygon( [(c[X]+originalx,c[Y]+originaly) for c in list(up.exterior.coords)] )

            x=0
            while up1.intersects(up2):
                x += increment
                y = LineFunctions.lineyval(leq, x)
                up2 = Polygon( [(c[X]+x,c[Y]+y) for c in list(up.exterior.coords)] )
            
            distance = np.sqrt(np.square(x-originalx) + np.square(y-originaly))
            if padding<distance : padding = distance

            allups.append(up1)
            allups.append(up2)

        if showDistance:
            geopandas.GeoSeries([up.exterior for up in allups]).plot()
            plt.show()

        return padding

    leq = LineFunctions.lineEQ(longestline[linep1idx], longestline[linep2idx])
    blockpadding = calculateDistance(leq, showDistance=False)

    nleq = LineFunctions.normalLineEQ(leq, longestline[linep1idx])
    rowpadding = calculateDistance(nleq, showDistance=False)

    return (blockpadding, rowpadding)


def plotProportions(blocktypes, unitPolygons, proportions, rlppolygon):
    """Plots all blocktypes on the rlp.
    
    The number of blocks of each bt depends on its proportion in proportions.
    
    Unit polygons are copied and moved around the rlp to create new blocks.

    Blockpadding is for perp lines, while Rowpadding is for parallel lines.
    
    """

    longestline = PolygonFunctions.findLongestLine(rlppolygon)

    unitPolygons = [PolygonFunctions.rotatePolygon(LineString(longestline), uP, showRotation=False) for uP in unitPolygons]
    unitPolygons = [PolygonFunctions.centerAtOrigin(uP, showTranslation=False) for uP in unitPolygons]

    horizontal_has_longest, (linePathX, mX), (linePathY, mY) = PolygonFunctions.findLinePaths(rlppolygon, showPaths=False)

    blockpadding, rowpadding = findPadding(unitPolygons, longestline)

    fig, ax = plt.subplots()

    if horizontal_has_longest:
        perpLines = BlockFunctions.blocklines(linePathX, blockpadding, rlppolygon, pathIsHorizontal=True, ax=ax, longestline=longestline)
        parallelLines = BlockFunctions.blocklines(linePathY, rowpadding, rlppolygon, pathIsHorizontal=False, ax=ax, longestline=longestline)            
    else:
        perpLines = BlockFunctions.blocklines(linePathX, rowpadding, rlppolygon, pathIsHorizontal=True, ax=ax, longestline=longestline)
        parallelLines = BlockFunctions.blocklines(linePathY, blockpadding, rlppolygon, pathIsHorizontal=False, ax=ax, longestline=longestline)            
    
    blockpoints = []
    rows_of_bps = []
    for l1 in parallelLines:
        row = []
        for l2 in perpLines:
            blockpoint = intersection(l1, l2)
            if not blockpoint.is_empty:
                blockpoints.append(blockpoint)
                row.append(blockpoint)
        rows_of_bps.append(row)

    # geopandas.GeoSeries(parallelLines+perpLines).plot(ax=ax, color="red")
    
    smallBlocks_as_rows, blockpoints_as_rows = BlockFunctions.initPlot(rows_of_bps, unitPolygons, ax=ax, rlppolygon=rlppolygon, showInit=False)
    num_blocks = len( [bp for row in blockpoints_as_rows for bp in row] )


    new_blocks_as_rows = []
    no_change = 0
    while no_change < 5:
        prev_blocks = new_blocks_as_rows
        
        plotting_guide = indexweightrandom(numspaces=num_blocks, blocktypes=blocktypes, rows=blockpoints_as_rows)
        new_blocks_as_rows = BlockFunctions.plotNewBlocks(blockpoints_as_rows, unitPolygons, plotting_guide, ax, rlppolygon, current_plot=new_blocks_as_rows, showBlocks=False)

        BlockFunctions.move_blocks_left(new_blocks_as_rows, rlppolygon, ax=ax)

        sanitised_blocks = []
        for row in new_blocks_as_rows:
            trow = []
            for block in row:
                if rlppolygon.contains(block):
                    trow.append(block)
                else:
                    print("block outside plot")
            sanitised_blocks.append(trow)
        new_blocks_as_rows=sanitised_blocks

        sizeprev = len([block.exterior for row in prev_blocks for block in row])
        sizenew = len([block.exterior for row in new_blocks_as_rows for block in row])

        if sizeprev==sizenew:
            no_change+=1

    print(len([block.exterior for row in new_blocks_as_rows for block in row]))

    geopandas.GeoSeries([block.exterior for row in new_blocks_as_rows for block in row]).plot(ax=ax, color="green")
    geopandas.GeoSeries(rlppolygon.exterior).plot(ax=ax, color="blue")

    return fig



def example():
    rlp = getRLP(getPath())
    rlp = rlp.to_crs(epsg=27700)

    rlppolygon = rlp.geometry[0]
    
    mht = ManageBlockTypes()
    fillMHT(mht)
    blocktypes = mht.getBlockTypes()

    unitPolygons = makeUnitPolygons(blocktypes)
    # unitPolygons =  [getUP()] + makeUnitPolygons(blocktypes)
    print(unitPolygons)

    bestproportions, profit = generateBestTypes(blocktypes, maxsize=rlppolygon.area, showResults=True)
    mht.addProportions(bestproportions)

    return plotProportions(blocktypes, unitPolygons, bestproportions, rlppolygon)

if not website_call:
    # example()


    rlp = getRLP(getPath())
    rlp = rlp.to_crs(epsg=27700)
    rlppolygon = rlp.geometry[0]
    fig, ax = plt.subplots()

    (dxfblock, gardens, parking, house) = InputBlocks.readDXF()
    upgdf = BlockFunctions.UnitPolygon(type="gdf", item_to_plot=dxfblock)
    
    InputBlocks.plotDXF(upgdf.item_to_plot, ax=ax)

    upgdf.move(Point(10,10))
    upgdf.center_at_origin()
    print(upgdf.intersects(shape=Point(100,200)))
    InputBlocks.plotDXF(upgdf.item_to_plot, ax=ax)
    
    geopandas.GeoSeries(upgdf.centroid()).plot(ax=ax, color="black")



    plt.show()


def startplot(rlp, showCloseToOrigin=True):
    rlp = rlp.to_crs(epsg=27700)
    rlppolygon = rlp.geometry[0]
    if showCloseToOrigin:
        rlppolygon = PolygonFunctions.moveToOrigin(rlppolygon)
    
    mht = ManageBlockTypes()
    fillMHT(mht)
    blocktypes = mht.getBlockTypes()

    unitPolygons = makeUnitPolygons(blocktypes)

    bestproportions, profit = generateBestTypes(blocktypes, maxsize=rlppolygon.area, showResults=False)
    mht.addProportions(bestproportions)

    return plotProportions(blocktypes, unitPolygons, bestproportions, rlppolygon)
