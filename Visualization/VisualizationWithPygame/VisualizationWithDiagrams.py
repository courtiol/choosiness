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
Several visualizations using matplotlib. These visualizations can be used also for simulations which use different
kind of environments.
"""

# useful tutorial for matplotlib http://matplotlib.org/users/pyplot_tutorial.html
# ------------------4 histograms for choosiness/quality of males and females-----------------------
class CVisualization4Histograms(CVisualizationWithPygameBaseClass):
    """
    Display statistics of the the simulation with 4 histograms (for female choosiness, male choosiness, female quality,
    male quality)
    """
    number_of_class_instances = 0
    def __init__(self, simulation):
        CVisualizationWithPygameBaseClass.__init__(self, simulation)

        x_size = int(self.width_of_window/100)
        y_size = int(self.height_of_window/100)
        self.fig = pylab.figure(figsize=[x_size, y_size], dpi=100)

        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.num_bins = 20

        # it is not necessary to update in every step the graphics
        # take expected life = average time of one generation as update rate
        max_s = max([self.simulation.settings.s_males, self.simulation.settings.s_females])
        self.update_in_every_n_step = int(round(1/(1-max_s)))
        self.counter = 0

        # since there is only one plt object we need to count the number of instances of this class
        # ToDo: not clean what happens when for some instance one instance of a class is closed
        CVisualization4Histograms.number_of_class_instances += 1
        self.current_class_instance_number = CVisualization4Histograms.number_of_class_instances

    def draw_simulation(self):
        if self.counter != 0:
            return
        self.counter = (self.counter+1) % self.update_in_every_n_step

        # Get data to plot
        females_choosiness = self._get_female_choosiness_array()
        males_choosiness = self._get_male_choosiness_array()
        females_quality = self._get_female_quality_array()
        males_quality = self._get_male_quality_array()

        # assemble plot
        plt.figure(self.current_class_instance_number)
        self.canvas.figure.clf()  # clears the previous diagram
        plt.subplot(221) # first subplot of 2×2 subplots
        self._compute_subfigure(females_choosiness, 'red', 'Choosiness of Females', 'choosiness (dynamic bins)')
        plt.subplot(222) # second subplot of 2×2 subplots
        self._compute_subfigure(males_choosiness, 'blue', 'Choosiness of Males', 'choosiness (dynamic bins)')
        plt.subplot(223) # third subplot of 2×2 subplots
        self._compute_subfigure(females_quality, 'red', 'Quality of Females', 'quality (dynamic bins)')
        plt.subplot(224) # fourth subplot of 2×2 subplots
        self._compute_subfigure(males_quality, 'blue', 'Quality of Males', 'quality (dynamic bins)')

        self._plot()


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

    def _get_male_choosiness_array(self):
        return [ind.phi for ind in self.simulation.population.males]

    def _get_female_choosiness_array(self):
        return [ind.phi for ind in self.simulation.population.females]

    def _get_female_quality_array(self):
        return [ind.q for ind in self.simulation.population.females]

    def _get_male_quality_array(self):
        return [ind.q for ind in self.simulation.population.males]

    def __str__(self):
        return "Diagrams"


#---------------------1 histogram with female & male choosiness------------------------------------
class C1HistogramVisualization(CVisualization4Histograms):
    """
    Histograms for the distribution of choosiness within the population
    """
    def __init__(self, simulation):
        CVisualization4Histograms.__init__(self, simulation)

    def draw_simulation(self):
        if self.counter != 0:
            return
        self.counter = (self.counter+1) % self.update_in_every_n_step

        # Get data to plot
        females_choosiness = self._get_female_choosiness_array()
        males_choosiness = self._get_male_choosiness_array()

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
        plt.xlabel('choosiness (fixed bins)')
        plt.ylabel('number of individuals')
        plt.title('Distribution of Choosiness')

        self._plot()