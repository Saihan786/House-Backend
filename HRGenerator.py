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
    


# I want this function to return a list of the most optimal solutions
# objective function is to maximise profit
# basic constraints of total cost being within budget and being within rlp size
# def generateOptimalTypes(housetypes, roadtypes, budget, maxsize):
def generateOptimalTypes():
    # housetypes = [ (name, revenue, cost, width, length, size) ]
    # variables of objective function and constraint x,y,z,etc. are equivalent to the quantity of a house type
    # objective function which is maximise P = revenue_ht1*x + revenue_ht2*y + ... (only for houses)
    #       additional constraint formulas include: cost_ht1*x + ... <= budget
    #                                               size_ht1*x + ... <= maxsize
    #                                               allhouses >= 0,
    









    # This example shows two lines that do NOT intersect as the budget is that much higher.
    
    # so for two housetypes, h1 and h2 (x1, x2) (revenues are 10,15 costs are 5,7, sizes are 9, 12):
    #       maximise P = h1.revenue*x1 + h2.revenue*x2
    #       h1.cost*x1 + h2.cost*x2 <= budget
    #       h1.size*x1 + h2.size*x2  <= maxsize
    #       x1, x2 >= 0    
    # maximise P = 10*x1 + 15*x2
    # 5*x1 + 7*x2 <= 1000
    # 9*x1 + 12*x2 <= 500
    # x1, x2 >= 0



    # This example shows two lines that DO intersect as the c values are close, but max size of one ht is small.
    
    # so for two housetypes, h1 and h2 (x1, x2) (revenues are 10,15 costs are 5,7, sizes are 9, 4):
    #       maximise P = h1.revenue*x1 + h2.revenue*x2
    #       h1.cost*x1 + h2.cost*x2 <= budget
    #       h1.size*x1 + h2.size*x2  <= maxsize
    #       x1, x2 >= 0    
    # maximise P = 10*x1 + 15*x2
    # 5*x1 + 7*x2 <= 500
    # 9*x1 + 4*x2 <= 500
    # x1, x2 >= 0

    # draw as linear programming since only two variables now
    # if constraint lines don't intersect, then only one type of house will be selected for this example
    # intersecting constraint lines represent similar c values, mostly (y=mx+c)
    #       if a line has a much smaller c value, it means it has relatively smaller size/money to work with
    #       so this would be the top priority (i.e. focus on house types that mitigate this)




    
    # This example will be for three housetypes, so three lines, inshaallah.

    # maximise P = 10*x1 + 15*x2 + 13*x3
    # 5*x1 + 7*x2 + 6*x3 <= 500
    # 9*x1 + 12*x2 + 2*x3 <= 500
    # x1, x2, x3 >= 0

    # simplex required


    
    manageht = ManageHouseTypes()
    manageht.addNewHouseType(name="housetype1", revenue=10, cost=5, width=3, length=3)
    manageht.addNewHouseType(name="housetype2", revenue=15, cost=7, width=2, length=2)

    # maximise P = 
    manageht.printHouseTypes()
    


    


    

# generateOptimalTypes()


# import scipy.optimize as opt

# # Coefficients of the objective function
# c = [-10, -15, -13]  # Note: maximize 10x1 + 15x2 + 13x3 is the same as minimize -10x1 - 15x2 - 13x3

# # Coefficients of the inequality constraints
# A = [
#     [5, 7, 6],
#     [9, 12, 2]
# ]

# # Right-hand side of the inequality constraints
# b = [500, 500]

# # Bounds for variables x1, x2, x3
# x_bounds = (0, None)
# bounds = [x_bounds, x_bounds, x_bounds]

# # Solve the linear programming problem
# result = opt.linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
# print(result)