__author__ = 'robert'

import CSimulation
import time
import pickle
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import C1HistogramVisualization

"""
Simple example for using the Simulation class together with any Visualization
"""

# Create simulation object
simulation = CSimulation.CSimulation()
print("10 iterations without graphics")
simulation.run_n_timesteps(10)
print(simulation.settings.average_number_of_collisions_per_timestep)

print("Now with graphics")
# choose a visualization and initialize it
# Examples: C1HistogramVisualization(simulation, 800, 800)
visualization =  CCombinationOfVisualizations(simulation, simulation.settings.width, simulation.settings.height)
visualization.init_display()
# modify the simulation that it can be visualized
add_visualization_to_simulation(simulation, visualization)

# Start the simulation
print("Start simulation")
print(simulation)
simulation.run()
