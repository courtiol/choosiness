import pygame
import math
import CIndividual
from Visualization.VisualizationWithPygame.CVisualizationWithPygameBaseClass import CVisualizationWithPygameBaseClass
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import CVisualizationWithMatplotlib

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