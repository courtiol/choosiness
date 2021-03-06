__author__ = 'robert'

import pygame

from Visualization.VisualizationWithPygame.CVisualizationWithPygameBaseClass import CVisualizationWithPygameBaseClass
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import C2DVisualizationOfSimulation
from Visualization.CVisualizationBaseClass import CSimpleVisualization
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import CNHistograms, \
    C1Histogram
from Visualization.VisualizationWithPygame.VisualizationOf2DEnvironment import CNoVisualizationOfSimulation
from Visualization.VisualizationWithPygame.VisualizationWithDiagrams import C1Histogram


class CCombinationOfVisualizations(CVisualizationWithPygameBaseClass):
        def __init__(self, simulation, width_of_window, height_of_window, list_of_visualizations):
            CVisualizationWithPygameBaseClass.__init__(self, simulation, width_of_window, height_of_window)
            self.list_of_visualizations = list_of_visualizations
            self.visualization_pointer = 0  # which visualization
            """
            self.list_of_visualizations = []
            for type_of_visualization in types_of_visualizations:
                # All visualizations should have this constructor
                self.list_of_visualizations.append(type_of_visualization(self.simulation, width_of_window,
                                                                            height_of_window))
            """
            self.current_visualization = self.list_of_visualizations[self.visualization_pointer]

        def init_display(self):
            self.current_visualization.init_display()

        def handle_user_event(self, event):
            """
            Encapsulates all possible user interactions. (Hot keys, click events)
            :return:
            """
            # add user events for changing the visualization then call
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._next_visualization()
                elif event.key == pygame.K_LEFT:
                        self._prior_visualization()
            # deal with remaining user events in the current visualization
            self.current_visualization.handle_user_event(event)

        def print_information_about_population(self):
            self.current_visualization.print_information_about_population()

        def draw_simulation(self):
            self.current_visualization.draw_simulation()

        def _next_visualization(self):
            # if the visualization is not updated in every step, add the counter to zero before changing the
            # visualization
            if hasattr(self.current_visualization, 'counter'):
                self.current_visualization.counter = 0
            self.visualization_pointer = (self.visualization_pointer+1) % len(self.list_of_visualizations)
            self.current_visualization = self.list_of_visualizations[self.visualization_pointer]
            self.current_visualization.init_screen()
            print(self.current_visualization)

        def _prior_visualization(self):
            self.visualization_pointer = (self.visualization_pointer-1) % len(self.list_of_visualizations)
            self.current_visualization = self.list_of_visualizations[self.visualization_pointer]
            self.current_visualization.init_screen()
            print(self.current_visualization)
