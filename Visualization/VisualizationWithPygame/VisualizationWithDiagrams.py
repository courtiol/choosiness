__author__ = 'robert'

import pygame
import math
import CIndividual
from Visualization.VisualizationWithPygame.CVisualizationWithPygameBaseClass import CVisualizationWithPygameBaseClass

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt
import numpy

"""
Several visualizations using matplotlib. All visualizations are using histograms to display several attributes of
individuals in the population. These visualizations can be used for different environments and different individuals.
The only assumption made here is, that the population consists of females and males.
"""

# Useful: tutorial for matplotlib http://matplotlib.org/users/pyplot_tutorial.html

#  ---------------------------------------------General version---------------------------------------------------
class CHistograms(CVisualizationWithPygameBaseClass):
    """
    This class can be used as a base class for different visualizations which use histograms.
    """
    number_of_class_instances = 0
    def __init__(self, simulation, width_of_window, height_of_window):
        CVisualizationWithPygameBaseClass.__init__(self, simulation, width_of_window, height_of_window)

        x_size = int(self.width_of_window/100)
        y_size = int(self.height_of_window/100)
        self.fig = pylab.figure(figsize=[x_size, y_size], dpi=100)

        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.num_bins = 40

        # it is not necessary to update in every step the graphics
        # take expected life = average time of one generation as update rate
        s_males = self.simulation.settings.settings_dict['classType_settings']['classType_of_population']['classType_settings']['classType_of_male_individual']['survival_prob']
        s_females = self.simulation.settings.settings_dict['classType_settings']['classType_of_population']['classType_settings']['classType_of_female_individual']['survival_prob']
        max_s = max([s_males, s_females])
        self.update_in_every_n_step = int(round(1/(1-max_s)))
        self.update_in_every_n_step += 10
        self.counter = 0

        # since there is only one plt object we need to count the number of instances of this class
        # ToDo: not so good. What happens when for some instance one instance of a class is closed
        CHistograms.number_of_class_instances += 1
        self.current_class_instance_number = CHistograms.number_of_class_instances

    def draw_simulation(self):
        """
        This method should be overwritten
        """
        pass


    def _plot(self):
        self.canvas.draw()
        # prepare plot
        renderer = self.canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = self.canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")

        # plot it in pygame
        CVisualizationWithPygameBaseClass.screen.blit(surf, (0, 0))

        pygame.display.flip()

    def _compute_subfigure(self, data, colour, title, x_axis_label):
        # n, bins, patches = plt.hist(data, self.num_bins, normed=False, facecolor=colour, alpha=0.5)
        plt.hist(data, self.num_bins, normed=False, facecolor=colour, alpha=0.5)
        plt.xlabel(x_axis_label)
        plt.ylabel("number of individuals")
        plt.title(title)

    def _get_attribute_array_of_group_of_individuals(self, relevant_attribute, group_of_individuals):
        """
        This method returns an array of attributes of a group of individuals.
        """
        return [individual.__dict__[relevant_attribute] for individual in group_of_individuals]

    def __str__(self):
        return "Diagrams"


#---------------------1 histogram with female & male------------------------------------
class C1Histogram(CHistograms):
    """
    1 Histogram to compare the distribution of an attribute of the male individuals and female individuals
    of a population.
    """
    def __init__(self, simulation, width_of_window, height_of_window, relevant_attribute = 'phi'):
        CHistograms.__init__(self, simulation, width_of_window, height_of_window)
        self.relevant_attribute = relevant_attribute

    def draw_simulation(self):
        self.counter = (self.counter+1) % self.update_in_every_n_step
        if self.counter != 0:
            return

        # update window title
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.current_number_of_females) +
                                   ' females in red and '+str(self.simulation.population.current_number_of_males) +
                                   ' males in blue')
        # Get data to plot
        females_choosiness = self._get_attribute_array_of_group_of_individuals(relevant_attribute = self.relevant_attribute,
                                                         group_of_individuals = self.simulation.population.females)
        males_choosiness = self._get_attribute_array_of_group_of_individuals(relevant_attribute = self.relevant_attribute,
                                                         group_of_individuals = self.simulation.population.males)

        # assemble plot
        plt.figure(self.current_class_instance_number)
        self.canvas.figure.clf()  # clears the previous diagram
        plt.subplot(111) # 1 subplot
        intervals = numpy.arange(0, 1, 1/self.num_bins) # use numpy to create a list of intervals/bins
        plt.hist(females_choosiness, normed=False, facecolor='red', alpha=0.5, label='females',
                 bins=intervals)
        plt.hist(males_choosiness, normed=False, facecolor='blue', alpha=0.5, label='males',
                 bins=intervals)

        plt.legend()
        plt.xlabel(self.relevant_attribute+' (fixed bins)')
        plt.ylabel('number of individuals')
        plt.title('Distribution of '+self.relevant_attribute)

        self._plot()


# ------------------4 histograms for choosiness/quality of males and females-----------------------
class CNHistograms(CHistograms):
    """
    This class shows for each attribute one histogram for males and one histogram for females
    """
    def __init__(self, simulation, width_of_window, height_of_window, list_of_attributes=['phi','q']):
        CHistograms.__init__(self, simulation, width_of_window, height_of_window)
        self.list_of_attributes = list_of_attributes
        # We want to create a number of subplots depending on the number of attributes that should be displayed
        # Settings_Gui:plt.subplot(320) means the 3 rows and 2 columns of subplots
        # Here we calculate therefore the number of rows.
        self.number_of_subplots = len(self.list_of_attributes)*100

    def draw_simulation(self):
        self.counter = (self.counter+1) % self.update_in_every_n_step
        if self.counter != 0:
            return

        # update window title
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.current_number_of_females) +
                                   ' females in red and '+str(self.simulation.population.current_number_of_males) +
                                   ' males in blue')

        # Get data to plot and assemble plot
        plot_position = self.number_of_subplots+20  # +20 means one column for males, one column for females
        plt.figure(self.current_class_instance_number)
        self.canvas.figure.clf()  # clears the previous diagram

        # Now we iterate over all attributes and create for each one a male and female plot
        for attribute in self.list_of_attributes:
            females_attribute = self._get_attribute_array_of_group_of_individuals(relevant_attribute = attribute,
                                                         group_of_individuals = self.simulation.population.females)
            males_attribute = self._get_attribute_array_of_group_of_individuals(relevant_attribute = attribute,
                                                         group_of_individuals = self.simulation.population.males)
            # females:
            plot_position += 1  # choose next "sub"-window for plotting
            plt.subplot(plot_position)
            self._compute_subfigure(females_attribute, 'red', attribute+' of Females', attribute+' (dynamic bins)')

            # males:
            plot_position += 1  # choose next "sub"-window for plotting
            plt.subplot(plot_position)
            self._compute_subfigure(males_attribute, 'blue', attribute+' of Males', attribute+' (dynamic bins)')

        self._plot()


class CAverage(CHistograms):
    def __init__(self, simulation, width_of_window, height_of_window, relevant_attribute = 'phi'):
        CHistograms.__init__(self, simulation, width_of_window, height_of_window)
        self.relevant_attribute = relevant_attribute
        self.female_averages = []
        self.male_averages = []
        self.corresponding_timesteps = []
    def draw_simulation(self):
        self.counter = (self.counter+1) % self.update_in_every_n_step
        if self.counter != 0:
            return

        self.getAverageOfAttribute()

        # update window title
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.current_number_of_females) +
                                   ' females in red and '+str(self.simulation.population.current_number_of_males) +
                                   ' males in blue')

        # assemble plot
        plt.figure(self.current_class_instance_number)
        self.canvas.figure.clf()  # clears the previous diagram
        plt.subplot(111) # 1 subplot
        plt.plot(self.corresponding_timesteps, self.male_averages, color='blue')
        plt.plot(self.corresponding_timesteps, self.female_averages, color='red')

        plt.xlabel('iterations of the simulation')
        plt.ylabel('average value of '+self.relevant_attribute)
        plt.title('average value of '+self.relevant_attribute+' for males (blue) and females (red)')
        self._plot()

    def getAverageOfAttribute(self):
        # save timestep
        self.corresponding_timesteps.append(self.simulation.settings.step_counter)
        # save average of female attribute
        female_attribute = self._get_attribute_array_of_group_of_individuals(self.relevant_attribute,
                                                                             self.simulation.population.females)
        self.female_averages.append(numpy.mean(female_attribute))
        # save average of male attribute
        male_attribute = self._get_attribute_array_of_group_of_individuals(self.relevant_attribute,
                                                                             self.simulation.population.males)
        self.male_averages.append(numpy.mean(male_attribute))
