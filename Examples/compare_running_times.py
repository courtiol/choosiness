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
print("Create simulation: ")
print(simulation.settings)
# Run the simulation and measure the time
number_of_iterations = 100
print("Test running time with "+str(number_of_iterations)+" iterations.")
simulation.run_n_timesteps(number_of_iterations)

#Print the results
measure_percentage_of_time.print_results()
print("number of collisions: "+str(simulation.settings.collision_counter))
print("average per timestep: "+str(simulation.settings.average_number_of_collisions_per_timestep))