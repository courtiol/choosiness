import numpy as np
import math
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from Environments import Environment2D
from Tools.usefulDecorators import measure_percentage_of_time


def find_neighbors(pindex, triang):
    """
    see http://stackoverflow.com/questions/12374781/how-to-find-all-neighbors-of-a-given-point-in-a-delaunay-triangulation-using-sci
    :param pindex: index of vertex
    :param triang: delaunay triangulation
    :return: array of indices of vertices
    """
    return triang.vertex_neighbor_vertices[1][triang.vertex_neighbor_vertices[0][pindex]:triang.vertex_neighbor_vertices[0][pindex+1]]


def sq_dist(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    dist = math.hypot(dx, dy)
    return dist


def check_for_collisions(points, dist, collision_handler):
    np_points = np.array(points)
    tri = Delaunay(np_points)
    for index in range(len(np_points)):
        neighbors = find_neighbors(index, tri)
        for neighbor in neighbors:
            # this line prevents from dealing with vertex pairs two times
            if neighbor > index:
                continue
            if sq_dist(points[index], points[neighbor]) > dist:
                continue
            collision_handler(neighbor, index)


class Environment2DDelaunay(Environment2D.Environment2D):
    """
    This class provides a faster method to check collisions using a delaunay triangulation, which can be computed in
    O(nlog n).
    """
    @measure_percentage_of_time
    def update(self, group1, group2, collision_handler):
        """
        We update the positions and compute afterwards collisions between objects from the first group and objects
        from the second group
        :param group1:
        :param group2:
        :param collision_handler: function pointer
        :return:
        """
        def collision_detected(index1, index2):
            """
            If a collision is detected this method is called. We convert the indices of objects that collided
            to the objects back and call the _collide method from the super class
            :param index1: index of first object in the array
            :param index2: index of second object in the array
            :return:
            """
            # We check if index1 in coord_1 or coord_2 lies
            if index1 < len(coord_1)-len(coord_2):  # belongs to group 1
                collided_object1 = group1[index1]
                if index2 >= len(coord_1)-len(coord_2):  # belongs to group 2
                    collided_object2 = group2[index2-len(coord_1)]
                else:
                    return
            else:
            # belongs to group 2
                collided_object2 = group2[index1-len(coord_1)]
                if index2 < len(coord_1)-len(coord_2):  # belongs to group 1
                    collided_object1 = group1[index2]
                else:
                    return
            # we deal with the collision
            self._collide(collided_object1, collided_object2, collision_handler)

        # First we move all the objects
        for object1 in group1:
            self._move(object1)
            self._bounce(object1)
        for object2 in group2:
            self._move(object2)
            self._bounce(object2)
        coord_1 = [[object1.x, object1.y] for object1 in group1]
        coord_2 = [[object2.x, object2.y] for object2 in group2]
        coord_1.extend(coord_2)
        # self.itemSize*2 = distance between two circle centers
        check_for_collisions(coord_1, self.itemSize*2, collision_detected)


class Environment2DTest(Environment2D.Environment2D):
    """
    Yet another collision handler for testing
    """
    def iterate_over_area(self, area, object, func):
        """
        Appends a marker at each point in range of an object
        :param area:
        :param object:
        :param func:
        :return:
        """
        sq_radius = self.itemSize**2
        # compute bounding box to decrease the array to check
        lowerx = int(max([object.x-self.itemSize,0]))
        upperx = int(min([object.x+self.itemSize,self.width]))
        for x in range(lowerx, upperx):
            lowery = int(max([object.y-self.itemSize,0]))
            uppery = int(min([object.y+self.itemSize,self.height]))
            for y in range(lowery, uppery):
                if (x-object.x)**2 + (y-object.y)**2 - sq_radius <= 0:
                    # if func return false don t check the others. This is necessary to prevent the algorithm from
                    # detecting several times the same pair of objects
                    if not func(area[x][y], object):
                        return

    @measure_percentage_of_time
    def update(self, group1, group2, collision_handler):
        # two collisions handler that are needed in this function
        def attach(point, object):
            point.append(object)
            return True

        def collision_detected(point, object):
            if len(point) > 0:
                self._collide(object, point[0], collision_handler)
                return False
        area = [[[] for x in range(self.width)] for x in range(self.height)]

        # First we move all the objects
        for object1 in group1:
            self._move(object1)
            self._bounce(object1)
        for object2 in group2:
            self._move(object2)
            self._bounce(object2)

        # attach males to the pixels in range
        for object1 in group1:
            self.iterate_over_area(area, object1, attach)
        # check for each female if it collided
        for object2 in group2:
            self.iterate_over_area(area, object2, collision_detected)
