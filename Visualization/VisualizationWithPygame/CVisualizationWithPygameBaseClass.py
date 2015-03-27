__author__ = 'robert'

import pygame
import CIndividual
from Visualization.CVisualizationBaseClass import CVisualizationBaseClass

"""
In this module all visualization using pyGame are stored. You find here also the base class which deals with standard
user interactions and the initialization of pygame. Since in pyGame it is only possible to have one window open in the
same time we use a static parameter screen which circumvents the problems that several visualizations are used in the
same time.
"""


# ---------------------------------------Visualization with pygame--------------------------
class CVisualizationWithPygameBaseClass(CVisualizationBaseClass):

    # There is only one window possible in pygame. Therefore all instances of this class share the same instance of
    # screen.
    screen = None

    def __init__(self, simulation, width_of_window, height_of_window):
        CVisualizationBaseClass.__init__(self, simulation)
        self.width_of_window = width_of_window
        self.height_of_window = height_of_window

    # overwrite
    def init_display(self):
        CVisualizationWithPygameBaseClass.screen = pygame.display.set_mode((self.width_of_window,
                                                                            self.height_of_window))
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.current_number_of_females) +
                                   ' females in red and '+str(self.simulation.population.current_number_of_males) +
                                   ' males in blue')
        pygame.init()

    def init_screen(self):
        CVisualizationWithPygameBaseClass.screen = pygame.display.set_mode((self.width_of_window,
                                                                            self.height_of_window))

    def do_interaction_with_user(self):
        """
        Encapsulates all possible user interactions. (Hot keys, click events)
        :return:
        """
        for event in pygame.event.get():
            self.handle_user_event(event)

    def handle_user_event(self, event):
        """
        Deal with user events - like pressed keyboard buttoms & mouse
        :param event: event which needs to be dealt with
        :return:-
        """
        # deal with standard events like quitting, pausing the simulation
        if event.type == pygame.QUIT:
            self.simulation.quit_simulation()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.simulation.pause_simulation()
            elif event.key == pygame.K_c:
                self._show_couples_array()
            elif event.key == pygame.K_s:
                self.simulation.save()
            elif event.key == pygame.K_i:
                print(str(self.simulation.settings.step_counter))

    def print_text_on_screen(self, text, pos_x, pos_y, size=30, colour=(0, 0, 0)):
        large_text = pygame.font.Font('freesansbold.ttf', size)
        text_surface = large_text.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x, pos_y)
        #CVisualizationWithPygameBaseClass.screen.blit(text_surface, text_rect)

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
