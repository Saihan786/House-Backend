import scipy.optimize as opt
from math import floor

# House Road Generator
# Primary function of this class is to generate the numbers of houses and roads of each type to optimise to profit and cost
# TODO:
#   number of bedrooms constraint
#   max number of units constraint
#   remove budget constraint
#   other constraints from Dan

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


# returns resulting proportions of housetypes and profit achieved using simplex to maximise the profit
def simplexmax(revenues, costs, sizes, budget, maxsize):
    objective = [-1*x for x in revenues]
    ineq_coeffs = [costs] + [sizes]
    ineq_values = [budget, maxsize]

    result = opt.linprog(objective, A_ub=ineq_coeffs, b_ub=ineq_values)

    proportions = result.x
    proportions = [floor(x) for x in proportions]
    
    totalprofit = 0
    profits = []
    for i in range(len(proportions)):
        profits.append(proportions[i] * revenues[i])
    for profit in profits:
        totalprofit+=profit
    
    return (proportions, totalprofit)

def printResults(proportions, profit, names):
    print("The best solution is to have: ")
    for i in range(len(proportions)):
        print("     ", proportions[i], "houses of housetype", names[i])
    print("The total profit is", profit, "pounds.")

# Objective function is to maximise profit
# Basic constraints of total cost are to be within budget and to be within rlp size
def generateBestTypes(housetypes, budget=500, maxsize=500):
    NAME, REVENUE, COST, WIDTH, LENGTH, SIZE = 0, 1, 2, 3, 4, 5
    names, revenues, costs, sizes = [], [], [], []

    for housetype in housetypes:
        names.append(housetype[NAME])
        revenues.append(housetype[REVENUE])
        costs.append(housetype[COST])
        sizes.append(housetype[SIZE])
    
    (proportions, profit) = simplexmax(revenues, costs, sizes, 10000000000, 1500)
    printResults(proportions, profit, names)
    return (proportions, profit)



def examples():
    mht = ManageHouseTypes()
    mht.addNewHouseType("ht1", 100000, 0, 5, 16)
    mht.addNewHouseType("ht2", 150000, 0, 5, 17)
    mht.addNewHouseType("ht3", 175000, 0, 5, 18)
    mht.addNewHouseType("ht4", 200000, 0, 97, 1)
    mht.addNewHouseType("ht5", 215000, 0, 1, 101)
    generateBestTypes(mht.getHouseTypes())