import Environments.Environment2D
import CPopulation
from Environments import Environment2DDelaunay, Environment2D,  EnvironmentL
from Visualization.CVisualizationBaseClass import CSimpleVisualization
from Tools.usefulDecorators import printAllParameters
from Visualization.VisualizationWithPygame.VisualizationCombination import CCombinationOfVisualizations
import pickle


# ----------------------------CSimulation-------------------------------------
class CSimulationSettings:
    """
    Stores the settings of the simulation
    """
    def __init__(self):
        # parameters regarding the population and individuals
        self.size_of_population = 100
        self.sex_ratio = 0.5
        self.s_males = 0.999
        self.s_females = 0.999
        self.latency_males = 0.95
        self.latency_females = 0.95
        self.mutation_range = 0.05
        self.mutation_rate = 1
        self.a = 1/2  # factor that influences the weighted average of the qualities of the offspring
        self.type_of_average = CPopulation.ARITHMETIC_MEAN  # choose between ARITHMETIC_MEAN and GEOMETRIC_MEAN
        self.maximal_number_of_saved_couples = 1000

        # parameters for environment
        # The following environments can be chosen:
        # Environment2D.Environment2D
        # Environment2D.Environment2DNoBounce
        # Environment2DDelaunay.Environment2DDelaunay
        # EnvironmentL.EnvironmentL
        self.type_of_environment =  Environment2DDelaunay.Environment2DDelaunay
        self.width = 800
        self.height = 800
        self.size_of_individuals = 6
        self.speed_of_individuals = 7

        self.collision_counter = 0
        self.step_counter = 1
        self.average_number_of_collisions_per_timestep = 0

    @printAllParameters
    def __str__(self):
        return ""


class CSimulation:
    """
    In this class the parameters of the simulation are saved. The methods "run" and "performTimeStep" are the frame of
    the simulation.
    """
    def __init__(self, settings=None):
        if settings is None:
            self.settings = CSimulationSettings()
        else:
            self.settings = settings
        # set the environment in which the population is placed
        self.env = self.settings.type_of_environment(width=self.settings.width, height=self.settings.height,
                                                     itemSize=self.settings.size_of_individuals,
                                                     itemSpeed=self.settings.speed_of_individuals)
        # create a population of males on random positions in that environment
        self.population = CPopulation.CPopulation(population_size=self.settings.size_of_population,
                                                  sex_ratio=self.settings.sex_ratio,
                                                  s_females=self.settings.s_females, s_males=self.settings.s_males,
                                                  latency_males=self.settings.latency_males,
                                                  latency_females=self.settings.latency_females,
                                                  mutation_range=self.settings.mutation_range,
                                                  mutation_rate=self.settings.mutation_rate,
                                                  set_initial_position_in_the_environment=self.env.place_item_in_environment,
                                                  a=self.settings.a, type_of_average=self.settings.type_of_average,
                                                  maximal_number_of_saved_couples=self.settings.maximal_number_of_saved_couples)

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
        for _ in range(n):
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
        z += "s_males: "+str(self.settings.s_males)+"\n"
        z += "s_females: "+str(self.settings.s_females)+"\n"
        z += "latency of males: "+str(self.settings.latency_males)+"\n"
        z += "latency of females: "+str(self.settings.latency_females)+"\n"
        z += "area: "+str(self.settings.width)+"times"+str(self.settings.height)+"\n"
        return z

    def save(self):
        print("Save simulation")
        pickle.dump(self.population, open("saved/population"+str(self.settings.step_counter)+".p", "wb"))
        pickle.dump(self.env, open("saved/environment"+str(self.settings.step_counter)+".p", "wb"))
        pickle.dump(self.settings, open("saved/settings"+str(self.settings.step_counter)+".p", "wb"))
