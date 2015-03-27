__author__ = 'robert'

from settings.settings import CSimulationSettings
from CSimulation import CSimulation
import time
import pickle
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import C1Histogram, CNHistograms, CAverage
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import C2DVisualizationOfSimulation
from Logger.StandardLogger import CLoggerOfSimulation, add_logger_to_simulation

def simulate(settings_file, number_of_iterations):
    """
    Run simulation with specified settings and number of iterations
    :param settings_file: path/filename of settings
    :param number_of_iterations: number of iterations
    :return:-
    """
    # Create simulation object
    settings = CSimulationSettings(settings_file)
    simulation = CSimulation(settings=settings)

    # initialize logger
    logger_of_simulation = CLoggerOfSimulation(simulation, 10000)  # log every 10000th iteration
    add_logger_to_simulation(simulation, logger_of_simulation)  # connects the logger to the simulation

    # We want to combine several visualizations. Therefore we need to define a list of the ones, that we want.
    # In each visualization we pick the attributes of the individuals, which we like to see
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
    simulation.run_n_timesteps(number_of_iterations)

list_of_simulation_settings = [('settings/settings.txt', 500000)]

for settings_file, number_of_iterations in list_of_simulation_settings:
    print("Run next simulation.")
    simulate(settings_file, number_of_iterations)