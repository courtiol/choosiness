__author__ = 'robert'

from CSimulation import CSimulation
from settings.settings import CSimulationSettings
from Logger.StandardLogger import CLoggerOfSimulation, add_logger_to_simulation

# constants:
frequency_logging = 100 # How often should be logged?
path_for_logging = "/data/fg2/schwieger/data_evolution_of_choosiness/inSoup/" # Where the logged data should be saved

def simulate(settings_file ,number_of_timesteps, frequency_logging, path_for_logging):
    # Create simulation object
    settings = CSimulationSettings(settings_file)
    simulation = CSimulation(settings=settings)

    # initialize logger
    logger_of_simulation = CLoggerOfSimulation(simulation=simulation, periodicity_of_logging=frequency_logging,
                                               path=path_for_logging)
    add_logger_to_simulation(simulation, logger_of_simulation) # connects the logger to the simulation

    # Run the simulation
    print("Simulation started.")
    print("Compute now "+str(number_of_timesteps)+" iterations")
    simulation.run_n_timesteps(number_of_timesteps)
    logger_of_simulation.log_current_state_of_simulation()
    print("Simulation is over.")

list_of_simulation_settings = [('settings/settings_comp_with_analytic1.txt', 1000),
                               ('settings/settings_comp_with_analytic2.txt', 1000),
                               ('settings/settings_comp_with_analytic3.txt', 1000),
                               ('settings/settings_comp_with_analytic4.txt', 1000)]

for settings_file, number_of_iterations in list_of_simulation_settings:
    simulate(settings_file=settings_file,number_of_timesteps=number_of_iterations, frequency_logging=frequency_logging,
         path_for_logging=path_for_logging)