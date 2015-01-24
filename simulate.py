import CSimulation
import time
import pickle
from Visualization.decorateSimulation import add_visualization_to_simulation
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations

# Start simulation
simulation = CSimulation.CSimulation()
print(simulation.env)
visualization = CCombinationOfVisualizations(simulation)
visualization.init_display()
add_visualization_to_simulation(simulation, visualization)
simulation.run()

"""
population = pickle.load( open( "saved/population878.p", "rb" ) )
environment = pickle.load( open( "saved/environment878.p", "rb" ) )
settings = pickle.load( open( "saved/settings878.p", "rb" ) )
simulation.population = population
simulation.env = environment
simulation.settings = settings
"""



#print("Start simulation")
#print(simulation)
#simulation.run()
# simulation.run_n_timesteps(500)
# pickle.dump( simulation.population, open( "saved/population"+str(simulation.settings.step_counter)+".p", "wb" ) )
# pickle.dump( simulation.env, open( "saved/environment"+str(simulation.settings.step_counter)+".p", "wb" ) )
# pickle.dump( simulation.settings, open( "saved/settings"+str(simulation.settings.step_counter)+".p", "wb" ) )

"""
while True:
    print("Run 1000 timesteps")
    timeA = time.clock() #save processor time
    simulation.run_n_timesteps(1000)
    timeB = time.clock() #save processor time
    print("This took "+str(timeB-timeA)+" processor time")
    simulation.showInformationAboutPopulation()
    print("Turn graphics off")
    print("Run 1000 timesteps")
    simulation.show_only_text()
    timeC = time.clock() #save processor time
    simulation.run_n_timesteps(1000)
    timeD = time.clock() #save processor time
    print("This took "+str(timeD-timeC)+" processor time")
    print("Turn graphics on")
    simulation.show_diagrams_graphics()
"""
# End simulation
