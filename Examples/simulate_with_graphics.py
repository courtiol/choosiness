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
print("100 iterations without graphics")
simulation.run_n_timesteps(100)

print("Now with graphics")
# choose a visualization and initialize it
visualization = CCombinationOfVisualizations(simulation)  # or e.g. C1HistogramVisualization(simulation)
visualization.init_display()
# modify the simulation that it can be visualized
add_visualization_to_simulation(simulation, visualization)

# Start the simulation
print("Start simulation")
print(simulation)
simulation.run()
