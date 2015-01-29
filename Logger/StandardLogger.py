__author__ = 'robert'

import pandas as pd
import os
import datetime
from Visualization.CVisualizationBaseClass import CVisualizationBaseClass
from Tools.usefulDecorators import CDecorator

def make_directory(name_of_directory):
  try:
    os.makedirs(name_of_directory)
  except OSError:
    print("Error while saving logging-files")

def compute_data_frame_of_group_of_individuals(group, list_of_relevant_attributes):
    """
    This method extracts all relevant attributes of a group of individuals and returns them as a data frame.
    :param group: group of individuals. For example: population.males
    :param list_of_relevant_attributes: list of attributes that should be saved. For example: ['q', 'phi']
    :return data frame of the group
    """
    data = {}
    for relevant_attribute in list_of_relevant_attributes:
        attribute_data = pd.Series([individual.__dict__[relevant_attribute] for individual in group])
        data[relevant_attribute] = attribute_data
    df_group = pd.DataFrame(data)
    return df_group

def compute_data_series_of_class(class_instance):
    """
    Iterates over all attributes of an instance of a class and converts them in pd.series format
    :param class_instance:
    :return:
    """
    keys = class_instance.__dict__.keys()
    values = [class_instance.__dict__[attribute] for attribute in keys]
    series = pd.Series(values, index=keys)
    return  series


class CLogger:
    def __init__(self, simulation, path="saved/"):
        self.simulation = simulation
        self.path = path # path were the logged data should be saved
        # create subdirectory and copy the settings of the simulation in a file
        self._save_settings_of_simulation()

    def _save_individuals_of_simulation(self, list_of_relevant_attributes, path_for_timestep):
        """
        Saves the population data
        :param simulation:
        :param list_of_relevant_attributes: list_of_relevant_attributes: list of attributes that should be saved. For example: ['q', 'phi']
        :param path_for_timestep: path to folder where the files should be saved
        :return:
        """
        # collect data from population
        data_male = compute_data_frame_of_group_of_individuals(self.simulation.population.males,
                                                               list_of_relevant_attributes)
        data_female = compute_data_frame_of_group_of_individuals(self.simulation.population.females,
                                                                 list_of_relevant_attributes)

        # save data as csv files
        current_step = str(self.simulation.settings.step_counter)
        data_male.to_csv(path_for_timestep+'males_'+current_step+'.csv')
        data_male.describe().to_csv(path_for_timestep+'males_overview_'+current_step+'.csv')
        data_female.to_csv(path_for_timestep+'females_'+current_step+'.csv')
        data_female.describe().to_csv(path_for_timestep+'females_overview_'+current_step+'.csv')

        print("Females after "+current_step+" iterations")
        print(data_female.describe())
        print("Males after "+current_step+" iterations")
        print(data_male.describe())


    def log_current_state_of_simulation(self):
        """
        Logs the current state of the simulation. This means the relevant attributes of the individuals in the
        population.
        :return:
        """
        list_of_relevant_attributes_of_individuals = ['q','phi']  # Which data of the population you want to save?
        # make an new directory which indicates the current iteration step
        path_for_timestep = self.path + str(self.simulation.settings.step_counter)+"/"
        make_directory(path_for_timestep)

        # save data about the individuals in the population
        self._save_individuals_of_simulation(list_of_relevant_attributes_of_individuals, path_for_timestep)

    def _save_settings_of_simulation(self):
        """
        Makes a subdirectory and updates the path. Further, it saves the settings file.
        :return:
        """
        self.path += str(datetime.datetime.now())+"/"
        make_directory(self.path)
        print("Start logging in "+self.path)
        settings = compute_data_series_of_class(self.simulation.settings)
        settings.to_csv(self.path+'settings.csv')

# --------------------------------------------------------------------------------------
"""
Interface for connecting to the simulation
"""
class CLoggerOfSimulation(CLogger, CVisualizationBaseClass):
    def __init__(self, simulation, periodicity_of_logging, path="./saved/"):
        CLogger.__init__(self, simulation, path)
        self.periodicity_of_logging = periodicity_of_logging
        self.counter = 0

    def loop(self):
        self.counter = (self.counter+1)%self.periodicity_of_logging
        if self.counter != 0:
            return
        self.log_current_state_of_simulation()

# ---------------------------------------------------------------------------------------
"""
The logger can be attached to the simulation class via this decorator.
"""
def add_logger_to_simulation(simulation, logger):
    """
    Adds chosen Logger to the simulation
    :param simulation - the simulation that that should be visualized
    :param Logger - chosen Logger for the simulation
    """
    # inserts the "logging-step" in the simulation
    simulation.perform_time_step = CDecorator(simulation.perform_time_step, [logger.loop])