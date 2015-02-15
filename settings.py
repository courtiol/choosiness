import CIndividual
import CPopulation
from Environments import Environment2DFaster, Environment2D,  EnvironmentSoup
from Tools.usefulDecorators import printAllParameters
import json
import jsonpickle

__author__ = 'robert'

"""
The settings of the simulation are saved as a dictionary. The keys of the dictionary should correspond to the parameter-
names of the chosen classes of the environment, individual, population and chromosomes.

Examples:
1) The following settings choose for the population the class CPopulation.CPopulationImmediateFlush, for the environment
the class EnvironmentSoup.EnvironmentSoup

        self.settings_dict = {}
        self.settings_dict['classType_of_population'] = CPopulation.CPopulationImmediateFlush
        self.settings_dict['population_settings'] = {}
        self.settings_dict['population_settings']['population_size'] = 5000
        self.settings_dict['population_settings']['maximal_number_of_saved_couples'] = \
            2*self.settings_dict['population_settings']['population_size']
        self.settings_dict['population_settings']['sex_ratio'] = 0.5
        self.settings_dict['population_settings']['type_of_average'] = CPopulation.ARITHMETIC_MEAN
        self.settings_dict['population_settings']['a'] = 0.5
        self.settings_dict['population_settings']['male_individual_settings'] = {}
        self.settings_dict['population_settings']['male_individual_settings']['gender'] = CIndividual.MALE
        self.settings_dict['population_settings']['male_individual_settings']['survival_prob'] = 0.99
        self.settings_dict['population_settings']['male_individual_settings']['latency'] = 0.98
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings'] = {}
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings']['mutation_range'] = 0.01
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings']['mutation_rate'] = 0.01
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings']['loci']\
            = [(0, False), (0.5, True), (0, False), (0.5, True)] # initial_chromosome

        self.settings_dict['population_settings']['female_individual_settings'] = {}
        self.settings_dict['population_settings']['female_individual_settings']['gender'] = CIndividual.FEMALE
        self.settings_dict['population_settings']['female_individual_settings']['survival_prob'] = 0.99
        self.settings_dict['population_settings']['female_individual_settings']['latency'] = 0.99
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings'] = {}
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings']['mutation_range'] = 0.01
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings']['mutation_rate'] = 0.01
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings']['loci']\
            = [(0, False), (0.5, True), (0, False), (0.5, True)] # initial_chromosome

        self.settings_dict['classType_of_environment'] = EnvironmentSoup.EnvironmentSoup
        self.settings_dict['environment_settings'] = {}
        self.settings_dict['environment_settings']['e'] = 0.99

2) The following settings choose for the environment the class Environment2DDelaunay.Environment2DDelaunay

        # insert population settings from up

        # You can choose with the same settings also Environment2D.Environment2D or Environment2D.Environment2DNoBounce
        self.settings_dict['classType_of_environment'] = Environment2D.Environment2D
        self.settings_dict['environment_settings'] = {}
        self.settings_dict['environment_settings']['width'] = 800
        self.settings_dict['environment_settings']['height'] = 800
        self.settings_dict['environment_settings']['itemSize'] = 6 # size_of_individuals
        self.settings_dict['environment_settings']['itemSpeed'] = 7 # speed_of_individuals
"""


class CSimulationSettings:
    """
    Stores the settings of the simulation
    """
    def __init__(self):
        # parameters regarding the population and individuals
        """
        self.size_of_population = 5000
        self.sex_ratio = 0.5
        self.s_males = 0.99
        self.s_females = 0.99
        self.latency_males = 0.98
        self.latency_females = 0.99
        self.mutation_range = 0.01
        self.mutation_rate = 0.01
        self.initial_chromosome = [(0, False), (0.5, True), (0, False), (0.5, True)]
        # + initial values of chromosomes in class CChromosome: Currently [(0, False), (0.0, True), (0, False), (0.0, True)]
        self.a = 1/2  # factor that influences the weighted average of the qualities of the offspring
        self.type_of_average = CPopulation.ARITHMETIC_MEAN  # choose between ARITHMETIC_MEAN and GEOMETRIC_MEAN
        self.maximal_number_of_saved_couples = 10000

        # parameters for environment
        # The following environments can be chosen:
        # Environment2D.Environment2D
        # Environment2D.Environment2DNoBounce
        # Environment2DDelaunay.Environment2DDelaunay
        self.type_of_environment =  EnvironmentSoup.EnvironmentSoup
        if self.type_of_environment is not EnvironmentSoup.EnvironmentSoup:
            self.width = 800
            self.height = 800
            self.size_of_individuals = 6
            self.speed_of_individuals = 7
        elif self.type_of_environment is EnvironmentSoup.EnvironmentSoup:
            self.e = 0.99
        """


        self.collision_counter = 0
        self.step_counter = 1
        self.average_number_of_collisions_per_timestep = 0

        self.settings_dict = {}
        self.settings_dict['classType_of_population'] = CPopulation.CPopulationImmediateFlush
        self.settings_dict['population_settings'] = {}
        self.settings_dict['population_settings']['population_size'] = 100
        self.settings_dict['population_settings']['maximal_number_of_saved_couples'] = \
            2*self.settings_dict['population_settings']['population_size']
        self.settings_dict['population_settings']['sex_ratio'] = 0.5
        self.settings_dict['population_settings']['type_of_average'] = CPopulation.ARITHMETIC_MEAN
        self.settings_dict['population_settings']['a'] = 0.5
        self.settings_dict['population_settings']['male_individual_settings'] = {}
        self.settings_dict['population_settings']['male_individual_settings']['gender'] = CIndividual.MALE
        self.settings_dict['population_settings']['male_individual_settings']['survival_prob'] = 0.99
        self.settings_dict['population_settings']['male_individual_settings']['latency'] = 0.98
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings'] = {}
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings']['mutation_range'] = 0.01
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings']['mutation_rate'] = 0.01
        self.settings_dict['population_settings']['male_individual_settings']['chromosome_settings']['loci']\
            = [(0, False), (0.5, True), (0, False), (0.5, True)] # initial_chromosome

        self.settings_dict['population_settings']['female_individual_settings'] = {}
        self.settings_dict['population_settings']['female_individual_settings']['gender'] = CIndividual.FEMALE
        self.settings_dict['population_settings']['female_individual_settings']['survival_prob'] = 0.99
        self.settings_dict['population_settings']['female_individual_settings']['latency'] = 0.99
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings'] = {}
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings']['mutation_range'] = 0.01
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings']['mutation_rate'] = 0.01
        self.settings_dict['population_settings']['female_individual_settings']['chromosome_settings']['loci']\
            = [(0, False), (0.5, True), (0, False), (0.5, True)] # initial_chromosome

        self.settings_dict['classType_of_environment'] = Environment2DFaster.Environment2DDelaunay
        self.settings_dict['environment_settings'] = {}
        self.settings_dict['environment_settings']['width'] = 800
        self.settings_dict['environment_settings']['height'] = 800
        self.settings_dict['environment_settings']['itemSize'] = 6 # size_of_individuals
        self.settings_dict['environment_settings']['itemSpeed'] = 7 # speed_of_individuals

        # ToDo: Decide what looks better
        """
        self.dict['population_settings'] = {'size_of_population': 5000,
                                   'sex_ratio': 0.5,
                                   'type_of_average': CPopulation.ARITHMETIC_MEAN,
                                   'maximal_number_of_saved_couples': 10000,
                                   'a':0.5,
                                   'male_individual_settings':
                                       {
                                        'survival_prob': 0.99,
                                        'latency': 0.98,
                                        'chromosome_settings':
                                            {
                                               'mutation_range': 0.01,
                                               'mutation_rate': 0.01,
                                               'initial_chromosome': [(0, False), (0.5, True), (0, False), (0.5, True)]
                                            }
                                       },
                                   'female_individual_settings':
                                       {
                                         'survival_prob': 0.99,
                                         'latency': 0.99,
                                         'chromosome_settings':
                                            {
                                               'mutation_range': 0.01,
                                               'mutation_rate': 0.01,
                                               'initial_chromosome': [(0, False), (0.5, True), (0, False), (0.5, True)]
                                            }
                                       }
                                   }
        self.dict['type_of_environment'] = EnvironmentSoup.EnvironmentSoup
        self.dict['environment_settings'] = {'e':0.99}
        """

    @printAllParameters
    def __str__(self):
        return ""

    def save_settings_to_file(self, filename):
        """
        Converts the settings into json-format and saves it in the given file
        :param filename: 'relative path/filename'
        """
        settings_as_json = jsonpickle.encode(self.settings_dict)
        f = open(filename, 'w')
        f.write(settings_as_json)
        print("settings saved to "+filename)

    def load_settings_from_file(self, filename):
        f = open(filename)
        json_str = f.read()
        self.settings_dict = jsonpickle.decode(json_str)
        print("settings loaded from "+filename)