"""Classes for managing Blocks, and functions for working with groups of
Blocks."""

from typing import List, Tuple
import scipy.optimize as opt
from math import floor
from numpy import random


class BlockType:
    """
    This defines a particular "BlockType", which is used to generate
    unit blocks. Unit blocks are themselves plotted on the region.

    Attributes:
        - NAME
        - REVENUE
        - COST
        - WIDTH
        - LENGTH
        - SIZE
        - PROPORTION
    """

    def __init__(
        self,
        name: str = "",
        revenue: int = 0,
        cost: int = 0,
        width: int = 0,
        length: int = 0,
        size: int = 0,
    ):
        self.NAME = name
        self.REVENUE = revenue
        self.COST = cost
        self.WIDTH = width
        self.LENGTH = length
        self.SIZE = size
        self.PROPORTION = False

    def setProportion(self, proportion):
        self.PROPORTION = proportion

    def toList(self):
        return [
            self.NAME,
            self.REVENUE,
            self.COST,
            self.WIDTH,
            self.LENGTH,
            self.SIZE,
            self.PROPORTION,
        ]

    def printStats(self):
        print("NAME:", self.NAME)
        print("REVENUE:", self.REVENUE)
        print("COST:", self.COST)
        print("WIDTH:", self.WIDTH)
        print("LENGTH:", self.LENGTH)
        print("SIZE:", self.SIZE)
        print("PROPORTION:", self.PROPORTION)


class ManageBlockTypes:
    """
    This allows you to manage multiple "BlockTypes".
    """

    def __init__(self, existingBlockTypes: List[BlockType] = []):
        self.blockTypes = existingBlockTypes

    def userAddNewBlockType(self):
        """Enables you to manually define a new BlockType."""

        name = input("Enter the name of this block type: ")
        revenue = input(f"Enter the total revenue in pounds from one {name}: ")
        cost = input(f"Enter the total cost in pounds for one {name}: ")
        width = input(f"Enter the width in metres of one {name}: ")
        length = input(f"Enter the length in metres of one {name}: ")
        size = float(width) * float(length)

        self.blockTypes.append(
            BlockType(
                name,
                int(revenue),
                int(cost),
                int(width),
                int(length),
                int(size),
            )
        )

    def addNewBlockType(self, name, revenue, cost, width, length):
        """
        Enables you to programmatically define a new BlockType.
        Args:
            - name (str): Name of the block
            - revenue (int): How much money a block brings in.
            - cost (int): Cost of the block.
            - width (int): Width of the block.
            - length (int): Length of the block.
        """

        size = width * length
        self.blockTypes.append(
            BlockType(name, revenue, cost, width, length, size)
        )

    def setProportions(self, proportions: List[int]):
        """
        Sets the `proportion` value of each BlockType managed by
        this instance.

        Args:
            - proportions ([int]): A list of proportions. For a proportion
            with index `i` in the provided list, the corresponding BlockType
            has index `i` in the list of managed BlockTypes.
        """

        if len(proportions) == len(self.blockTypes):
            for i in range(len(proportions)):
                self.blockTypes[i].setProportion(proportions[i])

    def getBlockTypes(self) -> List[BlockType]:
        return self.blockTypes

    def getNames(self) -> List[str]:
        return [blockType.NAME for blockType in self.blockTypes]

    def getRevenues(self) -> List[int]:
        return [blockType.REVENUE for blockType in self.blockTypes]

    def getCosts(self) -> List[int]:
        return [blockType.COST for blockType in self.blockTypes]

    def getWidths(self) -> List[int]:
        return [blockType.WIDTH for blockType in self.blockTypes]

    def getLengths(self) -> List[int]:
        return [blockType.LENGTH for blockType in self.blockTypes]

    def getSizes(self) -> List[int]:
        return [blockType.SIZE for blockType in self.blockTypes]

    def getProportions(self) -> List[int]:
        return [blockType.PROPORTION for blockType in self.blockTypes]

    def printBlockTypes(self):
        for blocktype in self.blockTypes:
            print(
                f"""
                There is a blocktype called {blocktype.NAME} which costs
                {blocktype.COST} pounds, and has a revenue of
                {blocktype.REVENUE} pounds.
                """
            )
            print(
                f"""
                It is {blocktype.WIDTH} metres wide and {blocktype.LENGTH}
                metres long and has a size of {blocktype.SIZE} squared metres.
                \n
                """
            )
        print()


def simplexmax(
    revenues, costs, sizes, budget, maxsize
) -> Tuple[List[int], int]:
    """
    Calculates the optimal proportion of blocks of blocktypes
    using simplex.
        - For index `i`, `revenues[i]`, `costs[i]`, and `sizes[i]`
        must refer to the same BlockType.

    Args:
        - revenues (List[int]): The revenue of each BlockType.
        - costs (List[int]): The cost of each BlockType.
        - sizes (List[int]): The size of each BlockType.
        - budget (int): Available money to be spent, in pounds.
        - maxsize (int): Available space to work within.

    Returns:
        - Tuple
            - proportions (List[int]): A list of the proportions for each
            BlockType
            - (int): The total profit made from building every
            Block in the suggested proportions.
    """

    objective = [-1 * x for x in revenues]
    ineq_coeffs = [costs] + [sizes]
    ineq_values = [budget, maxsize]

    result = opt.linprog(objective, A_ub=ineq_coeffs, b_ub=ineq_values)

    proportions = [floor(x) for x in result.x]
    profits = []
    for i in range(len(proportions)):
        profits.append(proportions[i] * (revenues[i] - costs[i]))

    return (proportions, sum(profits))


def generateBestTypes(
    manager: ManageBlockTypes,
    budget=500,
    maxsize=500,
    showResults=False,
):
    """
    Generates a list of the optimal number of blocks of each type, and overall
    profit separately.

    Args:
        - manager (ManageBlockTypes): A ManageBlockTypes instance that
        contains information about multiple BlockTypes.
        - budget (int): Available money to be spent, in pounds.
        - maxsize (int): Available space to work within.
    """

    (proportions, profit) = simplexmax(
        manager.getRevenues(),
        manager.getCosts(),
        manager.getSizes(),
        budget,
        maxsize,
    )

    if showResults:
        print("The best solution is to have: ")
        for i in range(len(proportions)):
            proportion, name = proportions[i], manager.getNames()
            print(f"{proportion} blocks of blocktype {name}")
        print(f"The total profit is {profit} pounds.")

    return (proportions, profit)


def indexweightrandom(
    numspaces, blocktypes, rows, accuracy=0.005, showInfo=False
):
    """
    This list acts as a guide for plotting the blocks.

    The list will be accurate to within the given accuracy, but more accurate
    values will take a longer time and more processing.

    The list will be in rows matching the rows of the plot.

    Returns:
        - random_plotting_as_rows (): a list of randomly determined blocktypes
        for plotting.
    """

    # ARTIFICAL EXAMPLES
    # plot_chances = [0.5, 0.5]
    # plot_chances = [1.0, 0.0]
    # plot_chances = [1 / (len(blocktypes)) for bt in blocktypes]

    total_proportion = sum([bt.PROPORTION for bt in blocktypes])

    plot_chances = []
    for bt in blocktypes:
        plot_chances.append(bt.PROPORTION / total_proportion)

    rng = random.default_rng()
    accuracy_reached = False
    counter = 0
    while not accuracy_reached:
        if counter > 20:
            accuracy *= 2

        counter += 1
        random_plotting: List[int] = rng.choice(
            len(blocktypes), numspaces, p=plot_chances
        )

        accuracy_reached = True
        for i in range(len(blocktypes)):
            x = len([num_bts for num_bts in random_plotting if num_bts == i])
            y = len(random_plotting)
            actual_plot_chance = x / y
            if abs(plot_chances[i] - actual_plot_chance) >= accuracy:
                accuracy_reached = False
                break

    random_plotting_as_rows = []
    blocki = 0
    for row in rows:
        pb_row = []
        for i in range(len(row)):
            pb_row.append(random_plotting[blocki])
            blocki += 1
        random_plotting_as_rows.append(pb_row)

    checkrow = [bt for row in random_plotting_as_rows for bt in row]
    for bval in checkrow == random_plotting:
        if bval == False:
            print("error when generating indexweightrandom as rows")

    return random_plotting_as_rows
