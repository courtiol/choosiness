import Environment
import CPopulation
import CIndividual
from Visualization.VisualizationWithPygame import C2DVisualizationOfSimulation
from Visualization.CVisualizationBaseClass import CSimpleVisualization
from Visualization.VisualizationWithPygame import CDiagramVisualizationOfSimulation
from Visualization.VisualizationWithPygame import CNoVisualizationOfSimulation
from Visualization.VisualizationWithPygame import CTestVisualization
import pickle


#----------------------------CSimulation-------------------------------------
# Parameters of the model:
# survival rate s (in CSimulation)
# latency for males and females (in CSimulation)
#
# Factors that influence the encounter rate e
# size_of_population (in CSimulation)
# width & height of area (in CSimulation)
# size of individuals in the simulation (in Environment)
# speed of individuals in the simulation (in Environment)
# sex_ratio (in CSimulation)
# populationSize (in CSimulation)
#
#Parameters that influence the mutation:
#
#mutation_rate (in CSimulation)
#mutation_range (in CSimulation)


def rotate(array, n):
    """
    Rotates an array
    :param array:
    :param n:
    :return:rotated array
    """
    return array[n:] + array[:n]


class CSimulationSettings:
    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.size_of_population = 400
        self.sex_ratio = 0.5
        self.s = 0.999
        self.latency_males = 0.95
        self.latency_females = 0.95
        self.mutation_range = 0.05
        self.mutation_rate = 1

        self.collision_counter = 0
        self.step_counter = 1
        self.average_number_of_collisions_per_timestep = 0


class CSimulation:
    """
    In this class the parameters of the simulation are saved. The methods "run" and "performTimeStep" are the frame of
    the simulation.
    """
    def __init__(self):
        self.settings = CSimulationSettings()

        self.graphics_just_text = CSimpleVisualization(self)
        self.graphics_2D = C2DVisualizationOfSimulation(self)
        self.graphics_diagram = CDiagramVisualizationOfSimulation(self)
        self.visualizations_of_simulation = []
        #different possible visualizations of the simulation
        self.visualizations_of_simulation.append(self.graphics_2D)
        self.visualizations_of_simulation.append(self.graphics_diagram)
        self.visualizations_of_simulation.append(CNoVisualizationOfSimulation(self)) #no visualization
        self.visualizations_of_simulation.append(CTestVisualization(self))
        self.graphicsSimulation = self.visualizations_of_simulation[0]
        self.visualization_pointer = 0 #which visualization

        #set the environment in which the population is placed
        self.env = Environment.Environment(self.settings.width, self.settings.height)

        #create a population of males on random positions in that environment
        self.population = CPopulation.CPopulation(self.settings.size_of_population,self.settings.sex_ratio, self.settings.s, self.settings.latency_males, self.settings.latency_females, self.settings.mutation_range, self.settings.mutation_rate, self.env.place_item_in_environment)

        #information about the current simulation
        self.selected_individual = None
        self.running = True
        self.pause = False

        #display information
        self.graphicsSimulation.initDisplay()

    def next_visualization(self):
        self.visualization_pointer = (self.visualization_pointer+1)%len(self.visualizations_of_simulation)
        self.graphicsSimulation = self.visualizations_of_simulation[self.visualization_pointer]
        self.graphicsSimulation.init_screen()
        print(self.graphicsSimulation)

    def prior_visualization(self):
        self.visualization_pointer = (self.visualization_pointer-1)%len(self.visualizations_of_simulation)
        self.graphicsSimulation = self.visualizations_of_simulation[self.visualization_pointer]
        self.graphicsSimulation.init_screen()
        print(self.graphicsSimulation)

    def show_only_text(self):
        """
        Turnes off the visual effects of the simulation. Instead information is shown in the terminal.
        This serves for speeding up the simulation
        :return:
        """
        self.graphicsSimulation = self.graphics_just_text

    def show_2D_graphics(self):
        """
        Turnes the graphic on. The simulation runs slower in this mode
        :return:
        """
        self.graphicsSimulation = self.graphics_2D

    def show_diagrams_graphics(self):
        """
        Shows only diagrams
        :return:
        """
        self.graphicsSimulation = self.graphics_diagram

    def __performTimeStep(self):
        """
        Performes one iteration of the simulation
        :return:
        """
        self.population.update_states()
        self.env.update(self.population.males, self.population.females, self.collision_occured)
        self.graphicsSimulation.drawSimulation()
        self.settings.step_counter += 1

    def run(self):
        """
        Runs until the user terminates the simulation
        :return:
        """
        while self.running:
            if self.pause == False:
                self.__performTimeStep()
            self.graphicsSimulation.doInteractionWithUser()

    def run_n_timesteps(self, n):
        """
        run n timesteps
        :param n: number of timesteps
        :return:
        """
        for i in range(n):
            if self.running:
                if self.pause == False:
                    self.__performTimeStep()
                self.graphicsSimulation.doInteractionWithUser()
            

    def collision_occured(self, male, female):
        """
        The method is not called in this class. Instead it is given as a function pointer to the environment class
        in the method "performTimeStep". Every time a female individual crashes into a male this method is called.
        The method then checks for possible mating in the population.
        :param male: male individual (class CIndividual)
        :param female: female individual (class CIndividual)
        :return:
        """
        self.settings.collision_counter += 1
        self.settings.average_number_of_collisions_per_timestep = self.settings.collision_counter/self.settings.step_counter
        self.population.check_for_mating(male, female)

    def quit_simulation(self):
        self.running = False

    def pause_simulation(self):
        self.pause = False if self.pause else True

    def give_information_about_selected_individual(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        #do smth with it
    
    def selectIndividual(self,x,y):
        self.selected_individual = self.env.find_item(x, y, [self.population])

    def showInformationAboutPopulation(self):
        self.graphicsSimulation.printInformationAboutPopulation()

    def save(self):
        print("Save simulation")
        pickle.dump( self.population, open( "saved/population"+str(self.settings.step_counter)+".p", "wb" ) )
        pickle.dump( self.env, open( "saved/environment"+str(self.settings.step_counter)+".p", "wb" ) )
        pickle.dump( self.settings, open( "saved/settings"+str(self.settings.step_counter)+".p", "wb" ) )

    def __str__(self):
        z = "total population: "+str(self.settings.size_of_population)+"\n"
        z += "sex_ratio: "+str(self.settings.sex_ratio)+"\n"
        z += "s: "+str(self.settings.s)+"\n"
        z += "latency of males: "+str(self.settings.latency_males)+"\n"
        z += "latency of females: "+str(self.settings.latency_females)+"\n"
        z += "area: "+str(self.settings.width)+"times"+str(self.settings.height)+"\n"
        return z


