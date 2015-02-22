__author__ = 'robert'

class CBaseEnvironment():
    """
    The following methods need to be implemented, in order to ensure compatibility with the simulation.
    """
    def place_item_in_environment(self, item):
        pass

    def update(self, group1, group2, collision_handler):
        pass
