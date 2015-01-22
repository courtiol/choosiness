import pygame
import math
import CIndividual
from Visualization.CVisualizationBaseClass import CVisualizationBaseClass
from Visualization.VisualizationWithPygame.CVisualizationWithPygameBaseClass import CVisualizationWithPygameBaseClass

# -------------------------------------diagrams (self made) -----------------------------------

"""
This class is not used anymore, since it is replaced by matplotlib.
"""

class CDiagramVisualizationOfSimulation(CVisualizationWithPygameBaseClass):
    def __init__(self, simulation):
        CVisualizationWithPygameBaseClass.__init__(self, simulation)
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
        CVisualizationWithPygameBaseClass.screen.fill(self.colour_of_background)
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

            pygame.draw.rect(CVisualizationWithPygameBaseClass.screen, self.colour_of_female_bar, (xf, yf, xf_offset,
                                                                                                   yf_offset))
            if female_bar_height > 0:
                self.print_text_on_screen(str(round(female_bar_height*100))+"%", xf+13, yf+yf_offset+9,
                                          self.text_size_bar_label)
            pygame.draw.rect(CVisualizationWithPygameBaseClass.screen, self.colour_of_male_bar, (xm-xf_offset, ym,
                                                                                                 xm_offset, ym_offset))
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