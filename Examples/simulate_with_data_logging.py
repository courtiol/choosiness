__author__ = 'robert'

from CSimulation import CSimulation
from Logger.StandardLogger import CLoggerOfSimulation, add_logger_to_simulation


# Start simulation
simulation = CSimulation()

# initialize logger
logger_of_simulation = CLoggerOfSimulation(simulation, 100)  # log every 100th iteration
add_logger_to_simulation(simulation, logger_of_simulation)

# Run the simulation
print("Simulation started.")
print("Compute now 10 iterations")
simulation.run_n_timesteps(10)
logger_of_simulation.log_current_state_of_simulation()
print("simulation is over")