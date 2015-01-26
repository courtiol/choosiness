__author__ = 'robert'

import CSimulation
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Tools.timer import Timer

# Start simulation
simulation = CSimulation.CSimulation()

visualization = CCombinationOfVisualizations(simulation)
visualization.init_display()
add_visualization_to_simulation(simulation, visualization)

with Timer() as t:
    simulation.run_n_timesteps(10)
print("=> elapsed lpush: %s s" % t.secs)
