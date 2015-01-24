__author__ = 'robert'

import CSimulation
import time
import pickle
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations

"""
Simple example for using the Simulation class together with any Visualization
"""

# Create simulation object
simulation = CSimulation.CSimulation()
print("100 iterations without graphics")
simulation.run_n_timesteps(100)
print("now with graphics")
#choose a visualization and initialize it
visualization = CCombinationOfVisualizations(simulation)
visualization.init_display()
#modify the simulation that it can be visualized
add_visualization_to_simulation(simulation, visualization)

#Start the simulation
print("Start simulation")
print(simulation)
simulation.run()
