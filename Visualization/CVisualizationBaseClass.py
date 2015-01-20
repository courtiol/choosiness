__author__ = 'robert'

"""
In this module you find different graphical representations of the simulation. Each representation of the simulation
should be derived from the the following abstract base class:
"""

#-------------------------------------abstract base class-----------------------------------
class CVisualizationBaseClass:
    """
    Abstract base class for any visualization of the simulation
    """

    def __init__(self, simulation):
        self.simulation = simulation

    def printInformationAboutPopulation(self):
        print(self.simulation.population)

    #overwrite me
    #These functions are necessary
    def drawSimulation(self):
        pass
    def initDisplay(self):
        pass
    def doInteractionWithUser(self):
        pass

"""
Very simple example
"""
class CSimpleVisualization(CVisualizationBaseClass):
    """
    . The most simple "visualization". The class just prints out information about the simulation in the terminal
    """
    def __init__(self, simulation):
        self.simulation = simulation

    def initDisplay(self):
        print("Starting the simulation:")

    def doInteractionWithUser(self):
        pass#no interaction implemented

    def drawSimulation(self):
        #print(self.simulation.step_counter)
        pass