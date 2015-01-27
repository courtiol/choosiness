__author__ = 'robert'

import CSimulation
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Tools.usefulDecorators import measure_percentage_of_time

"""
Template for measuring running times.
Set @measure_percentage_of_time from the package Tools in front of functions to measure their running time.
"""

# Start simulation
simulation = CSimulation.CSimulation()
# Run the simulation and measure the time
simulation.run_n_timesteps(30)

#Print the results
measure_percentage_of_time.print_results()
print("col: "+str(simulation.settings.collision_counter))
print("average: "+str(simulation.settings.average_number_of_collisions_per_timestep))