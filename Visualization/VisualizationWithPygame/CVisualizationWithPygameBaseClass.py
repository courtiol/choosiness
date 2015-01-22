__author__ = 'robert'

import pygame
#import math
import CIndividual
from Visualization.CVisualizationBaseClass import CVisualizationBaseClass

"""
In this module you find different graphical representations of the simulation. Each representation of the simulation
should be derived from the the following abstract base class:
"""

# ---------------------------------------Visualization with pygame--------------------------
class CVisualizationWithPygameBaseClass(CVisualizationBaseClass):

    # There is only one window possible in pygame. Therefore all instances of this class share the same instance of
    # screen.
    screen = None

    def __init__(self, simulation):
        CVisualizationBaseClass.__init__(self, simulation)
        self.width_of_window = self.simulation.settings.width #ToDo: Assign better with parameters of constructor
        self.height_of_window = self.simulation.settings.height

    # overwrite
    def init_display(self):
        #global screen
        CVisualizationWithPygameBaseClass.screen = pygame.display.set_mode((self.width_of_window, self.height_of_window))
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.get_current_females_size()) +
                                   ' females in red and '+str(self.simulation.population.get_current_males_size()) +
                                   ' males in blue')
        pygame.init()

    def init_screen(self):
        #global screen
        CVisualizationWithPygameBaseClass.screen = pygame.display.set_mode((self.simulation.settings.width, self.simulation.settings.height))

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
        CVisualizationWithPygameBaseClass.screen.blit(text_surface, text_rect)

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

