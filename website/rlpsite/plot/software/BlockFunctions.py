"""Supporting functions when working with blocks (an abstraction over polygons)."""

import matplotlib
import geopandas.geoseries
import matplotlib.pyplot as plt
import geopandas

from shapely import Polygon, LineString, affinity, Point
from shapely import distance as dist
from shapely.ops import unary_union

try:
    from ..software import PolygonFunctions, LineFunctions, InputBlocks
    matplotlib.use('agg')

    website_call = True

except ImportError:
    import PolygonFunctions, LineFunctions, InputBlocks

X, Y = 0, 1
linep1idx, linep2idx = 0, 1


class UnitPolygon():
    """An instance of this class represents one type of block that can be plotted.
    
    This class is used to abstract over the idea of all functionalities associated with
    unit polygons, like iterating through its coordinates or moving it around, while enabling
    versatility of the actual "item_to_plot" being plotted.

    The "item_to_plot" being plotted can either be a polygon or a gdf, for now.
    
    """

    def __init__(self, type, item_to_plot) -> None:
        """Determines what the "item_to_plot" being plotted is."""
        
        if type=="gdf":
            self.type = type
        if type=="polygon":
            self.type = type
        
        self.item_to_plot = item_to_plot

    
    def __move_single_polygon(self, polygon, blockpoint, polygon_to_fit_inside=None, geometry=None):
        """Returns a single polygon moved to the desired location.

        The polygon does not have to be the item of this class instance.

        Returns None for empty Points.

        If "polygon_to_fit_inside"=True and "geometry"=True, the entire geometry must fit inside the
        polygon or None is returned for all its polygons.
        
        """

        corners = []
        try:
            for corner in polygon.exterior.coords[:-1]:
                corners.append( (corner[X]+blockpoint.coords[0][X] , corner[Y]+blockpoint.coords[0][Y]) )
        except:
            return None
        block = Polygon(corners)

        if (not polygon_to_fit_inside) or polygon_to_fit_inside.contains(block):
            return block
        else:
            return None
        
    
    def __move_single_geometry(self, blockpoint, geometry, polygon_to_fit_inside=None):
        """Returns the whole moved geometry as a list.
        
        Can be used to check if the whole moved geometry stays inside the polygon.

        If any of the polygons don't fit, returns None.
        
        """


        blocks = []
        for p in geometry:
            corners = []
            try:
                for corner in p.exterior.coords[:-1]:
                    corners.append( (corner[X]+blockpoint.coords[0][X] , corner[Y]+blockpoint.coords[0][Y]) )
            except:
                return None
            block = Polygon(corners)
            blocks.append(block)

        if polygon_to_fit_inside:
            for b in blocks:
                if not polygon_to_fit_inside.contains(b):
                    return None
        return blocks

    
    def move(self, blockpoint, polygon_to_fit_inside=None):
        """Returns a block that has been moved to the desired point. 'Blockpoint' is a Point() object or a gdf of Points.

        Cannot have a blockpoint which is a gdf while the item is a Polygon (returns None in this case).
        For a gdf blockpoint, it must have a geometry that is the same dimension as the gdf item, or None is returned.

        The block may be a single polygon or a *copy* gdf of polygons (to prevent the item from changing).
    
        Optionally returns None if the block does not fit inside the polygon.

        """

        copyblock = self.item_to_plot.copy()
        InputBlocks.centerDXFAtOrigin(copyblock)

        try:
            blockpoint.geometry
            bp_is_gdf = True
        except:
            bp_is_gdf = False

        if self.type=="polygon" and not bp_is_gdf:
            return self.__move_single_polygon(self.item_to_plot, blockpoint, polygon_to_fit_inside)

        elif self.type=="gdf" and bp_is_gdf:
            try:
                moved_polygons = []
                counter = 0
                for polygon in copyblock.geometry:
                    bp = blockpoint.geometry[counter]
                    moved_polygon = self.__move_single_polygon(polygon=polygon, blockpoint=bp, polygon_to_fit_inside=polygon_to_fit_inside)
                    moved_polygons.append(moved_polygon)
                    counter+=1
                copyblock.geometry = moved_polygons
            except Exception as e:
                print("reach none")
                print(e)
                return None
            return copyblock
        
        elif self.type=="gdf" and not bp_is_gdf:
            result = self.__move_single_geometry(blockpoint=blockpoint, geometry=copyblock.geometry, polygon_to_fit_inside=polygon_to_fit_inside)
            result = geopandas.GeoSeries(result, index=copyblock.geometry.index)
            copyblock.geometry = result
            return copyblock

        return None


    def move_to(self, up):
        """Returns a block that touches the given UP. UP is a UnitPolygon.
        
        The block may be a single polygon or a *copy* gdf of polygons (to prevent the item from changing).
    
        Optionally returns None if the block does not fit inside the polygon.

        Requires that the up has center origin to begin with.

        WIP - FIX ALL CASES

        """

        block = None
        shape_type = up.type
        
        init_point = self.centroid()
        prev_point = up.centroid()

        try:
            leq = LineFunctions.lineEQ((init_point.x, init_point.y), (prev_point.x, prev_point.y))
        except:
            raise Exception
        
        if shape_type=="polygon":
            if self.type=="polygon":
                final_point = LineFunctions.point_from_distance(leq, init_point, dist(self, up))
                centered = self.copy().center_at_origin()
                return centered.move(Point(final_point))

            elif self.type=="gdf":
                # FIX THIS CASE
                final_point = LineFunctions.point_from_distance(leq, init_point, dist(self, up))
                centered = self.copy().center_at_origin()
                return centered.move(Point(final_point))
        elif shape_type=="gdf":
            if self.type=="polygon":
                # FIX THIS CASE
                final_point = LineFunctions.point_from_distance(leq, init_point, dist(self, up))
                centered = self.copy().center_at_origin()
                return centered.move(Point(final_point))
            elif self.type=="gdf":
                distances = []
                for p in self.item_to_plot.geometry:
                    distances_to_up = geopandas.GeoSeries.distance(up.item_to_plot, p)
                    closest_distance = min(list(distances_to_up))
                    distances.append( closest_distance )
                distances = [min(distances) for d in distances]

                new_points = []
                for d in distances:
                    new_points.append( Point(LineFunctions.point_from_distance(leq, init_point, d)) )

                new_points = geopandas.GeoSeries(new_points)
                new_points_wrapper = geopandas.GeoDataFrame(geometry=new_points)
                moved_item = self.copy().move(blockpoint=new_points_wrapper)
                return moved_item
        else:
            print("Unrecognised shape_type when intersecting UnitPolygon.")
            return None
        return block
    

    def center_at_origin(self):
        """Returns a block that has been centered at the origin.
        
        For GDFs, this adjusts the actual gdf while returning a new reference to it.
        
        """
        
        if self.type=="polygon":
            return PolygonFunctions.centerAtOrigin(self.item_to_plot)
        elif self.type=="gdf":
            InputBlocks.centerDXFAtOrigin(self.item_to_plot)
            return self.item_to_plot
    

    def area(self):
        """Returns total area covered by item."""
    
        if self.type=="polygon":
            return self.item_to_plot.area
        elif self.type=="gdf":
            total_area = 0
            for area in self.item_to_plot.area:
                total_area+=area
            return total_area


    def centroid(self):
        """Returns centroid of union of polygons of item."""

        if self.type=="polygon":
            return self.item_to_plot.centroid
        elif self.type=="gdf":
            return unary_union(self.item_to_plot.geometry).centroid
    

    def intersects(self, shape, shape_type="polygon"):
        """Returns true if the item intersects the given shape.
        
        Returns true if, should the item be a gdf, any parts of the gdf
        intersect with the given block.

        shape_type indicates different cases for the shape and how the 
        UnitPolygon should treat it in each case.
        
        """
        
        if shape_type=="polygon":
            if self.type=="polygon":
                return self.item_to_plot.intersects(shape)
            elif self.type=="gdf":
                return True in list( self.item_to_plot.intersects(shape) )
        elif shape_type=="UnitPolygon":
            if self.type=="polygon":
                return self.item_to_plot.intersects(shape.item_to_plot)
            elif self.type=="gdf":
                return True in list( self.item_to_plot.intersects(shape.item_to_plot) )
        else:
            print("Unrecognised shape_type when intersecting UnitPolygon.")

        
    
    def rotate(self, line, should_be_centered=True):
        """Returns a rotated polygon or dxf, and rotates the item in both cases in the process.
        
        The rotated item is parallel to the given line.

        Centers the item at the origin normally.
        
        """


        if self.type=="polygon":
            self.item_to_plot = PolygonFunctions.rotatePolygon(LineString(line), self.item_to_plot, showRotation=False)
        elif self.type=="gdf":
            InputBlocks.dxf_parallel_to_ll(dxf=self.item_to_plot, center_at_origin=False, resultline=line)
        
        if should_be_centered:
            return self.center_at_origin()
        return self.item_to_plot
    

    def copy(self):
        """Returns a copy of this UnitPolygon instance."""

        return UnitPolygon(type=self.type, item_to_plot=self.item_to_plot)
    

    def distance(self, up):
        """Returns the distance between the item of this and the item of another
        UnitPolygon."""

    
    # def is_contained_by(self, polygon):
    #     """Checks if the item is contained inside the polygon.
        
    #     Can be used to check if the whole moved geometry stays inside the polygon.

    #     If any of the polygons don't fit, returns None.
        
    #     """

    #     if self.type=="polygon":
    #         return polygon.contains(self.item_to_plot)
    #     elif self.type=="gdf":
    #         for p in self.item_to_plot.geometry:
    #             if not polygon.contains(p):
    #                 return False

        

            

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
    

def filter_blocks(block_ups_as_rows, smallest_up=None, replaceSmall=False):
    """Filters the blocks by removing the ones that overlap with another block.
    
    Returns filtered blocks as rows.

    Returns filtered blockpoints_as_rows (under same condition as filtered blocks).
    
    """
    
    distinctblocks = []

    for x in range(-1+len(block_ups_as_rows)):
        row = []
        for y in range(len( block_ups_as_rows[x] )):
            
            block_up = block_ups_as_rows[x][y]
            keepBlock = True
            shape_type = "UnitPolygon"
            
            prev = block_ups_as_rows[x][y-1]


            if block_up.intersects(prev, shape_type=shape_type):
                keepBlock=False

            for nextrowblock in block_ups_as_rows[x+1]:
                if block_up.intersects(nextrowblock, shape_type=shape_type):
                    keepBlock=False

            if keepBlock:
                row.append(block_up)
            elif replaceSmall:
                center = block_up.centroid()
                new_block = smallest_up.move(blockpoint=center)
                row.append( UnitPolygon(type=block_up.type, item_to_plot=new_block) )

        distinctblocks.append(row)
    distinctblocks.append( block_ups_as_rows[ -1+len(block_ups_as_rows) ] )

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


def initPlot(make_smallblocks, rows_of_bps, unitPolygons, ax, rlppolygon, showInit=False):
    """Returns blockpoints (as rows) that will be included in next iteration.

    Creates an initial plot which only uses the smallest blocktype.

    This method is mostly just to see which blockpoints are not invalid for plotting
    (like blockpoints that cause overlaps with the polygon).
    
    """

    smallest_up = unitPolygons[0]
    for up in unitPolygons:
        if up.area() < smallest_up.area():
            smallest_up = up

    filtered_blockpoints_as_rows = []
    distinctblock_ups = []
    
    if make_smallblocks:
        block_ups = []
        for row in rows_of_bps:
            newbprow = []
            newblockrow = []
            for blockpoint in row:
                block = smallest_up.move(blockpoint=blockpoint)
                # block = move_block_to_point(smallest_up, blockpoint, rlppolygon)
                if block is not None:
                    newblockrow.append( UnitPolygon(type=smallest_up.type, item_to_plot=block) )
                    newbprow.append(blockpoint)
            block_ups.append(newblockrow)
            filtered_blockpoints_as_rows.append(newbprow)

        distinctblock_ups = filter_blocks(block_ups)
    else:
        for row in rows_of_bps:
            newbprow = []
            for blockpoint in row:
                block = smallest_up.move(blockpoint=blockpoint)
                if block is not None:
                    newbprow.append(blockpoint)
            filtered_blockpoints_as_rows.append(newbprow)

    if showInit:
        geopandas.GeoSeries([db.exterior for row in distinctblock_ups for db in row]).plot(ax=ax, color="green")
    return distinctblock_ups, filtered_blockpoints_as_rows


def plotNewBlocks(rows_of_bps, unitPolygons, plotting_guide, ax, rlppolygon, current_plot=None, showBlocks=False):
    """Plots a variety of blocktypes using weightedrandomness and a plotting guide.
    
    Blocks cannot be placed if they cause overlap.
    
    """

    block_ups_as_rows = []

    for x in range(len(rows_of_bps)):

        row = []
        for y in range(len( rows_of_bps[x] )):
            bp = rows_of_bps[x][y]
            bt = plotting_guide[x][y]
            up = unitPolygons[bt]

            block_dxf = up.move(blockpoint=bp, polygon_to_fit_inside=rlppolygon)
            
            if not None in list(block_dxf.geometry):
                block_up = UnitPolygon(type=up.type, item_to_plot=block_dxf)
                row.append(block_up)

        block_ups_as_rows.append(row)
    

    smallest_up = unitPolygons[0]
    for up in unitPolygons:
        if up.area() < smallest_up.area():
            smallest_up = up
    
    if current_plot:
        appended_blocks = append_blocks(block_ups_as_rows, current_plot)

        distinctblocks = []
        for i in range(len(current_plot)):
            distinctblocks += [current_plot[i]+appended_blocks[i]]
        
    else:
        distinctblocks = filter_blocks(block_ups_as_rows, smallest_up, replaceSmall=True)
        print("passed distinct")

    if showBlocks:
        geopandas.GeoSeries([block.exterior for row in distinctblocks for block in row]).plot(ax=ax, color="green")
    return distinctblocks


def move_blocks_left(block_ups_as_rows, rlppolygon, ax=None):
    """Changes the input parameter to move all blocks left until they touch to open up space for more blocks.
    
    TODO: Move first point of each row to be closer to the edge of the polygon.
    
    """

    for row in block_ups_as_rows:
        # range(1, len(row)), but later will have separate way to make first block to touch the polygon inshaallah
        for i in range(1, len(row)):
            prev = row[i-1]
            cur = row[i]

            try:
                block = cur.move_to(prev)
            except Exception as e:
                print("\n\n\n")
                print("Exception:", e)
                print("prev:")
                print(prev.item_to_plot)
                print("cur:")
                print(cur.item_to_plot)
                print("\n")

            row[i] = UnitPolygon(type=cur.type, item_to_plot=block)