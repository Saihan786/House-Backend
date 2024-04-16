import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass

@dataclass
class Coordinate:
    x: float
    y: float

class Graph:    
    def __init__(self):
        self.coordinates = []
        self.fig, self.ax = plt.subplots()
        x = np.linspace(0, 2, 100)  # Sample data.


    def draw(self):
        point = plt.ginput(1)
        x = [p[0] for p in point]
        y = [p[1] for p in point]
        plt.plot(x,y)
        self.ax.figure.canvas.draw()
        

    lines = []
    def draw_line(self):
        ax = plt.gca()
        xy = plt.ginput(2)

        x = [p[0] for p in xy]
        y = [p[1] for p in xy]
        line = plt.plot(x,y)
        ax.figure.canvas.draw()

        self.lines.append(line)
        
    def __add_data_to_graph(self):
        xcoords = []
        ycoords = []
        for coord in self.coordinates:
            xcoords.append(coord.x)
            ycoords.append(coord.y)
        self.ax.scatter(xcoords,ycoords)
        
    def showGraph(self):
        self.__add_data_to_graph()
        self.draw()
        plt.show()

    def addCoord(self, coordinate: Coordinate):
        self.coordinates.append(coordinate)

    def setCoords(self, coordinates: list[Coordinate]):
        self.coordinates = self.coordinates + coordinates

    def printCoords(self):
        print(self.coordinates)



graph = Graph()
coords = [Coordinate(1,2), Coordinate(1,5), Coordinate(1,46)]
graph.setCoords(coords)
graph.showGraph()


