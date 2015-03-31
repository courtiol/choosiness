from settings import settings

__author__ = 'robert'

import CSimulation
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import C1Histogram, CNHistograms
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import C2DVisualizationOfSimulation

"""
Simple example for using the Simulation class together with any Visualization
"""

# Create simulation object
settings = settings.CSimulationData('Examples/example_settings_2D.txt')
simulation = CSimulation.CSimulation(settings)

# We don't need to visualize the simulation from the first iteration on
print("10 iterations without graphics")
simulation.run_n_timesteps(10)
print(simulation.settings.average_number_of_collisions_per_timestep)

print("Now with graphics")
# choose a visualization and initialize it
# Examples: C1Histogram(simulation, 800, 800)

# We want to combine several visualizations. Therefore we need to define a list of the ones, that we want.
width = 800
height = 800
used_of_visualizations = [C1Histogram(simulation, width, height, 'phi'),
                           CNHistograms(simulation, width, height, ['phi','q']),
                           C2DVisualizationOfSimulation(simulation, width, height)]
# Create a combination of these visualizations. You can iterate through the simulations by using left and right arrow
visualization =  CCombinationOfVisualizations(simulation, width, height,
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
