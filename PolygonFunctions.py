""""Supporting functions when working with polygons."""

from shapely import Polygon, LineString, affinity
import geopandas
import matplotlib.pyplot as plt
import LineFunctions


X,Y = 0,1
linep1idx, linep2idx = 0, 1


def findLongestLineIndex(polygon):
    """Supporting method to find the longest line and adjacent line.
    
    Returns the list of lines and index of the longest line from the polygon.
    
    """

    b = polygon.boundary.coords
    lines = [LineString(b[point:point+2]) for point in range(len(b)-1)]

    length = 0
    longestlineindex = 0
    for i in range(len(lines)):
        if lines[i].length>length:
            length=lines[i].length
            longestlineindex = i

    return (lines, longestlineindex)


def findLongestLine(polygon):
    """Returns longest line of the polygon."""

    lines, longestlineindex = findLongestLineIndex(polygon)

    return lines[longestlineindex].coords


def findAdjacentLine(polygon):
    """Returns the line adjacent to the longest line of the polygon, and the point at which they meet.

    Returns ([adjacent line coords], [corner])
    
    """
    
    lines, longestlineindex = findLongestLineIndex(polygon)
    
    adjacentlineindex = longestlineindex+1
    if adjacentlineindex >= len(lines) : adjacentlineindex = 0

    corner = None
    for lcoord in lines[longestlineindex].coords:
        for acoord in lines[adjacentlineindex].coords:
            if lcoord==acoord:
                corner = lcoord

    return (lines[adjacentlineindex].coords, corner)


def findAdjacentLines(polygon):
    """Returns linePathX and linePathY which are each associated with a parallel/perpendicular line.

    Returns [ (linePathX, gradient) , (linePathY, gradient) ]

    Line paths are used instead of the corner to plot houses. They are lists of lines.

    The gradients are for the lines that will be plotted from the line paths.

    The line path containing the longest line will use the perpendicularline.
    
    """

    coords = polygon.exterior.coords[:-1]
    xmin = xmax = ymin = ymax = 0
    
    for idx in range(len(coords)):
        if coords[idx][X] < coords[xmin][X]:
            xmin = idx
        elif coords[idx][X] > coords[xmax][X]:
            xmax = idx
        elif coords[idx][Y] < coords[ymin][Y]:
            ymin = idx
        elif coords[idx][Y] > coords[ymax][Y]:
            ymax = idx

    
    longestline = findLongestLine(polygon)    
    mparallel, c, isV = LineFunctions.lineEQ(longestline[linep1idx], longestline[linep2idx])
    mperp = -1/mparallel

    if (-1 < mparallel < 1) or True:
        # parallel line is more horizontal
        #   so the parallel line will be for the ypath and ypath will not include the longest line
        #   and the perpendicular line will be for the xpath and xpath will include the longest line.
        

        def find_path(startpoint, endpoint, longestline):
            """Returns a list of coordinate lines between the given points."""
            pass

        
        if longestline[linep2idx][Y] > longestline[linep1idx][Y]:
            longestline = [ longestline[linep2idx], longestline[linep1idx] ]


        if ymax > ymin:
            ymaxfirst = coords[ymax:-1] + [coords[-1]] + coords[0:ymax]
        else:
            ymaxfirst = coords[ymax:ymin+1]

        for i in range(-1+len(ymaxfirst)):
            line = [ymaxfirst[i], ymaxfirst[i+1]]
            if line==[c for c in longestline]:
                # This path contains the longest line, so have to change it.

                rcoords = list(reversed(coords))
                rymax = len(coords)-ymax-1
                ymaxfirst = rcoords[rymax:-1] + [rcoords[-1]] + rcoords[0:rymax]

        ypath = []
        for i in range(-1+len(ymaxfirst)):
            ypath.append([ymaxfirst[i], ymaxfirst[i+1]])

            if ymaxfirst[i+1]==coords[ymin]:
                break
        
        


        if longestline[linep2idx][X] < longestline[linep1idx][X]:
            longestline = [ longestline[linep2idx], longestline[linep1idx] ]

        if xmin > xmax:
            xminfirst = coords[xmin:-1] + [coords[-1]] + coords[0:xmin]
        else:
            xminfirst = coords[xmin:xmax+1]
        

        containsLongest = False
        for i in range(-1+len(xminfirst)):
            line = [xminfirst[i], xminfirst[i+1]]
            if line==[c for c in longestline]:
                # This path contains the longest line, so don't have to change it.
                containsLongest = True
                
        if not containsLongest:
            # change this path
                rcoords = list(reversed(coords))
                rxmin = len(coords)-xmin-1
                xminfirst = rcoords[rxmin:-1] + [rcoords[-1]] + rcoords[0:rxmin]
        

        xpath = []
        for i in range(-1+len(xminfirst)):
            xpath.append([xminfirst[i], xminfirst[i+1]])

            if xminfirst[i+1]==coords[xmax]:
                break
                
                
        # repeat the above process for the xpath, then repeat all of this for the else case.


        
        
    else:
        # parallel line is more vertical
        #   so the parallel line will be for the xpath and xpath will not include the longest line
        pass

    import geopandas
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    geopandas.GeoSeries(polygon.exterior).plot(ax=ax, color="blue")
    geopandas.GeoSeries([LineString(c) for c in xpath]).plot(ax=ax, color="green")
    plt.show()
    
















from RedLinePlot import getRLP, getPath
rlp = getRLP(getPath())
rlp = rlp.to_crs(epsg=27700)
rlp["name"] = ["rlp"]
rlppolygon = rlp.geometry[0]

findAdjacentLines(rlppolygon)






def lines(polygon):
        """Returns the longest line and its adjacent line of a given polygon."""

        longestline = findLongestLine(polygon)
        longestline = LineFunctions.orderLine(longestline)
        adjacentline, corner = findAdjacentLine(polygon)
        adjacentline = LineFunctions.orderLine(adjacentline)

        return longestline, adjacentline, corner


def adjacentlines(polygon):
    pass


def rotatePolygon(resultLine, polygon, showRotation=False):
    """"Rotates the polygon until it is parallel to the line.
    
    Prints meta information about the rotation and displays it if boolean is set to True.
        NOTE: In order to effectively display the rotation, the resultLine and polygon must be relatively close to each other.
    
    Returns the rotated polygon.
    
    """

    oldPolygon = polygon
    polygonLine = LineString([polygon.exterior.coords[0], polygon.exterior.coords[1]])

    resultAngle, changeAngle = LineFunctions.findAngle(resultLine), LineFunctions.findAngle(polygonLine)
    polygon = affinity.rotate(polygon, resultAngle-changeAngle, origin="centroid", use_radians=True)
    polygonLine = LineString([polygon.exterior.coords[0], polygon.exterior.coords[1]])
    

    if showRotation:
        ax = geopandas.GeoSeries(resultLine).plot()
        geopandas.GeoSeries(oldPolygon).plot(ax=ax, color="red")
        geopandas.GeoSeries(polygon).plot(ax=ax, color="green")
        plt.show()

        print("Original angle of polygonLine is", changeAngle)
        print("The rotated angle of polygonLine should be", resultAngle)
        print("The actual rotated angle is", LineFunctions.findAngle(polygonLine))
        if LineFunctions.isParallel(polygonLine, resultLine):
            print("Successful rotation")
        else:
            print("Unsuccessful rotation")
    
    return polygon


def moveToOrigin(polygon, showTranslation=False):
    """Moves the polygon until two of its vertices touch the axis lines.

    Exists the option to show the translation, which is only effective if the distance translated is not too large.
    
    Returns the moved polygon.
    
    """

    X,Y = 0,1
    leftmost = polygon.exterior.coords[0][X]
    bottom = polygon.exterior.coords[0][Y]
    for coord in polygon.exterior.coords[1:-1]:
        if coord[X] < leftmost : leftmost=coord[X]
        if coord[Y] < bottom : bottom=coord[Y]
    
    shiftcoords = [(coord[X]-leftmost, coord[Y]-bottom) for coord in polygon.exterior.coords[:-1]]

    if showTranslation:
        ax = geopandas.GeoSeries(Polygon(shiftcoords).exterior).plot(color="green")
        geopandas.GeoSeries(polygon.exterior).plot(ax=ax, color="red")
        plt.show()
    
    return Polygon(shiftcoords)