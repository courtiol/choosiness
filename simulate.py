__author__ = 'robert'

import CSimulation
import time
import pickle
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import C1Histogram, CNHistograms, CAverage
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import C2DVisualizationOfSimulation
from Logger.StandardLogger import CLoggerOfSimulation, add_logger_to_simulation

# Create simulation object
simulation = CSimulation.CSimulation()

# initialize logger
logger_of_simulation = CLoggerOfSimulation(simulation, 10000)  # log every 10000th iteration
add_logger_to_simulation(simulation, logger_of_simulation) # connects the logger to the simulation

# We don't need to visualize the simulation from the first iteration on
print("10 iterations without graphics")
simulation.run_n_timesteps(10)
print(simulation.settings.average_number_of_collisions_per_timestep)

print("Now with graphics")
# choose a visualization and initialize it
# Examples: C1Histogram(simulation, 800, 800)

# We want to combine several visualizations. Therefore we need to define a list of the ones, that we want.
used_of_visualizations = [C1Histogram(simulation, 1200, 800, 'phi'),
                           CNHistograms(simulation, 1200, 800, ['phi','q']),
                           CAverage(simulation, 1200, 800, 'phi'),
                           CAverage(simulation, 1200, 800, 'q')]
# Create a combination of these visualizations. You can iterate through the simulations by using left and right arrow
visualization =  CCombinationOfVisualizations(simulation, 1200, 800,
                                              used_of_visualizations)
visualization.init_display()
# modify the simulation that it can be visualized
add_visualization_to_simulation(simulation, visualization)

# Start the simulation
print("Start simulation")
print("Switch between the visualizations by using the arrow keys.")
print("The following settings are used:")
print(simulation)
simulation.run()