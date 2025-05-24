import scipy.optimize as opt
from math import floor
from numpy import random

# Block Road Generator
# Primary function of this class is to generate the numbers of blocks and roads of each type to optimise to profit and cost
# TODO:
#   number of bedrooms constraint
#   max number of units constraint
#   remove budget constraint
#   other constraints from Dan

class BlockType():
    NAME=""
    REVENUE=0
    COST=0
    WIDTH=0
    LENGTH=0
    SIZE=0
    PROPORTION=False

    def __init__(self, name, revenue, cost, width, length, size):
        self.NAME=name
        self.REVENUE=revenue
        self.COST=cost
        self.WIDTH=width
        self.LENGTH=length
        self.SIZE=size
    
    def addProportion(self, proportion):
        self.PROPORTION = proportion
        
    def toList(self):
        return [self.NAME, self.REVENUE, self.COST, self.WIDTH, self.LENGTH, self.SIZE, self.PROPORTION]
    
    def printStats(self):
        print("NAME:", self.NAME)
        print("REVENUE:", self.REVENUE)
        print("COST:", self.COST)
        print("WIDTH:", self.WIDTH)
        print("LENGTH:", self.LENGTH)
        print("SIZE:", self.SIZE)
        print("PROPORTION:", self.PROPORTION)


class ManageBlockTypes():
    blockTypes = []

    def __init__(self):
        self.blockTypes = []
    
    def userAddNewBlockType(self):
        name = input("Enter the name of this block type: ")
        revenue = input("Enter the total revenue in pounds from one ", name, " block (no symbols): ")
        cost = input("Enter the total cost in pounds for one ", name, " block (no symbols): ")
        width = input("Enter the width in metres of one ", name, " block: ")
        length = input("Enter the length in metres of one ", name, " block: ")
        size = float(width) * float(length)

        self.blockTypes.append( BlockType(name, revenue, cost, width, length, size) )

    def addNewBlockType(self, name, revenue, cost, width, length):
        """Adds the name, revenue, cost, width, and length."""
        
        size = float(width) * float(length)
        self.blockTypes.append( BlockType(name, revenue, cost, width, length, size) )

    def addProportions(self, proportions):
        if len(proportions)==len(self.blockTypes):
            for i in range(len(proportions)):
                self.blockTypes[i].addProportion(proportions[i])

    def getBlockTypes(self):
        return self.blockTypes

    def printBlockTypes(self):
        for blocktype in self.blockTypes:
            print("There is a blocktype called", blocktype.NAME, "which costs", blocktype.COST, "pounds and has a revenue of", blocktype.REVENUE, "pounds")
            print("It is", blocktype.WIDTH, "metres wide and", blocktype.LENGTH, "metres long and has a size of", blocktype.SIZE, "squared metres")
            print()
        print()


def simplexmax(revenues, costs, sizes, budget, maxsize):
    """Calculates and returns the optimal proportion of blocks of blocktypes using simplex."""

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
    """Prints results of generation in easily-readable format."""

    print("The best solution is to have: ")
    for i in range(len(proportions)):
        print("     ", proportions[i], "blocks of blocktype", names[i])
    print("The total profit is", profit, "pounds.")


def generateBestTypes(blocktypes, budget=500, maxsize=500, showResults=False):
    """Returns a list of the optimal number of blocks of each type, and overall profit separately.
    
    Can be used to check if an answer is optimal.
    
    """

    names, revenues, costs, sizes = [], [], [], []

    for blocktype in blocktypes:
        names.append(blocktype.NAME)
        revenues.append(blocktype.REVENUE)
        costs.append(blocktype.COST)
        sizes.append(blocktype.SIZE)
    
    (proportions, profit) = simplexmax(revenues, costs, sizes, budget, maxsize)

    if showResults : printResults(proportions, profit, names)

    return (proportions, profit)


def generateBasicTypes(blocktypes, budget=500, maxsize=500, showResults=False):
    """Returns a list of basic proportions of each blocktype.
    
    This result is more generally applicable than generateBestTypes() as the values can be used to guide
    a plotting process in order to eventually force a particular number of blocks.

    """

    (proportions, profit) = generateBestTypes(blocktypes, budget, maxsize)

    minproportion = min([p for p in proportions if p!=0])
    basicproportions = [p/minproportion for p in proportions]
    basicproportions = [round(p) for p in basicproportions]

    if showResults: print("The proportions are:", basicproportions)

    return (basicproportions)


def weightrandom(numspaces, blocktypes):
    """Returns a list of randomly determined blocktypes for initial plotting."""
    
    # for now, just to see this artificial example
    blocktypes[1].PROPORTION = 35
    
    total_proportion = sum( [bt.PROPORTION for bt in blocktypes] )

    plot_chances = []
    for bt in blocktypes:
        plot_chances.append( bt.PROPORTION / total_proportion )
    
    rng = random.default_rng()
    plot_blocktypes = rng.choice( [bt.NAME for bt in blocktypes] , numspaces, p=plot_chances)

    return plot_blocktypes


def indexweightrandom(numspaces, blocktypes, rows, accuracy=0.005, showInfo=False):
    """Returns a list of randomly determined blocktypes for initial plotting.

    This list acts as a guide for plotting the blocks.
    
    The blocktypes are represented by their index in the blocktypes array.

    The list will be accurate to within the given accuracy,
    but more accurate values will take a longer time and more processing.

    The list will be in rows matching the rows of the plot.
    
    """

    
    total_proportion = sum( [bt.PROPORTION for bt in blocktypes] )

    plot_chances = []
    for bt in blocktypes:
        plot_chances.append( bt.PROPORTION / total_proportion )
    

    # for now, just to see this artificial example
    # plot_chances = [0.5, 0.5]
    # plot_chances = [1.0, 0.0]
    plot_chances = [1/(len(blocktypes)) for i in range( len(blocktypes) )]


    rng = random.default_rng()

    accuracy_reached = False
    counter = 0
    while not accuracy_reached:

        if counter>20:
            accuracy*=2
        
        counter+=1
        plot_blocktypes = rng.choice( len(blocktypes) , numspaces, p=plot_chances)

        accuracy_reached = True
        for i in range(len(blocktypes)):
            actual_plot_chance = len( [v for v in plot_blocktypes if v==i] ) / len(plot_blocktypes)
            if abs(plot_chances[i] - actual_plot_chance) >= accuracy:
                accuracy_reached = False
                break
    
    if showInfo:
        print("counter =", counter)
        print( len( [v for v in plot_blocktypes if v==0] ) )
        print( len( [v for v in plot_blocktypes if v==0] ) / len(plot_blocktypes) )
        print( len( [v for v in plot_blocktypes if v==1] ) )
        print( len( [v for v in plot_blocktypes if v==1] ) / len(plot_blocktypes) )
        print()

    plot_blocktypes_as_rows = []
    blocki = 0
    for row in rows:
        pb_row = []
        for i in range(len(row)):
            # pb_row.append(plot_blocktypes[blocki])
            pb_row.append(plot_blocktypes[blocki])
            blocki+=1
        plot_blocktypes_as_rows.append(pb_row)
        
    checkrow = [ bt for row in plot_blocktypes_as_rows for bt in row ]
    for bval in checkrow==plot_blocktypes:
        if bval==False:
            print("error when generating indexweightrandom as rows")

    return plot_blocktypes_as_rows



def examples():
    mht = ManageBlockTypes()
    mht.addNewBlockType("ht1", 100000, 0, 5, 16)
    mht.addNewBlockType("ht2", 150000, 0, 5, 17)
    mht.addNewBlockType("ht3", 175000, 0, 5, 18)
    mht.addNewBlockType("ht4", 200000, 0, 97, 1)
    mht.addNewBlockType("ht5", 215000, 0, 1, 101)
    generateBestTypes(mht.getBlockTypes())