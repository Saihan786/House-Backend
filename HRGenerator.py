# House Road Generator
# Primary function of this class is to generate the numbers of houses and roads of each type to optimise to profit and cost

class ManageHouseTypes():
    houseTypes = []

    def __init__(self):
        self.NAME=0
        self.REVENUE=1
        self.COST=2
        self.WIDTH=3
        self.LENGTH=4
        self.SIZE=5
        self.houseTypes = []
    
    def userAddNewHouseType(self):
        name = input("Enter the name of this house type: ")
        revenue = input("Enter the total revenue in pounds from one ", name, " house (no symbols): ")
        cost = input("Enter the total cost in pounds for one ", name, " house (no symbols): ")
        width = input("Enter the width in metres of one ", name, " house: ")
        length = input("Enter the length in metres of one ", name, " house: ")
        size = float(width) * float(length)

        self.houseTypes.append( (name, revenue, cost, width, length, size) )

    def addNewHouseType(self, name, revenue, cost, width, length):
        size = float(width) * float(length)
        self.houseTypes.append( (name, revenue, cost, width, length, size) )

    def getHouseTypes(self):
        return self.houseTypes

    def printHouseTypes(self):
        for housetype in self.houseTypes:
            print("There is a housetype called", housetype[self.NAME], "which costs", housetype[self.COST], "pounds and has a revenue of", housetype[self.REVENUE], "pounds")
            print("It is", housetype[self.WIDTH], "metres wide and", housetype[self.LENGTH], "metres long and has a size of", housetype[self.SIZE], "squared metres")
            print()
        print()


class ManageRoadTypes():
    def __init__(self) -> None:
        self.NAME=0
        self.COST=1
        self.WIDTH=2
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

    def printRoadTypes(self):
        for roadtype in self.roadTypes:
            print("There is a roadtype called", roadtype[self.NAME], "which costs", roadtype[self.COST], "pounds and has a width of", roadtype[self.WIDTH], "metres")
        print()
    



# basic constraint of total cost being within budget and maximising profit and being within rlp size
# def generateOptimalTypes(housetypes, roadtypes, budget, maxsize):
def generateOptimalTypes():
    unitroadlength = 1    # in metres
    
    # so for two housetypes, h1 and h2 (x1, x2), and two road types, r1 and r2 (y1, y2)     (revenues are 1,2 and costs are 1,2,3,4):
    #       maximise P = h1.revenue*x1 + h2.revenue*x2
    #       y1 + y2 >= x1 + x2
    #       h1.cost*x1 + h2.cost*x2 + r1.cost*y1 + r2.cost*y2 <= budget
    #       h1.size*x1 + h2.size*x2   +   r1.width*unitroadlength*y1 + r2.width*unitroadlength*y2 <= maxsize
    #       x1 + x2 >= 0
    #       y1 + y2 >= 0

    


    
    manageht = ManageHouseTypes()
    manageht.addNewHouseType(name="housetype1", revenue=10, cost=5, width=3, length=3)
    manageht.addNewHouseType(name="housetype2", revenue=15, cost=7, width=5, length=5)

    managert = ManageRoadTypes()
    managert.addNewRoadType(name="roadtype1", cost=10, width=5)
    managert.addNewRoadType(name="roadtype2", cost=12, width=8)

    # maximise P = 
    manageht.printHouseTypes()
    managert.printRoadTypes()
    





    
    # housetypes = [ (name, revenue, cost, width, length, size) ]
    # roadtypes = [ (name, cost, width) ]
    # variables of objective function and constraint x,y,z,etc. are equivalent to the quantity of a house/road type
    # objective function which is maximise P = revenue_ht1*x + revenue_ht2*y + ... (only for houses)
    #       additional constraint formulas include: sum(allroads) >= sum(allhouses),
    #                                               cost_ht1*x + ... <= budget
    #                                               size_ht1*x + width_rt1*unitroadlength*y <= maxsize
    #                                               sum(allroads) >= 0,
    #                                               sum(allhouses) >= 0,

generateOptimalTypes()