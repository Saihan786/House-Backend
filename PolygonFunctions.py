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
    """Returns the line adjacent to the longest line of the polygon, and the point at which they meet.

    Returns ([adjacent line coords], [corner])
    
    """

    coords = polygon.exterior.coords[:-1]
    
    minxvalue = min([coord[X] for coord in coords])
    maxxvalue = max([coord[X] for coord in coords])


    
    
    minxidx, maxxidx = 0, 0
    maxxfirst = []
    for i in range(len(coords)):
        if coords[i][X]==minxvalue: minxidx=i
        if coords[i][X]==maxxvalue: maxxidx=i

    maxxfirst = coords[minxidx:] + coords[0:minxidx]
    maxxfirst = coords[maxxidx:] + coords[0:maxxidx]



    lines, longestlineindex = findLongestLineIndex(polygon)
    longestline = findLongestLine(polygon)

    if longestline[linep2idx][X] < longestline[linep1idx][X]:
        longestline = [ longestline[linep2idx], longestline[linep1idx] ]

    adjacentlines = []
    if longestline[linep1idx][X]==minxvalue:
        """Only use adjacent lines up to the point with the largest x value"""

        for i in range(len(maxxfirst)):
            if maxxfirst[i][X]==minxvalue: minxidx=i
            if maxxfirst[i][X]==maxxvalue: maxxidx=i

        if longestline[linep2idx]==maxxfirst[1]:
            reversemaxXidx = len(maxxfirst) - maxxidx
            adjacentpoints = [maxxfirst[0]] + list(reversed(maxxfirst))[:reversemaxXidx]
        else:
            adjacentpoints = maxxfirst[0:maxxidx+1]

        for i in range(-1+len(adjacentpoints)):
            adjacentlines.append( LineString( [adjacentpoints[i] , adjacentpoints[i+1]] ) )
            
        
        from geopandas import GeoSeries
        from shapely import Point
        ax=GeoSeries(polygon).plot()
        # GeoSeries( adjacentlines ).plot(ax=ax, color="yellow")
        # GeoSeries( LineString(longestline) ).plot(ax=ax, color="red")
        plt.show()
        
    elif longestline[linep2idx][X]==maxxvalue:
        """Only use adjacent lines down to the point with the smallest x value"""

        for i in range(len(maxxfirst)):
            if maxxfirst[i][X]==minxvalue: minxidx=i
            if maxxfirst[i][X]==maxxvalue: maxxidx=i

        if longestline[linep1idx]==maxxfirst[1]:
            reverseminXidx = len(maxxfirst) - minxidx
            adjacentpoints = [maxxfirst[0]] + list(reversed(maxxfirst))[:reverseminXidx]
        else:
            adjacentpoints = maxxfirst[0:minxidx+1]

        for i in range(-1+len(adjacentpoints)):
            adjacentlines.append( LineString( [adjacentpoints[i] , adjacentpoints[i+1]] ) )






























    else:
        """Have to use adjacent lines in both directions"""
        


































    
    
    adjacentlineindex = longestlineindex+1
    if adjacentlineindex >= len(lines) : adjacentlineindex = 0



    corner = None
    for lcoord in lines[longestlineindex].coords:
        for acoord in lines[adjacentlineindex].coords:
            if lcoord==acoord:
                corner = lcoord

    return (lines[adjacentlineindex].coords, corner)



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