__author__ = 'robert'

from CSimulation import CSimulation
from Logger.StandardLogger import CLoggerOfSimulation, add_logger_to_simulation

"""
This example demonstrates how the course of the simulation can be logged in csv-files. The output files will be saved
 in subfolders in the working directory. (Take care what is the working directory when specifying the running options)
"""
# Create simulation object
simulation = CSimulation()

# initialize logger
logger_of_simulation = CLoggerOfSimulation(simulation, 100)  # log every 100th iteration
add_logger_to_simulation(simulation, logger_of_simulation) # connects the logger to the simulation

# Run the simulation
print("Simulation started.")
print("Compute now 1000 iterations")
simulation.run_n_timesteps(1000)
logger_of_simulation.log_current_state_of_simulation()
print("Simulation is over.")