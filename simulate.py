__author__ = 'RobertS'

from settings.settings import CSimulationData
from CSimulation import CSimulation
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import C1Histogram, CNHistograms, CAverage
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import C2DVisualizationOfSimulation
from Logger.StandardLogger import CLoggerOfSimulation, add_logger_to_simulation

# Parameters for visualisation and file creation (to include in GUI later on)
# ToDO: transfer these declaration in create_settings...
frequency_saving = 10000
width_window = 1200
height_window = 800
number_of_iterations = 500000

def simulate(settings_file, number_of_iterations, frequency_saving, width_window, height_window):
    """
    Run simulation with specified settings and number of iterations
    :param settings_file: path/filename of settings
    :param number_of_iterations: number of iterations
    :return:-
    """
    # Create simulation object
    settings = CSimulationData(settings_file)
    simulation = CSimulation(settings=settings)

    # initialize logger
    logger_of_simulation = CLoggerOfSimulation(simulation, frequency_saving)  # log every frequency_saving iteration
    add_logger_to_simulation(simulation, logger_of_simulation)  # connects the logger to the simulation

    # We want to combine several visualizations. Therefore we need to define a list of the ones, that we want.
    # In each visualization we pick the attributes of the individuals, which we like to see
    # ToDO: include following in gui settings stuff
    used_of_visualizations = [C1Histogram(simulation, width_window, height_window, 'phi'),
                          CNHistograms(simulation, width_window, height_window, ['phi','q']),
                          CAverage(simulation, width_window, height_window, 'phi'),
                          CAverage(simulation, width_window, height_window, 'q'),
                          C2DVisualizationOfSimulation(simulation, width_window, height_window)]

    # Create a combination of these visualizations. You can iterate through the simulations by using left and right arrow
    # ToDO: do not initialize the loger in the following class!
    visualization = CCombinationOfVisualizations(simulation, width_window, height_window, used_of_visualizations)

    visualization.init_display()
    # modify the simulation that it can be visualized
    add_visualization_to_simulation(simulation, visualization)

    # Start the simulation
    print("Start simulation")
    print("Switch between the visualizations by using the arrow keys.")
    print("The following settings are used:")
    print(simulation)
    simulation.run_n_timesteps(number_of_iterations)

list_of_simulation_settings = [('settings/settings.txt', number_of_iterations)]

for settings_file, number_of_iterations in list_of_simulation_settings:
    print("Run next simulation.")
    simulate(settings_file, number_of_iterations, frequency_saving, width_window, height_window)