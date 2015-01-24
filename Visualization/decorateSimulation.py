__author__ = 'robert'

"""
The visualizations can be attached to the simulation class via this decorator.
"""

def add_visualization_to_simulation(simulation, visualization):
    """
    Adds chosen visualization to the simulation
    :param simulation - the simulation that that should be visualized
    :param visualization - chosen visualization for the simulation
    """
    #inserts the "drawing-step" in the simulation
    simulation.perform_time_step = CDecorator(simulation.perform_time_step, [visualization.draw_simulation])
    #add user control
    simulation.hook_for_user_control = CDecorator(simulation.hook_for_user_control,
                                                  [visualization.do_interaction_with_user])


#----------------------------------Decorator class---------------------------------------------------
class CDecorator():
    """
    Standard decorator class
    """
    def __init__(self, function_to_be_manipulated, list_of_functions):
        self.old_function = function_to_be_manipulated
        self.functions_after_performing_timestep = list_of_functions

    def __call__(self):
        self.old_function()
        for func in self.functions_after_performing_timestep:
            func()