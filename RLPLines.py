import matplotlib.pyplot as plt
import numpy as np
import geopandas
from AddDataToDF import coords, rlpAsRing

oldcoords = coords()
endpoints = []
lines = []

def findLine(x1,y1, x2,y2):
    if not (x2-x1)==0:
        m = (y2-y1) / (x2-x1)
        c = y1-(m*x1)
    else:
        # add edge case for x2-x1==0
        # for now, causes error as m and c haven't been initialised so cannot be returned
        pass    
    return (m, c)


# find endpoints for each line (lines represent sides of rlp)
for i in range(-1, -1+len(oldcoords)):
    endpoints.append( (oldcoords[i], oldcoords[i+1]) )

# initialise range of x values on plot of lines
xmin, xmax = endpoints[0][0][0], endpoints[0][0][0]
for pair in endpoints:
    p1,p2 = pair
    x1,y1 = p1
    if x1 < xmin:
        xmin = x1
    if x1 > xmax:
        xmax = x1

# find line equations
for pair in endpoints:
    p1,p2 = pair
    x1,y1 = p1
    x2,y2 = p2

    m, c = findLine(x1,y1, x2, y2)
    print("y =", m, "* x   +  ", c)
    lines.append((m, c))

    x_axis = np.linspace(xmin,xmax)
    plt.plot(x_axis, m*x_axis+c, label="linear")


from shapely import LinearRing
square = LinearRing(oldcoords)
geopandas.GeoSeries(square).plot()




plt.show()