"""Supporting functions when working with blocks (an abstraction over polygons)."""

import matplotlib
import geopandas.geoseries
import matplotlib.pyplot as plt
import geopandas

from shapely import Polygon, LineString, affinity, Point, intersection
from shapely import distance as dist

try:
    from ..software import PolygonFunctions, LineFunctions
    matplotlib.use('agg')

    website_call = True

except ImportError:
    import PolygonFunctions, LineFunctions

X, Y = 0, 1
linep1idx, linep2idx = 0, 1


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


def move_block_to_point(up, blockpoint, rlppolygon=None):
    """Returns a block that has been moved to the desired point.
    
    Optionally returns None if the block does not fit inside the polygon.

    Requires that the up has center origin to begin with.
    
    """
    
    corners = []
    for corner in up.exterior.coords[:-1]:
        corners.append( (corner[X]+blockpoint.coords[0][X] , corner[Y]+blockpoint.coords[0][Y]) )
    block = Polygon(corners)

    if (not rlppolygon) or rlppolygon.contains(block):
        return block
    else:
        return None
    

def filter_blocks(blocks_as_rows, smallest_up=None, replaceSmall=False):
    """Filters the blocks by removing the ones that overlap with another block.
    
    Returns filtered blocks as rows.

    Returns filtered blockpoints_as_rows (under same condition as filtered blocks).
    
    """
    
    distinctblocks = []

    for x in range(-1+len(blocks_as_rows)):
        row = []
        for y in range(len( blocks_as_rows[x] )):
            
            block = blocks_as_rows[x][y]
            keepBlock = True
            
            prev = blocks_as_rows[x][y-1]
            if block.intersects(prev):
                keepBlock=False

            for nextrowblock in blocks_as_rows[x+1]:
                if block.intersects(nextrowblock):
                    keepBlock=False

            if keepBlock:
                row.append(block)
            elif replaceSmall:
                row.append( move_block_to_point(smallest_up, block.centroid) )

        distinctblocks.append(row)
    distinctblocks.append( blocks_as_rows[ -1+len(blocks_as_rows) ] )

    return distinctblocks


def append_blocks(blocks_as_rows, current_plot):
    """Filters the blocks by removing the ones that overlap with current blocks.
    This essentially appends the blocks that can be appended.

    "current_plot" must have the same number of rows as blocks_as_rows.

    Returns filtered blocks as rows.

    Returns filtered blockpoints_as_rows (under same condition as filtered blocks).

    *****WARNING*****
    *****PERFORMANCE ISSUE O(N^2) WHEN COMPARING b_a_r TO c_p*****

    """

    distinctblocks = []

    for x in range(-1+len(blocks_as_rows)):
        row = []
        for y in range(len( blocks_as_rows[x] )):
            
            block = blocks_as_rows[x][y]
            keepBlock = True

            current_row = current_plot[x]
            for cur in current_row:
                if block.intersects(cur):
                    keepBlock = False
            
            prev = blocks_as_rows[x][y-1]
            if block.intersects(prev):
                keepBlock=False

            for nextrowblock in blocks_as_rows[x+1]:
                if block.intersects(nextrowblock):
                    keepBlock=False

            if keepBlock:
                row.append(block)

        distinctblocks.append(row)
    distinctblocks.append( blocks_as_rows[ -1+len(blocks_as_rows) ] )

    return distinctblocks


def initPlot(rows_of_bps, unitPolygons, ax, rlppolygon, showInit=False):
    """Returns blockpoints (as rows) that will be included in next iteration.

    Creates an initial plot which only uses the smallest blocktype.

    This method is mostly just to see which blockpoints are not invalid for plotting
    (like blockpoints that cause overlaps with the polygon).
    
    """

    smallest_up = unitPolygons[0]
    for up in unitPolygons:
        if up.area < smallest_up.area:
            smallest_up = up


    blocks = []
    filtered_blockpoints_as_rows = []
    for row in rows_of_bps:
        newbprow = []
        newblockrow = []
        for blockpoint in row:
            block = move_block_to_point(smallest_up, blockpoint, rlppolygon)
            if block is not None:
                newblockrow.append(block)
                newbprow.append(blockpoint)
        blocks.append(newblockrow)
        filtered_blockpoints_as_rows.append(newbprow)

    distinctblocks = filter_blocks(blocks)

    if showInit:
        geopandas.GeoSeries([db.exterior for row in distinctblocks for db in row]).plot(ax=ax, color="green")
    return distinctblocks, filtered_blockpoints_as_rows


def plotNewBlocks(rows_of_bps, unitPolygons, plotting_guide, ax, rlppolygon, current_plot=None, showBlocks=False):
    """Plots a variety of blocktypes using weightedrandomness and a plotting guide.
    
    Blocks cannot be placed if they cause overlap.
    
    """

    blocks_as_rows = []

    for x in range(len(rows_of_bps)):

        row = []
        for y in range(len( rows_of_bps[x] )):
            bp = rows_of_bps[x][y]
            bt = plotting_guide[x][y]
            up = unitPolygons[bt]

            block = move_block_to_point(up, bp, rlppolygon)
            if block is not None:
                row.append(block)

        blocks_as_rows.append(row)

    smallest_up = unitPolygons[0]
    for up in unitPolygons:
        if up.area < smallest_up.area:
            smallest_up = up
    
    if current_plot:
        appended_blocks = append_blocks(blocks_as_rows, current_plot)

        distinctblocks = []
        for i in range(len(current_plot)):
            distinctblocks += [current_plot[i]+appended_blocks[i]]
        
        
        
    else:
        distinctblocks = filter_blocks(blocks_as_rows, smallest_up, replaceSmall=True)

    if showBlocks:
        geopandas.GeoSeries([block.exterior for row in distinctblocks for block in row]).plot(ax=ax, color="green")
    return distinctblocks


def move_blocks_left(blocks_as_rows, rlppolygon, ax=None):
    """Changes the input parameter to move all blocks left until they touch to open up space for more blocks.
    
    TODO: Move first point of each row to be closer to the edge of the polygon.
    
    """

    for row in blocks_as_rows:
        # range(1, len(row)), but later will have separate way to make first block to touch the polygon inshaallah
        for i in range(1, len(row)):
            prev = row[i-1]
            cur = row[i]

            init_point = cur.centroid
            prev_point = prev.centroid

            try:
                leq = LineFunctions.lineEQ((init_point.x, init_point.y), (prev_point.x, prev_point.y))
            except:
                print(init_point)
                print(prev_point)
                raise Exception

            final_point = LineFunctions.point_from_distance(leq, (init_point.x, init_point.y), dist(prev, cur))

            up = PolygonFunctions.centerAtOrigin(cur)
            block = move_block_to_point(up, Point(final_point))

            row[i] = block