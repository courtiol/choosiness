import pygame
import math
import Environment
import CPopulation
import CIndividual
from Visualization.CVisualizationBaseClass import CVisualizationBaseClass

"""
In this module you find different graphical representations of the simulation. Each representation of the simulation
should be derived from the the following abstract base class:
"""
#shared by all classes in this module
screen = None

#---------------------------------------Visualization with pygame--------------------------
class CVisualizationWithPygame(CVisualizationBaseClass):
    def __init__(self, simulation):
        CVisualizationBaseClass.__init__(self,simulation)

    #overwrite
    def initDisplay(self):
        global screen
        screen = pygame.display.set_mode((self.simulation.settings.width, self.simulation.settings.height))
        pygame.display.set_caption("Simulation with "+str		(self.simulation.population.get_current_females_size())+' females in red and '+str(self.simulation.population.get_current_males_size())+' males in blue')
        pygame.init()

    def init_screen(self):
        global screen
        screen = pygame.display.set_mode((self.simulation.settings.width, self.simulation.settings.height))

    def doInteractionWithUser(self):
        """
        Encapsulates all possible user interactions. (Hot keys, click events)
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.simulation.quit_simulation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                self.simulation.selectIndividual(mouseX, mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.simulation.selected_individual = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.simulation.pause_simulation()
                elif event.key == pygame.K_c:
                    self.__show_couples_array()
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
                self.__show_information_about_selected_individual()

    def printTextOnScreen(self, text, posX, posY, size=30, colour=(0,0,0)):
        largeText = pygame.font.Font('freesansbold.ttf',size)
        textSurface = largeText.render(text, True, colour)
        TextRect = textSurface.get_rect()
        TextRect.center = (posX,posY)
        screen.blit(textSurface, TextRect)

    def __show_couples_array(self):
        print("couples with length "+str(len(self.simulation.population.couples))+"\n")
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
        text += "i - current timestep\n"
        text += "left click on circle - information about individual in terminal"
        return text

#---------------------------------------No visualization-----------------------------------
class CNoVisualizationOfSimulation(CVisualizationWithPygame):
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self,simulation)
        self.colour_of_background = (255,255,255)
    #overwrite
    def init_screen(self):
        CVisualizationWithPygame.init_screen(self)
        screen.fill(self.colour_of_background)
        self.printTextOnScreen("No visualization selected", self.simulation.settings.width/2, self.simulation.settings.height/2-40, 30)
        self.printTextOnScreen("p - pause/run", self.simulation.settings.width/2, self.simulation.settings.height/2, 15)
        self.printTextOnScreen("v - next visualization", self.simulation.settings.width/2, self.simulation.settings.height/2+20, 15)
        self.printTextOnScreen("i - current timestep", self.simulation.settings.width/2, self.simulation.settings.height/2+40, 15)
        pygame.display.flip()

    def __str__(self):
        return "No visualization"

#---------------------------------------2D-Visualization-----------------------------------
class C2DVisualizationOfSimulation(CVisualizationWithPygame):
    """
    The class encapsulates the visual output of the simulation. In order to that it makes use of pygame. It requires also
    a pointer to the instance of the simulation.
    """
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self,simulation)
        self.colour_of_environment = (255,255,255)
        self.colour_of_males = (0, 0, 255) #blue
        self.thickness_latency = 2
        self.thickness_available = 0
        self.colour_of_females = (255, 0, 0) #red
        self.colour_of_dead_individual = (0, 0, 0) #black

    def drawSimulation(self):
        self.__drawEnvironment()
        self.__drawPopulation(self.simulation.population)
        pygame.display.flip()

    #display
    def __drawEnvironment(self):
        """
        Sets the background colour, shows the current number of collisions and the average collision number per
        step.
        :return:
        """
        screen.fill(self.colour_of_environment)
        text = 'collisions: '+str(self.simulation.settings.collision_counter)
        text += " average: "+str(round(self.simulation.settings.average_number_of_collisions_per_timestep,4))
        self.printTextOnScreen(text, self.simulation.settings.width/2, self.simulation.settings.height/2)

    def __drawPopulation(self, population):
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.get_current_females_size())+' females in red and '+str(self.simulation.population.get_current_males_size())+' males in blue')
        thickness = 0
        for p in population.males:
            self.__drawIndividual(p)
        for p in population.females:
            self.__drawIndividual(p)

    def __drawIndividual(self, individual):
        """
        Each individual is represented by a circle. The colour of the circle depends on the gender and state of the
        individual.
        :param individual:individual which is drawn.
        :return:
        """
        # thickness = 2
        if (individual.get_gender() == CIndividual.MALE):
            if individual.state == CIndividual.IN_LATENCY:
                pygame.draw.circle(screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_latency)
            else:
                pygame.draw.circle(screen, self.colour_of_males, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_available)
            self.printTextOnScreen(str(round(individual.q,4)), int(individual.x), int(individual.y), 15)
        else:
            if individual.state == CIndividual.IN_LATENCY:
                pygame.draw.circle(screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_latency)
            else:
                pygame.draw.circle(screen, self.colour_of_females, (int(individual.x), int(individual.y)),
                                   self.simulation.env.objectSize, self.thickness_available)
            self.printTextOnScreen(str(round(individual.phi,4)), int(individual.x), int(individual.y), 15)

    def __show_information_about_selected_individual(self):
        if self.simulation.selected_individual != None:
            print(str(self.simulation.selected_individual))

    def __str__(self):
        return "2D visualization"

#-------------------------------------diagrams-----------------------------------
class CDiagramVisualizationOfSimulation(CVisualizationWithPygame):
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self, simulation)
        self.window_height = 800
        self.window_width = 800
        self.colour_of_background = (255,255,255)
        self.colour_of_female_bar = (255,0,0)
        self.colour_of_male_bar = (0,0,255)
        self.number_of_bars = 10.0
        self.width_of_bars = self.window_width/self.number_of_bars
        self.text_size = int(self.window_width/(8*self.number_of_bars))
        self.text_size_bar_label = int(self.text_size*1)
        self.maximal_height = round(self.window_height*0.6)

    def drawSimulation(self):
        screen.fill(self.colour_of_background)
        pygame.display.set_caption("Simulation with "+str(self.simulation.population.get_current_females_size())+' females in red and '+str(self.simulation.population.get_current_males_size())+' males in blue')
        self.printTextOnScreen("Choosiness of females(red) and males(blue). ", 170,10, self.text_size)
        self.printTextOnScreen(str(len(self.simulation.population.couples))+" babies are in the waiting queue", 200,self.window_height-50, self.text_size)

        for i in range(int(self.number_of_bars)):
            text_x = i*self.width_of_bars+self.text_size+15
            text_y = self.window_height-750
            self.printTextOnScreen(str(i/self.number_of_bars)+"-"+str((i+1)/self.number_of_bars), text_x, text_y, self.text_size)
        self.__draw_bars()
        pygame.display.flip()

    def __draw_bars(self):
        female_bars = self.__count_choosiness_of_females()
        male_bars = self.__count_choosiness_of_males()
        for i in range(int(self.number_of_bars)):
            female_bar_height = female_bars[i]/self.simulation.population.get_current_females_size()
            male_bar_height = male_bars[i]/self.simulation.population.get_current_males_size()
            (xf,yf,xf_offset, yf_offset) = self.__compute_position_of_bar(female_bar_height, i)
            (xm,ym,xm_offset, ym_offset) = self.__compute_position_of_bar(male_bar_height, i)

            pygame.draw.rect(screen, self.colour_of_female_bar, (xf,yf,xf_offset, yf_offset) )
            if female_bar_height > 0:
                self.printTextOnScreen(str(round(female_bar_height*100))+"%", xf+13,yf+yf_offset+9, self.text_size_bar_label)
            pygame.draw.rect(screen, self.colour_of_male_bar, (xm-xf_offset,ym,xm_offset, ym_offset) )
            if male_bar_height > 0:
                self.printTextOnScreen(str(round(male_bar_height*100))+"%", xm-xf_offset+13,ym+ym_offset+9, self.text_size_bar_label)
        return

    def __compute_position_of_bar(self, bar_height, i):
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
        return (x,y,x_offset,y_offset)

    def __count_choosiness_of_females(self):
        return self.__count_choosiness(self.simulation.population.females)

    def __count_choosiness_of_males(self):
        return self.__count_choosiness(self.simulation.population.males)

    def __count_choosiness(self, group_of_individuals):
        """
        Counts individuals according to their choosiness and saves the result in the array bars[]
        :return:bars
        """
        bars = []
        for i in range(int(self.number_of_bars)):
            bars.append(0)
        for ind in group_of_individuals:
            choosiness = math.floor(ind.phi*self.number_of_bars)
            bars[int(choosiness)] = bars[int(choosiness)]+1
        return bars

    def __str__(self):
        return "Diagram visualization"

#-----------------------------------------------------------
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

import matplotlib.pyplot as plt


class CTestVisualization(CVisualizationWithPygame):
    def __init__(self, simulation):
        CVisualizationWithPygame.__init__(self, simulation)
        self.fig = pylab.figure(figsize=[4, 4],dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.num_bins = 20
        self.update_in_every_n_step = 10 #it not necessary to update in every step the graphics
        self.counter = 0

    def drawSimulation(self):
        self.counter = (self.counter+1)%self.update_in_every_n_step
        if self.counter != 0:
            return
        #female phi-plot
        females = self.__get_female_choosiness_array()
        female_surf = self.__plot(females,'red', 'Choosiness of Females', 'choosiness')
        screen.blit(female_surf, (0,0))

        #male phi-plot
        males = self.__get_male_choosiness_array()
        male_surf = self.__plot(males,'blue', 'Choosiness of Males', 'choosiness')
        screen.blit(male_surf, (400,0))

        #female q-plot
        females = self.__get_female_quality_array()
        female_surf = self.__plot(females,'red', 'Quality of Females', 'quality')
        screen.blit(female_surf, (0,400))

        #female q-plot
        males = self.__get_male_quality_array()
        male_surf = self.__plot(males,'blue', 'Quality of Males', 'quality')
        screen.blit(male_surf, (400,400))

        pygame.display.flip()

    def __plot(self, data, colour, title, xaxis_label):
        self.canvas.figure.clf() #clears the previous diagram
        n, bins, patches = plt.hist(data, self.num_bins, normed=False, facecolor=colour, alpha=0.5)
        plt.xlabel(xaxis_label)
        plt.ylabel("Frequency")
        plt.title(title)

        self.canvas.draw()
        renderer = self.canvas.get_renderer()

        raw_data = renderer.tostring_rgb()
        size = self.canvas.get_width_height()

        return pygame.image.fromstring(raw_data, size, "RGB")


    def __get_male_choosiness_array(self):
        return [ind.phi for ind in self.simulation.population.males]

    def __get_female_choosiness_array(self):
        return [ind.phi for ind in self.simulation.population.females]

    def __get_female_quality_array(self):
        return [ind.q for ind in self.simulation.population.females]

    def __get_male_quality_array(self):
        return [ind.q for ind in self.simulation.population.males]

    def __str__(self):
        return "Diagrams"
