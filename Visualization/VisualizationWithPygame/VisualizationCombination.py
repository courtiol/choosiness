__author__ = 'robert'

import pygame

from Visualization.VisualizationWithPygame.CVisualizationWithPygameBaseClass import CVisualizationWithPygameBaseClass
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import C2DVisualizationOfSimulation
from Visualization.CVisualizationBaseClass import CSimpleVisualization
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import CVisualizationWithMatplotlib, \
    CHistogramVisualization
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import CNoVisualizationOfSimulation
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import CHistogramVisualization

class CCombinationOfVisualizations(CVisualizationWithPygameBaseClass):
        def __init__(self, simulation):
            CVisualizationWithPygameBaseClass.__init__(self, simulation)
            self.list_of_visualizations = []
            self.visualization_pointer = 0  # which visualization
            self.list_of_visualizations.append(C2DVisualizationOfSimulation(self.simulation))
            self.list_of_visualizations.append(CNoVisualizationOfSimulation(self.simulation))  # no visualization
            self.list_of_visualizations.append(CVisualizationWithMatplotlib(self.simulation))
            self.list_of_visualizations.append(CHistogramVisualization(self.simulation))
            self.current_visualization = self.list_of_visualizations[self.visualization_pointer]

        def init_display(self):
            self.current_visualization.init_display()

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
                    elif event.key == pygame.K_i:
                        print(str(self.simulation.settings.step_counter))
                    elif event.key == pygame.K_RIGHT:
                        self._next_visualization()
                    elif event.key == pygame.K_LEFT:
                        self._prior_visualization()
            if self.simulation.selected_individual:
                self.simulation.give_information_about_selected_individual()
                self._show_information_about_selected_individual()

        def print_information_about_population(self):
            self.current_visualization.print_information_about_population()

        def draw_simulation(self):
            self.current_visualization.draw_simulation()

        def _next_visualization(self):
            self.visualization_pointer = (self.visualization_pointer+1) % len(self.list_of_visualizations)
            self.current_visualization = self.list_of_visualizations[self.visualization_pointer]
            self.current_visualization.init_screen()
            print(self.current_visualization)

        def _prior_visualization(self):
            self.visualization_pointer = (self.visualization_pointer-1) % len(self.list_of_visualizations)
            self.current_visualization = self.list_of_visualizations[self.visualization_pointer]
            self.current_visualization.init_screen()
            print(self.current_visualization)
