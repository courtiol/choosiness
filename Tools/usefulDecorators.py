__author__ = 'robert'

def printAllParameters(__str__):
    """
    Decorator for __str__. After applying the method prints the values of all parameters of the class
    :param __str__:
    :return:new __str__ method
    """
    def new_str(*args):
        z = ""
        for key in args[0].__dict__.keys():
            z += key+": "+str(args[0].__dict__[key])+"\n"
        z += __str__(*args)
        return z
    return new_str