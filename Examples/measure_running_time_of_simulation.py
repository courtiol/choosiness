__author__ = 'robert'

import CSimulation
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
from Tools.timer import Timer

"""
Settings_Gui how to measure the time a certain number of iterations need
"""

# Start simulation
simulation = CSimulation.CSimulation()

with Timer() as t:
    simulation.run_n_timesteps(10)
print("=> elapsed lpush: %s s" % t.secs)
