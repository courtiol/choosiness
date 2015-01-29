__author__ = 'robert'

from Tools.usefulDecorators import printAllParameters
from Tools.usefulDecorators import measure_percentage_of_time
from random import shuffle, uniform


class EnvironmentL():
    """
    The collisions are computed here without any geometry
    """
    def __init__(self, width, height, itemSize, itemSpeed):  # ToDo: Change constructor
        self.e = 0.9  # ToDo: Change that
        #self.number_of_calls = 0 # ToDo: Remove that
        #self.number_of_couples = 0 # ToDo: Remove that
        #self.minima = 0 # ToDo: Remove that

    def place_item_in_environment(self, item):
        # Nothing to do here
        pass

    @measure_percentage_of_time
    def update(self, group1, group2, collision_handler):
        #self.number_of_couples += len(group2) #min([len(group1), len(group2)]) # ToDo: Remove that
        #self.number_of_calls += 1 # ToDo: Remove that
        #self.minima += min([len(group1), len(group2)])
        #print("av. num. of couples "+str(self.number_of_couples/self.number_of_calls)) # ToDo: Remove that
        #print("av. num. of self.minima "+str(self.minima/self.number_of_calls)) # ToDo: Remove that
        # shuffle both groups to avoid any effect of the orders of the groups
        shuffle(group1)
        shuffle(group2)
        for i in range(min([len(group1), len(group2)])):
            if uniform(0, 1) <= self.e:
                collision_handler(group1[i], group2[i])

    @printAllParameters
    def __str__(self):
        return ""
