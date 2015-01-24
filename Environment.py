import math
import random


# Parameters of environment:
# helpers:
# ------------Start-----------------
def add_vectors(angle1, length1, angle2, length2):
    """
    Returns the sum of two vectors
    :rtype : vector in polar coordinates (angle, length)
    :param two vectors in polar coordinates
    :return: sum of vectors
    """
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return angle, length

# -----------End-----------------


class Environment():
    """
    Defines the structure of the environment (e.g.boundary of a simulation and its properties)
    """

    def __init__(self, width, height, itemSize, itemSpeed):
        """

        :param width: the width of the environment
        :param height: the highz
        :return:
        """
        self.width = width
        self.height = height
        self.itemSize = itemSize
        self.itemSpeed = itemSpeed

    def _move(self, item):
        """
        Update position based on speed, angle
        :param item: the object/item whose position should be updated
        :return:
        """
        item.x += math.sin(item.angle) * item.speed
        item.y -= math.cos(item.angle) * item.speed

    def place_item_in_environment(self, item):
        """
        The method places an object/item on some place in the environment. Here it will be just a random point.
        :param item: the object that should be placed in the environment
        :return:
        """
        x = random.uniform(self.itemSize, self.width - self.itemSize)
        y = random.uniform(self.itemSize, self.height - self.itemSize)
        item.x = x
        item.y = y
        item.speed = self.itemSpeed
        item.angle = random.uniform(0, math.pi * 2)

    # ALEX checked untill there!
    def update(self, item1, item2, collision_handler):
        """
        Moves individuals and tests for collisions with the walls and each other
        :param item1:
        :param item2:
        :param collision_handler: method of type collision_handler(CIndividual,CIndividual). The method is called
        when a collision occurs.
        :return:
        """
        for i, objectA in enumerate(item1):
            self._move(objectA)
            self._bounce(objectA)
            # for object in population1.individuals[i+1:]:
            for objectB in item2:
                self._collide(objectA, objectB, collision_handler)
        for objectB in item2:
            self._move(objectB)
            self._bounce(objectB)

    def _bounce(self, item):
        """
        Tests whether an individual has hit the boundary of the environment
        :param item:
        :return:
        """

        if item.x > self.width - self.itemSize:
            item.x = 2 * (self.width - self.itemSize) - item.x
            item.angle = - item.angle

        elif item.x < self.itemSize:
            item.x = 2 * self.itemSize - item.x
            item.angle = - item.angle

        if item.y > self.height - self.itemSize:
            item.y = 2 * (self.height - self.itemSize) - item.y
            item.angle = math.pi - item.angle

        elif item.y < self.itemSize:
            item.y = 2 * self.itemSize - item.y
            item.angle = math.pi - item.angle

    def find_item(self, x, y, groups_of_items):
        """
        Returns any individual that occupies position x, y
        :param x: integer
        :param y: integer
        :param groups_of_items: list of populations
        :return: CIndividual
        """
        for group in groups_of_items:
            for item in group.males:
                if math.hypot(item.x - x, item.y - y) <= self.itemSize:
                    return item
            for item in group.females:
                if math.hypot(item.x - x, item.y - y) <= self.itemSize:
                    return item
        return None

    def _collide(self, p1, p2, collision_handler):
        """
        Tests whether two individuals overlap
        If they do, make them bounce
            i.e. update their angle, speed and position
        :param p1: first individual
        :param p2: second individual
        :param collision_handler:
        :return:
        """

        dx = p1.x - p2.x
        dy = p1.y - p2.y

        dist = math.hypot(dx, dy)
        if dist < 2 * self.itemSize:
            collision_handler(p1, p2)
            angle = math.atan2(dy, dx) + 0.5 * math.pi

            p1.angle, p1.speed = add_vectors(p1.angle, 0, angle, p2.speed)
            p2.angle, p2.speed = add_vectors(p2.angle, 0, angle + math.pi, p1.speed)

            overlap = 0.5 * (2 * self.itemSize - dist + 1)
            p1.x += math.sin(angle) * overlap
            p1.y -= math.cos(angle) * overlap
            p2.x -= math.sin(angle) * overlap
            p2.y += math.cos(angle) * overlap
