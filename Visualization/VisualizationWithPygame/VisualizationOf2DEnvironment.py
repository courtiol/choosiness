import pygame
import math
import CIndividual
from Visualization.VisualizationWithPygame.CVisualizationWithPygameBaseClass import CVisualizationWithPygameBaseClass
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import CVisualization4Histograms

"""
Visualization of a 2D-Environment. Individuals are represented as circles. States and gender of the individuals are
represented as colours.
"""
# ---------------------------------------No visualization-----------------------------------
class CNoVisualizationOfSimulation(CVisualizationWithPygameBaseClass):
    """
    No visualization at all. Just information about shortcuts on the screen.
    """
    def __init__(self, simulation):
        CVisualizationWithPygameBaseClass.__init__(self, simulation)
        self.colour_of_background = (255, 255, 255)
        self.selected_individual = None

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


    def give_information_about_selected_individual(self):
        if self.selected_individual is not None:
            print(str(self.selected_individual))

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
        self.selected_individual = None

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
        if individual.gender == CIndividual.MALE:
            if individual.state == CIndividual.IN_LATENCY:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.itemSize, self.thickness_latency)
            else:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.itemSize, self.thickness_available)
            self.print_text_on_screen(str(round(individual.q, 4)), int(individual.x), int(individual.y), 15)
        else:
            if individual.state == CIndividual.IN_LATENCY:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.itemSize, self.thickness_latency)
            else:
                pygame.draw.circle(CVisualizationWithPygameBaseClass.screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.itemSize, self.thickness_available)
            self.print_text_on_screen(str(round(individual.phi, 4)), int(individual.x), int(individual.y), 15)

    def give_information_about_selected_individual(self):
        """
        shows __str of individual
        :return:
        """
        if self.selected_individual is not None:
            print(str(self.selected_individual))

    def select_individual(self, x, y):
        """
        Searches in the environment for an individual with coordinates (x,y) and selects this individual
        :param x: x-coordinate
        :param y: y-coordinate
        :return:-
        """
        self.selected_individual = self.simulation.env.find_item(x, y, [self.simulation.population])

    def __str__(self):
        return "2D visualization"

    def handle_user_event(self, event):
        """
        overwritten method from the super class
        :param event: user event
        :return:
        """
        #add user events for selecting individuals in the environment
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            self.select_individual(mouse_x, mouse_y)
            if self.selected_individual is not None:
                self.give_information_about_selected_individual()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected_individual = None
        #deal with other possible user events in the super class
        CVisualizationWithPygameBaseClass.handle_user_event(self,event)
