import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass

# this makes a Graph with coordinates you can set
class Graph:    
    @dataclass
    class Coordinate:
        x: float
        y: float

    def __init__(self):
        self.coordinates = []
        self.fig, self.ax = plt.subplots()
        x = np.linspace(0, 2, 100)  # Sample data.

    def __draw(self):
        point = plt.ginput(1)
        x = [p[0] for p in point]
        y = [p[1] for p in point]
        plt.plot(x,y)
        self.ax.figure.canvas.draw()
        
    def __add_data_to_graph(self):
        xcoords = []
        ycoords = []
        for coord in self.coordinates:
            xcoords.append(coord.x)
            ycoords.append(coord.y)
        self.ax.scatter(xcoords,ycoords)
        

    def __setup_coords(self, coords: list[int]):        
        self.coordinates = []
        for x,y in zip(coords[0::2], coords[1::2]):
            self.coordinates.append(self.Coordinate(x,y))
        

    def showGraph(self):
        self.__add_data_to_graph()
        self.__draw()

    def updateGraph(self):
        plt.draw()

    def setCoords(self, coordinates: list[int]):
        self.__setup_coords(coordinates)

    def printCoords(self):
        print(self.coordinates)


