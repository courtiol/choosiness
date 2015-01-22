import pygame
import math
import CIndividual
from Visualization.CVisualizationBaseClass import CVisualizationBaseClass

"""
In this module you find different graphical representations of the simulation. Each representation of the simulation
should be derived from the the following abstract base class:
"""
# shared by all classes in this module
screen = None


# ---------------------------------------Visualization with pygame--------------------------
class CVisualizationWithPygame(CVisualizationBaseClass):
    def __init__(self, simulation):
        CVisualizationBaseClass.__init__(self, simulation)
        self.width_of_window = self.simulation.settings.width #ToDo: Assign better with parameters of constructor
        self.height_of_window = self.simulation.settings.height

    # overwrite
    def init_display(self):
        global screen
        screen = pygame.display.set_mode((self.width_of_window, self.height_of_window))
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.get_current_females_size()) +
                                   ' females in red and '+str(self.simulation.population.get_current_males_size()) +
                                   ' males in blue')
        pygame.init()

    def init_screen(self):
        global screen
        screen = pygame.display.set_mode((self.simulation.settings.width, self.simulation.settings.height))

    def do_interaction_with_user(self):
        """
        Encapsulates all possible user interactions. (Hot keys, click events)
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.simulation.quit_simulation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                self.simulation.select_individual(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.simulation.selected_individual = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.simulation.pause_simulation()
                elif event.key == pygame.K_c:
                    self._show_couples_array()
                elif event.key == pygame.K_s:
                    self.simulation.save()
                elif event.key == pygame.K_RIGHT:
                    self.simulation.next_visualization()
                elif event.key == pygame.K_LEFT:
                    self.simulation.prior_visualization()
                elif event.key == pygame.K_i:
                    print(str(self.simulation.settings.step_counter))
            if self.simulation.selected_individual:
                self.simulation.give_information_about_selected_individual()
                self._show_information_about_selected_individual()

    def print_text_on_screen(self, text, pos_x, pos_y, size=30, colour=(0, 0, 0)):
        large_text = pygame.font.Font('freesansbold.ttf', size)
        text_surface = large_text.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        screen.blit(text_surface, text_rect)

    def _show_couples_array(self):
        print("couples with length " + str(len(self.simulation.population.couples)) + "\n")
        for couple in self.simulation.population.couples:
            print(couple)

    def help(self):
        """
        Shows information about possible user interactions
        """
        text = "p - pause\n"
        text += "right arrow - next visualization\n"
        text += "left arrow - prior visualization\n"
        text += "s - save"
        text += "i - current time step\n"
        text += "left click on circle - information about individual in terminal"
        return text


# ---------------------------------------No visualization-----------------------------------
class CNoVisualizationOfSimulation(CVisualizationWithPygame):
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self, simulation)
        self.colour_of_background = (255, 255, 255)

    # overwrite
    def init_screen(self):
        CVisualizationWithPygame.init_screen(self)
        screen.fill(self.colour_of_background)
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
class C2DVisualizationOfSimulation(CVisualizationWithPygame):
    """
    The class encapsulates the visual output of the simulation. In order to that it makes use of pygame.
    It requires also a pointer to the instance of the simulation.
    """
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self, simulation)
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
        screen.fill(self.colour_of_environment)
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
                pygame.draw.circle(screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_latency)
            else:
                pygame.draw.circle(screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_available)
            self.print_text_on_screen(str(round(individual.q, 4)), int(individual.x), int(individual.y), 15)
        else:
            if individual.state == CIndividual.IN_LATENCY:
                pygame.draw.circle(screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_latency)
            else:
                pygame.draw.circle(screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_available)
            self.print_text_on_screen(str(round(individual.phi, 4)), int(individual.x), int(individual.y), 15)

    def _show_information_about_selected_individual(self):
        if self.simulation.selected_individual is not None:
            print(str(self.simulation.selected_individual))

    def __str__(self):
        return "2D visualization"


# -------------------------------------diagrams-----------------------------------
class CDiagramVisualizationOfSimulation(CVisualizationWithPygame):
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self, simulation)
        self.window_height = 800
        self.window_width = 800
        self.colour_of_background = (255, 255, 255)
        self.colour_of_female_bar = (255, 0, 0)
        self.colour_of_male_bar = (0, 0, 255)
        self.number_of_bars = 10.0
        self.width_of_bars = self.window_width/self.number_of_bars
        self.text_size = int(self.window_width/(8*self.number_of_bars))
        self.text_size_bar_label = int(self.text_size*1)
        self.maximal_height = round(self.window_height*0.6)

    def draw_simulation(self):
        screen.fill(self.colour_of_background)
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.get_current_females_size()) +
                                   ' females in red and '+str(self.simulation.population.get_current_males_size()) +
                                   ' males in blue')
        self.print_text_on_screen("Choosiness of females(red) and males(blue). ", 170, 10, self.text_size)
        self.print_text_on_screen(str(len(self.simulation.population.couples)) +
                                  " babies are in the waiting queue", 200, self.window_height-50, self.text_size)

        for i in range(int(self.number_of_bars)):
            text_x = i*self.width_of_bars+self.text_size+15
            text_y = self.window_height-750
            self.print_text_on_screen(str(i/self.number_of_bars)+"-"+str((i+1)/self.number_of_bars),
                                      text_x, text_y, self.text_size)
        self._draw_bars()
        pygame.display.flip()

    def _draw_bars(self):
        female_bars = self._count_choosiness_of_females()
        male_bars = self._count_choosiness_of_males()
        for i in range(int(self.number_of_bars)):
            female_bar_height = female_bars[i]/self.simulation.population.get_current_females_size()
            male_bar_height = male_bars[i]/self.simulation.population.get_current_males_size()
            (xf, yf, xf_offset, yf_offset) = self._compute_position_of_bar(female_bar_height, i)
            (xm, ym, xm_offset, ym_offset) = self._compute_position_of_bar(male_bar_height, i)

            pygame.draw.rect(screen, self.colour_of_female_bar, (xf, yf, xf_offset, yf_offset))
            if female_bar_height > 0:
                self.print_text_on_screen(str(round(female_bar_height*100))+"%", xf+13, yf+yf_offset+9,
                                          self.text_size_bar_label)
            pygame.draw.rect(screen, self.colour_of_male_bar, (xm-xf_offset, ym, xm_offset, ym_offset))
            if male_bar_height > 0:
                self.print_text_on_screen(str(round(male_bar_height*100))+"%", xm-xf_offset+13, ym+ym_offset+9,
                                          self.text_size_bar_label)

    def _compute_position_of_bar(self, bar_height, i):
        """
        Computes the coordinates of the bar
        :param bar_height: height of the bar
        :param i: x-position (value between 0 and self.number_of_bars)
        :return:rectangle
        """
        x = i*self.width_of_bars+self.text_size+15
        y = 90
        x_offset = int(self.width_of_bars*0.2)
        y_offset = self.maximal_height*bar_height
        return x, y, x_offset, y_offset

    def _count_choosiness_of_females(self):
        return self._count_choosiness(self.simulation.population.females)

    def _count_choosiness_of_males(self):
        return self._count_choosiness(self.simulation.population.males)

    def _count_choosiness(self, group_of_individuals):
        """
        Counts individuals according to their choosiness and saves the result in the array bars[]
        :return:bars
        """
        bars = []
        for i in range(int(self.number_of_bars)):
            bars.append(0)
        for ind in group_of_individuals:
            choosiness = math.floor(ind.phi*self.number_of_bars)
            bars[int(choosiness)] += 1
        return bars

    def __str__(self):
        return "Diagram visualization"

# -----------------------------------------------------------
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt
import numpy

# useful tutorial for matplotlib http://matplotlib.org/users/pyplot_tutorial.html


class CVisualizationWithMatplotlib(CVisualizationWithPygame):
    """
    Display statistics of the the simulation with 4 histograms (for female choosiness, male choosiness, female quality,
    male quality)
    """
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self, simulation)

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
        screen.blit(surf, (0, 0))

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

#-----------------------------------------------------------------
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