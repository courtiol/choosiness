import math, random

#Parameters of environment:

#helpers:
#------------Start-----------------
def addVectors(angle1, length1, angle2, length2):
    """
    Returns the sum of two vectors
    :param angle1:
    :param length1:
    :param angle2:
    :param length2:
    :return:
    """

    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle  = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)
#-----------End-----------------

class Environment():
    """
    Defines the structure of the environment (e.g.boundary of a simulation and its properties)
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objectSize = 7

    def __move(self, object):
        """
        Update position based on speed, angle
        """
        object.x += math.sin(object.angle) * object.speed
        object.y -= math.cos(object.angle) * object.speed

    def place_object_in_environment(self, object):
        x = random.uniform(self.objectSize, self.width - self.objectSize)
        y = random.uniform(self.objectSize, self.height - self.objectSize)
        object.x = x
        object.y = y
        object.direction = (1,2)
        object.speed = 5
        object.angle = random.uniform(0, math.pi*2)

    def update(self, objects1, objects2, collision_handler):
        """
        Moves individuals and tests for collisions with the walls and each other
        :param objects1:
        :param objects2:
        :param collision_handler: method of type collision_handler(CIndividual,CIndividual). The method is called
        when a collision occurs.
        :return:
        """
        for i, objectA in enumerate(objects1):
            self.__move(objectA)
            self.__bounce(objectA)
            #for object in population1.individuals[i+1:]:
            for objectB in objects2:
                self.__collide(objectA, objectB, collision_handler)
        for objectB in objects2:
            self.__move(objectB)
            self.__bounce(objectB)

    def __bounce(self, object):
        """
        Tests whether an individual has hit the boundary of the environment
        :param object:
        :return:
        """
        
        if object.x > self.width - self.objectSize:
            object.x = 2*(self.width - self.objectSize) - object.x
            object.angle = - object.angle

        elif object.x < self.objectSize:
            object.x = 2*self.objectSize - object.x
            object.angle = - object.angle

        if object.y > self.height - self.objectSize:
            object.y = 2*(self.height - self.objectSize) - object.y
            object.angle = math.pi - object.angle

        elif object.y < self.objectSize:
            object.y = 2*self.objectSize - object.y
            object.angle = math.pi - object.angle

    def findObject(self, x, y, groups_of_object):
        """
        Returns any individual that occupies position x, y
        :param x: integer
        :param y: integer
        :param groups_of_object: list of populations
        :return: CIndividual
        """
        for group in groups_of_object:
            for object in group.males:
                if math.hypot(object.x - x, object.y - y) <= self.objectSize:
                    return object
            for object in group.females:
                if math.hypot(object.x - x, object.y - y) <= self.objectSize:
                    return object
        return None

    def __collide(self, p1, p2, collision_handler):
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
        if dist < 2*self.objectSize:
            collision_handler(p1, p2)
            angle = math.atan2(dy, dx) + 0.5 * math.pi

            (p1.angle, p1.speed) = addVectors(p1.angle, 0, angle, p2.speed)
            (p2.angle, p2.speed) = addVectors(p2.angle, 0, angle+math.pi, p1.speed)

            overlap = 0.5*(2*self.objectSize - dist+1)
            p1.x += math.sin(angle)*overlap
            p1.y -= math.cos(angle)*overlap
            p2.x -= math.sin(angle)*overlap
            p2.y += math.cos(angle)*overlap
