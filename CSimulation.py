import Environment
import CPopulation
from Visualization.CVisualizationBaseClass import CSimpleVisualization

from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
import pickle



# ----------------------------CSimulation-------------------------------------

class CSimulationSettings:
    """
    Stores the settings of the simulation
    """
    def __init__(self):
        #parameters regarding the population and individuals
        self.size_of_population = 400
        self.sex_ratio = 0.5
        self.s = 0.999
        self.latency_males = 0.95
        self.latency_females = 0.95
        self.mutation_range = 0.05
        self.mutation_rate = 1

        #parameters for environment
        self.width = 800
        self.height = 800
        self.size_of_individuals = 5
        self.speed_of_individuals = 7

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
        # set the environment in which the population is placed
        self.env = Environment.Environment(width=self.settings.width, height=self.settings.height,
                                           itemSize=self.settings.size_of_individuals,
                                           itemSpeed=self.settings.speed_of_individuals)
        # create a population of males on random positions in that environment
        self.population = CPopulation.CPopulation(self.settings.size_of_population, self.settings.sex_ratio,
                                                  self.settings.s, self.settings.latency_males,
                                                  self.settings.latency_females, self.settings.mutation_range,
                                                  self.settings.mutation_rate, self.env.place_item_in_environment)

        # information about the current simulation
        self.selected_individual = None
        self.running = True
        self.pause = False

        # display information
        # self.graphicsSimulation.init_display()

    def perform_time_step(self):
        """
        Performes one iteration of the simulation
        :return:
        """
        self.population.update_states()
        self.env.update(self.population.males, self.population.females, self.collision_occured)
        self.settings.step_counter += 1

    def run(self):
        """
        Runs until the user terminates the simulation
        :return:
        """
        while self.running:
            if not self.pause:
                self.perform_time_step()
            self.hook_for_user_control()

    def run_n_timesteps(self, n):
        """
        run n timesteps
        :param n: number of timesteps
        :return:
        """
        for i in range(n):
            if self.running:
                if not self.pause:
                    self.perform_time_step()
                self.hook_for_user_control()

    def hook_for_user_control(self):
        """
        This is a hook for decorators, that want to interact with users
        """
        pass
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
        self.settings.average_number_of_collisions_per_timestep = \
            self.settings.collision_counter/self.settings.step_counter
        self.population.check_for_mating(male, female)

    def quit_simulation(self):
        self.running = False

    def pause_simulation(self):
        self.pause = False if self.pause else True

    def __str__(self):
        z = "total population: "+str(self.settings.size_of_population)+"\n"
        z += "sex_ratio: "+str(self.settings.sex_ratio)+"\n"
        z += "s: "+str(self.settings.s)+"\n"
        z += "latency of males: "+str(self.settings.latency_males)+"\n"
        z += "latency of females: "+str(self.settings.latency_females)+"\n"
        z += "area: "+str(self.settings.width)+"times"+str(self.settings.height)+"\n"
        return z

    def save(self):
        print("Save simulation")
        pickle.dump(self.population, open("saved/population"+str(self.settings.step_counter)+".p", "wb"))
        pickle.dump(self.env, open("saved/environment"+str(self.settings.step_counter)+".p", "wb"))
        pickle.dump(self.settings, open("saved/settings"+str(self.settings.step_counter)+".p", "wb"))
