import matplotlib.pyplot as plt
import numpy as np
import geopandas
from AddDataToDF import coords

oldcoords = coords()

def findLineFromTuples(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    if not (x2-x1)==0:
        m = (y2-y1) / (x2-x1)
        c = y1-(m*x1)
    else:
        # add edge case for x2-x1==0
        # for now, causes error as m and c haven't been initialised so cannot be returned
        pass    
    return (m, c)


from shapely import LinearRing
square = LinearRing(oldcoords)
geopandas.GeoSeries(square).plot()





# PROBLEMS:
#    I DON'T KNOW WHAT TO DO FOR VERTICAL LINES, IGNORING THIS CASE FOR NOW
#    With shapes that go back in on themselves (like concave shapes and hourglasses), the role of top and bottom is more vague and leads to issues: may need multiple tops and bottoms here
#       Maybe solve something to do with multiple lines in the same range of x values here


def rotateToMinX(coords):
    xmin = 0
    for i in range(1, len(coords)):
        xval = coords[i][0]
        curmin = coords[xmin][0]
        if xval < curmin:
            xmin = i
    return coords[xmin:]+coords[0:xmin]
oldcoords = rotateToMinX(oldcoords)


def drawRegions(regions):
    plt.figure()
    m,c = 0,1
    for region in regions:
        line1 = region[0]
        line2 = region[1]

        xmin = region[2]
        xmax = region[3]
        xspace = np.linspace(xmin, xmax)

        plt.plot(xspace, line1[m]*xspace + line1[c])
        plt.plot(xspace, line2[m]*xspace + line2[c])





# for every possible polygon, there is a:
#       start (leftmost point)
#       two lines from the start, one for the top and one for the bottom
#       top line and bottom line change every time a new point is reached
#       region in which points can appear is always between current top and bottom lines (except for hourglass-like shapes, idk what to do here yet)
#       end (rightmost point where final top and bottom lines converge)

# the array "oldcoords" contains n coordinates
# travelling from the start value [x y y y y] both forwards and backwards [y x y y y] [y y y y x]:
#       travels through the points on the paths of the top and bottom lines
#       uses left and right pointers l and r that index into the list
#       either l and r eventually equal (so they converge to the same point) OR they overlap (so l>r)
#       l and r must only start indexing AFTER the initial point, because the initial point is the same for l and r

# the end goal is to produce a list of regions
# each region is bounded by a top line, a bottom line, and a range of x values
# the range of x values represents the period in which both this top line and bottom line are used
# whenever a new point is in the path of a line (so a new line begins), a new region will be described and added to the list
plt.figure()

start = 0
x, y = 0, 1
l, r = start+1, len(oldcoords) - 1
xmin = xmax = oldcoords[start][x]

# each region here is a tuple (equation for top line, equation for bottom line, xmin, xmax)
regions = []

cur = start
lprev = rprev = start
iter = 0
while l<=r:
    print(l, r)
    topline = findLineFromTuples(oldcoords[lprev], oldcoords[l])
    bottomline = findLineFromTuples(oldcoords[rprev], oldcoords[r])

    if oldcoords[l][x] < oldcoords[r][x]:
        xmax = oldcoords[l][x]
        lprev = l
        l+=1
    else:
        xmax = oldcoords[r][x]
        rprev = r
        r-=1

    region = (topline, bottomline, xmin, xmax)
    regions.append(region)

    
    
    
    xspace = np.linspace(xmin, xmax)
    xmin = xmax
    
    # print(region)


    # plt.plot(xspace, topline[0]*xspace + topline[1], label=iter)
    # plt.plot(xspace, bottomline[0]*xspace + bottomline[1], label=iter)
    # plt.legend()


    # if iter==1 : break


    iter+=1
    # break
    print("next", l, r)

print()
print()
print()


drawRegions(regions)





plt.show()