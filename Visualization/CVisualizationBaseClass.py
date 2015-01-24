__author__ = 'robert'

"""
In this module you find different graphical representations of the simulation. Each representation of the simulation
should be derived from the the following abstract base class:
"""

# -------------------------------------abstract base class-----------------------------------


class CVisualizationBaseClass:
    """
    This class defines the 'contract' for the interaction with the simulation class
    """

    def __init__(self, simulation):
        self.simulation = simulation

    def print_information_about_population(self):
        print(self.simulation.population)

    def draw_simulation(self):
        pass

    def init_display(self):
        pass

    def do_interaction_with_user(self):
        pass

"""
Very simple example
"""


class CSimpleVisualization(CVisualizationBaseClass):
    """
    . The most simple "visualization". The class just prints out information about the simulation in the terminal
    """
    def __init__(self, simulation):
        super(CSimpleVisualization,self).__init__(simulation)

    def init_display(self):
        print("Starting the simulation:")

    # no interaction implemented
    def do_interaction_with_user(self):
        pass

    def draw_simulation(self):
        # print(self.simulation.step_counter)
        pass