# don't consider budget or road costs
# might be easier to work with one blocktype for now

import matplotlib
import geopandas.geoseries
import matplotlib.pyplot as plt
import geopandas
import numpy as np

from shapely import Polygon, LineString, affinity, Point, intersection


try:
    from .HRGenerator import ManageBlockTypes, generateBestTypes, generateBasicTypes, indexweightrandom
    from .RedLinePlot import getRLP, getPath
    from ..software import PolygonFunctions, LineFunctions
    matplotlib.use('agg')

except ImportError:
    from HRGenerator import ManageBlockTypes, generateBestTypes, generateBasicTypes, indexweightrandom
    from RedLinePlot import getRLP, getPath
    import PolygonFunctions, LineFunctions


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


def blocklines(path, distance, rlppolygon, pathIsHorizontal, ax=None, longestline=None):
    """Returns a list of all new lines, each from a point on the lines of the given path.

    The points are equidistant from each other at a given distance.
    
    The new lines have the given gradient m.
    
    """

    lines = []
    p1 = path[0][linep1idx]

    lleq = LineFunctions.lineEQ(longestline[linep1idx], longestline[linep2idx])
    nleq = LineFunctions.normalLineEQ(lleq, p1)

    if pathIsHorizontal:
        x = p1[X]

        points = []
        while x < path[ -1+len(path) ][linep2idx][X]:
            y = LineFunctions.lineyval(lleq, x)
            points.append( (x,y) )
            point = (x,y)
            
            nleq = LineFunctions.normalLineEQ(lleq, point)
            newline = LineFunctions.leqtoline(nleq, rlppolygon)
            lines.append(newline)
            
            x+=distance

    else:
        y = p1[Y]

        points = []
        while y > path[ -1+len(path) ][linep2idx][Y]:
            x = LineFunctions.linexval(nleq, y)
            points.append( (x,y) )
            point = (x,y)

            lleq = LineFunctions.normalLineEQ(nleq, point)
            newline = LineFunctions.leqtoline(lleq, rlppolygon)
            lines.append(newline)

            y-=distance

    return lines


def move_block_to_point(up, blockpoint, rlppolygon):
    """Returns a block that has been moved to the desired point.
    
    Returns None if the block does not fit inside the polygon.

    Requires that the up has center origin to begin with.
    
    """
    
    corners = []
    for corner in up.exterior.coords[:-1]:
        corners.append( (corner[X]+blockpoint.coords[0][X] , corner[Y]+blockpoint.coords[0][Y]) )
    block = Polygon(corners)

    if rlppolygon.contains(block):
        return block
    else:
        return None
    

def filter_blocks(blocks, smallBlocks=None, replaceSmall=False):
    """Filters the blocks by removing the ones that overlap with another block.
    
    Returns filtered blocks.
    
    *****NEEDS TO BE OPTIMISED FOR PERFORMANCE, SEE BELOW*****
    
    """
    
    distinctblocks = []

    # THIS SHOULD BE OPTIMISED (IT'S O(N^2) RIGHT NOW, FAR TOO SLOW AND UNSCALEABLE)
    for i in range(len(blocks)):
        keepBlock = True
        for j in range(i+1, len(blocks)):
            if blocks[i].intersects(blocks[j]):
                keepBlock = False
        if keepBlock:
            distinctblocks.append(blocks[i])
        elif replaceSmall:
            distinctblocks.append(smallBlocks[i])

    return distinctblocks


def initPlot(blockpoints, unitPolygons, ax, rlppolygon, showInit=False):
    """Returns a list of the each smallest block to be plotted.

    Returns blockpoints that will be included in next iteration.

    Creates an initial plot which only uses the smallest blocktype.
    
    """

    blocks = []

    smallest_up = unitPolygons[0]
    for up in unitPolygons:
        if up.area < smallest_up.area:
            smallest_up = up

    filtered_blockpoints = []
    for blockpoint in blockpoints:
        block = move_block_to_point(smallest_up, blockpoint, rlppolygon)
        if block is not None:
            blocks.append(block)
            filtered_blockpoints.append(blockpoint)

    distinctblocks = filter_blocks(blocks)

    # print("number of blocks on plot:", len(distinctblocks))
    if showInit:
        geopandas.GeoSeries([db.exterior for db in distinctblocks]).plot(ax=ax, color="green")
    return distinctblocks, filtered_blockpoints


def replaceBlocks(blockpoints, unitPolygons, plot_blocktypes, smallBlocks, ax, rlppolygon):
    """Plots different blocktypes using weightedrandomness and an initial plot.
    
    If a block can't be replaced, it stays the same.
    
    """

    blocks = []

    for i in range(len(blockpoints)):
        bp = blockpoints[i]
        bt = plot_blocktypes[i]
        up = unitPolygons[bt]

        block = move_block_to_point(up, bp, rlppolygon)
        if block is not None:
            blocks.append(block)
    
    distinctblocks = filter_blocks(blocks, smallBlocks, replaceSmall=False)

    # print("number of blocks on plot:", len(distinctblocks))
    geopandas.GeoSeries([block.exterior for block in distinctblocks]).plot(ax=ax, color="green")
    return distinctblocks
    

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
    # blockpadding, rowpadding = 30, 50

    fig, ax = plt.subplots()

    if horizontal_has_longest:
        perpLines = blocklines(linePathX, blockpadding, rlppolygon, pathIsHorizontal=True, ax=ax, longestline=longestline)
        parallelLines = blocklines(linePathY, rowpadding, rlppolygon, pathIsHorizontal=False, ax=ax, longestline=longestline)            
    else:
        perpLines = blocklines(linePathX, rowpadding, rlppolygon, pathIsHorizontal=True, ax=ax, longestline=longestline)
        parallelLines = blocklines(linePathY, blockpadding, rlppolygon, pathIsHorizontal=False, ax=ax, longestline=longestline)            
    
    blockpoints = []
    for l1 in perpLines:
        for l2 in parallelLines:
            blockpoint = intersection(l1, l2)
            if not blockpoint.is_empty:
                blockpoints.append(blockpoint)

    # geopandas.GeoSeries(parallelLines).plot(ax=ax, color="green")
    # geopandas.GeoSeries(perpLines).plot(ax=ax, color="green")
    
    smallBlocks, blockpoints = initPlot(blockpoints, unitPolygons, ax=ax, rlppolygon=rlppolygon, showInit=False)

    plot_blocktypes = indexweightrandom(numspaces=len(smallBlocks), blocktypes=blocktypes)
    randomBlocks = replaceBlocks(blockpoints, unitPolygons, plot_blocktypes, smallBlocks, ax, rlppolygon)

    geopandas.GeoSeries(rlppolygon.exterior).plot(ax=ax, color="blue")
    plt.show()
    return (fig, randomBlocks)



def example():
    rlp = getRLP(getPath())
    rlp = rlp.to_crs(epsg=27700)

    rlppolygon = rlp.geometry[0]
    
    mht = ManageBlockTypes()
    fillMHT(mht)
    blocktypes = mht.getBlockTypes()

    unitPolygons = makeUnitPolygons(blocktypes)

    bestproportions, profit = generateBestTypes(blocktypes, maxsize=rlppolygon.area, showResults=False)
    mht.addProportions(bestproportions)

    return plotProportions(blocktypes, unitPolygons, bestproportions, rlppolygon)


def startplot(rlp, showCloseToOrigin=True):
    rlp = rlp.to_crs(epsg=27700)
    rlppolygon = rlp.geometry[0]
    if showCloseToOrigin:
        rlppolygon = PolygonFunctions.moveToOrigin(rlppolygon)
    
    mht = ManageBlockTypes()
    fillMHT(mht)
    blocktypes = mht.getBlockTypes()

    unitPolygons = makeUnitPolygons(blocktypes)

    basicproportions = generateBasicTypes(mht.getBlockTypes(), maxsize=rlppolygon.area, showResults=False)
    mht.addProportions(basicproportions)
    return plotProportions(blocktypes, unitPolygons, basicproportions, rlppolygon)

example()
# plt.show()