import matplotlib.pyplot as plt
import numpy as np
import geopandas
from AddDataToDF import coords, rlpAsRing

oldcoords = coords()
endpoints = []
lines = []

# find endpoints
for i in range(-1, -1+len(oldcoords)):
    if oldcoords[i][0] < oldcoords[i+1][0]:
        endpoints.append( (oldcoords[i], oldcoords[i+1]) )
    else:
        endpoints.append( (oldcoords[i+1], oldcoords[i]) )

# find line equations
for pair in endpoints:
    p1,p2 = pair
    x1,y1 = p1
    x2,y2 = p2
    
    line = np.polynomial.polynomial.Polynomial.fit([x1,x2], [y1,y2], 1)
    lines.append(line)

    x_axis = np.linspace(-10,10)
    axes = line.linspace(domain=x_axis)
    plt.plot(axes)



plt.show()