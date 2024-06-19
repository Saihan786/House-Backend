class HouseTypes():
    houseTypes = []

    def __init__(self):
        self.houseTypes = []
    
    def userAddNewHouseType(self):
        name = input("Enter the name of this house type: ")
        profit = input("Enter the total profit in pounds from one house of this house type (no symbols): ")
        width = input("Enter the width in metres of one house of this house type: ")
        length = input("Enter the length in metres of one house of this house type: ")
        size = float(width) * float(length)

        self.houseTypes.append( (name, profit, width, length, size) )

    def addNewHouseType(self, name, profit, width, length):
        size = float(width) * float(length)
        self.houseTypes.append( (name, profit, width, length, size) )

    def getHouseTypes(self):
        return self.houseTypes


class RoadTypes():
    def __init__(self) -> None:
        self.roadTypes = []

    def userAddNewRoadType(self):
        name = input("Enter the name of this house type: ")
        cost = input("Enter the cost in pounds of one house of this house type: ")
        width = input("Enter the width in metres of one house of this house type: ")

        self.roadTypes.append( (name, cost, width) )

    def addNewRoadType(self, name, cost, width):
        self.roadTypes.append( (name, cost, width) )


    def getRoadTypes(self):
        return self.roadTypes