from Tools.usefulDecorators import printAllParameters
import pickle
from settings.settings import CSimulationSettings


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
        self.env = self.settings.settings_dict['classType_of_environment'](
                    **self.settings.settings_dict['classType_settings']['classType_of_environment'])

        # create a population of males on random positions in that environment
        # ToDo: Consider better solutions instead of adding smth to the settings
        self.settings.settings_dict['classType_settings']['classType_of_population']['set_initial_position_in_the_environment'] = \
            self.env.place_item_in_environment

        self.population = self.settings.settings_dict['classType_of_population'](
            **self.settings.settings_dict['classType_settings']['classType_of_population'])

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
        try:
            self.population.update_states()
        except:
            print("The population could not be updated anymore.")
            print(self.population)
            self.running = False
            return
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
        print("The simulation is over.")

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
        z = str(self.settings)
        return z

    def save(self):
        print("Save simulation")
        pickle.dump(self.population, open("saved/population"+str(self.settings.step_counter)+".p", "wb"))
        pickle.dump(self.env, open("saved/environment"+str(self.settings.step_counter)+".p", "wb"))
        pickle.dump(self.settings, open("saved/settings"+str(self.settings.step_counter)+".p", "wb"))
