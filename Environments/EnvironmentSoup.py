__author__ = 'robert'

from Tools.usefulDecorators import printAllParameters
from Tools.usefulDecorators import measure_percentage_of_time
from random import shuffle, uniform


class EnvironmentSoup():
    """
    The collisions are computed here without any geometry.
    """
    def __init__(self, e):
        self.e = e

    def place_item_in_environment(self, item):
        # Nothing to do here
        pass

    @measure_percentage_of_time
    def update(self, group1, group2, collision_handler):
        # shuffle both groups to avoid any effect of the orders of the groups
        shuffle(group1)
        shuffle(group2)
        for i in range(min([len(group1), len(group2)])):
            if uniform(0, 1) <= self.e:
                collision_handler(group1[i], group2[i])

    @printAllParameters
    def __str__(self):
        return ""
