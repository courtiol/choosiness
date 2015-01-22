import pygame
import math
import CIndividual

# ---------------------------------------No visualization-----------------------------------
from Visualization.VisualizationWithPygame.CVisualizationWithPygameBaseClass import CVisualizationWithPygameBaseClass


class CNoVisualizationOfSimulation(CVisualizationWithPygameBaseClass):
    def __init__(self, simulation):
        CVisualizationWithPygameBaseClass.__init__(self, simulation)
        self.colour_of_background = (255, 255, 255)

    # overwrite
    def init_screen(self):
        CVisualizationWithPygameBaseClass.init_screen(self)
        CVisualizationWithPygameBaseClass.screen.fill(self.colour_of_background)
        self.print_text_on_screen("No visualization selected", self.simulation.settings.width/2,
                                  self.simulation.settings.height/2-40, 30)
        self.print_text_on_screen("p - pause/run", self.simulation.settings.width/2,
                                  self.simulation.settings.height/2, 15)
        self.print_text_on_screen("v - next visualization", self.simulation.settings.width/2,
                                  self.simulation.settings.height/2+20, 15)
        self.print_text_on_screen("i - current time step", self.simulation.settings.width/2,
                                  self.simulation.settings.height/2+40, 15)
        pygame.display.flip()

    def __str__(self):
        return "No visualization"


# ---------------------------------------2D-Visualization-----------------------------------
class C2DVisualizationOfSimulation(CVisualizationWithPygameBaseClass):
    """
    The class encapsulates the visual output of the simulation. In order to that it makes use of pygame.
    It requires also a pointer to the instance of the simulation.
    """
    def __init__(self, simulation):
        CVisualizationWithPygameBaseClass.__init__(self, simulation)
        self.colour_of_environment = (255, 255, 255)
        self.colour_of_males = (0, 0, 255)  # blue
        self.thickness_latency = 2
        self.thickness_available = 0
        self.colour_of_females = (255, 0, 0)  # red
        self.colour_of_dead_individual = (0, 0, 0)  # black

    def draw_simulation(self):
        self._draw_environment()
        self._draw_population(self.simulation.population)
        pygame.display.flip()

    # display
    def _draw_environment(self):
        """
        Sets the background colour, shows the current number of collisions and the average collision number per
        step.
        :return:
        """
        CVisualizationWithPygameBaseClass.screen.fill(self.colour_of_environment)
        text = 'collisions: '+str(self.simulation.settings.collision_counter)
        text += " average: "+str(round(self.simulation.settings.average_number_of_collisions_per_timestep, 4))
        self.print_text_on_screen(text, self.simulation.settings.width/2, self.simulation.settings.height/2)

    def _draw_population(self, population):
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.get_current_females_size()) +
                                   ' females in red and '+str(self.simulation.population.get_current_males_size()) +
                                   ' males in blue')
        for p in population.males:
            self._draw_individual(p)
        for p in population.females:
            self._draw_individual(p)

    def _draw_individual(self, individual):
        """
        Each individual is represented by a circle. The colour of the circle depends on the gender and state of the
        individual.
        :param individual:individual which is drawn.
        :return:
        """
        # thickness = 2
        if individual.get_gender() == CIndividual.MALE:
            if individual.state == CIndividual.IN_LATENCY:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_latency)
            else:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_available)
            self.print_text_on_screen(str(round(individual.q, 4)), int(individual.x), int(individual.y), 15)
        else:
            if individual.state == CIndividual.IN_LATENCY:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_latency)
            else:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_available)
            self.print_text_on_screen(str(round(individual.phi, 4)), int(individual.x), int(individual.y), 15)

    def _show_information_about_selected_individual(self):
        if self.simulation.selected_individual is not None:
            print(str(self.simulation.selected_individual))

    def __str__(self):
        return "2D visualization"

# -------------------------Everything with matplotlib-------------------------------------------
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt
import numpy

# useful tutorial for matplotlib http://matplotlib.org/users/pyplot_tutorial.html


# ------------------4 histograms for choosiness/quality of males and females-----------------------
class CVisualizationWithMatplotlib(CVisualizationWithPygameBaseClass):
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
        # self.update_in_every_n_step = int(round(1/(1-self.simulation.settings.s)))
        self.update_in_every_n_step = 1 # ToDo: comment and take line up
        self.counter = 0

        # since there is only one plt object we need to count the number of instances of this class
        # ToDo: not clean what happens when for some instance one instance of a class is closed
        CVisualizationWithMatplotlib.number_of_class_instances += 1
        self.current_class_instance_number = CVisualizationWithMatplotlib.number_of_class_instances

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
class CHistogramVisualization(CVisualizationWithMatplotlib):
    """
    Histograms for the distribution of choosiness within the population
    """
    def __init__(self, simulation):
        CVisualizationWithMatplotlib.__init__(self, simulation)

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