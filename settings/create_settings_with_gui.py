__author__ = 'robert'

import sys
from PyQt4 import QtGui
import inspect
import jsonpickle

# import these classes for settings
import settings
import CPopulation
from Environments.EnvironmentBase import CBaseEnvironment

# Don't remove this. The imports are necessary for 'inspect'
# imports for inspect:
import Environments.Environment2D
import Environments.EnvironmentSoup
import Environments.Environment2DFaster
import CIndividual

# ---------------------------------------


def get_dict_from_class(class_type):
    """
    Checks for a given class the constructor and creates a dictionary from this for the parameters that are required.
    If a parameter has the form ... : class_type it creates a nested dictionary from this
    :param class_type:
    :return: dictionary with the parameters that are necessary to create an object of type class_type
    """
    current_dict = {}
    # Get the signature of the constructor
    signature_of_constructor = inspect.signature(class_type)
    # iterate over the arguments
    for parameter_name, _ in signature_of_constructor.parameters.items():
        # if the current parameter is a class....
        # ToDo: Do that better
        if signature_of_constructor.parameters[parameter_name].annotation != inspect._empty \
                    and inspect.isclass(signature_of_constructor.parameters[parameter_name].annotation):
            current_dict[parameter_name] = \
                getDictFromBaseClass(signature_of_constructor.parameters[parameter_name].annotation)
        elif parameter_name != 'classType_settings':
            current_dict[parameter_name] = Reference('placeholder')
    return current_dict

def getDictFromBaseClass(base_class_type):
    """
    Creates a dictionary from a given base class by calling 'getDictFromClass' for a very direct subclass
    :param base_class_type:
    :return:
    """
    subclasses = get_subclasses(base_class_type)
    list = []
    for subclass in subclasses:
        list.append((subclass, get_dict_from_class(subclass)))
    print(list)
    return list


class Reference():
    """
    Workaround, since python does not offer references for base types
    """
    def __init__(self, v):
        self.v = v
    def __str__(self):
        return str(self.v)
    # ToDo: Remove this maybe after debugging. Since __repr__ should be unique and distinct from __str.
    def __repr__(self):
        return str(self.v)
#------------------------------------------


def get_subclasses(base_class):
    """
    Returns a list of (directly) derived subclasses
    :param base_class:
    :return: list of (direct) subclasses
    """
    list_of_classes = []
    for sc in base_class.__subclasses__():
        list_of_classes.append(sc)
    return list_of_classes


class SettingsGui(QtGui.QWidget):
    """
    Creates dynamically a gui for the settings of the simulation, where all implementations of
    CPopulation.CBasePopulation and CBaseEnvironment can be selected. To do that the 'inspect' module is used. The
    constructor of each class is iterated. For each parameter in the constructor that is by itself a derived class
    of any base class the necessary settings are recursively extracted.
    """
    def __init__(self):
        super(SettingsGui, self).__init__()
        # two dictionaries for assigning values between the widgets and the settings dictionary:
        self.widget_to_dict_entry = {}
        self.dict_entry_to_widget = {}

        self.initUI()


    def get_stacked_layout(self, list_of_dicts):
        """
        Creates a stacked layout for a dictionary of the form: [(name1, dictionary1), ... , (name1, dictionary1)]
        'name' must be a string.
        :param list_of_dicts: parameter of the form [(name1, dictionary1), ... , (name1, dictionary1)]
        :return:
        """
        stacked_layout = QtGui.QStackedLayout()
        combobox = QtGui.QComboBox(self)  # Combobox which has 'name1', ..., 'name_n' as choice
        dict_name_in_combobox_to_layout = {}
        # iterate over dictionaries in the list
        index = 0
        for name, item_dict in list_of_dicts:
            combobox.addItem(str(name))  # add the current name
            new_hbox = self.get_layout_of_dict(item_dict) # create recursively 'subsettings'
            # Assemble stacked layout
            parentWidget = QtGui.QWidget()
            parentWidget.setLayout(new_hbox)
            # save which combobox entry corresponds to which stacked layout
            dict_name_in_combobox_to_layout[str(name)] = index
            index += 1
            stacked_layout.addWidget(parentWidget)

        # This method is used when another entry in the combobox is selected
        def connect_combobox(text):
            print(text)
            stacked_layout.setCurrentIndex(dict_name_in_combobox_to_layout[text])
        combobox.activated[str].connect(connect_combobox)
        return combobox, stacked_layout

    def get_layout_of_dict(self, data_dict):
        """
        Creates a layout from a dictionary/tree of the form:
        {... , 'class_type':[(a_1,same structure), ..., (a_n,same structure)], ...}
        """
        vbox = QtGui.QVBoxLayout()
        for key in data_dict.keys():
            label = QtGui.QLabel(str(key), self)  # Create a label for each key
            if type(data_dict[key]) == list:  # inner node
                # Create 'subsettings' for this list
                combobox, stacked_layout = self.get_stacked_layout(data_dict[key])
                # Assemble everything to a vertical layout
                hbox = QtGui.QVBoxLayout()
                hbox.addWidget(label)
                hbox.addWidget(combobox)
                vbox.addLayout(hbox)
                vbox.addLayout(stacked_layout)
                # save which widget belongs to which dict entry and vice versa
                self.widget_to_dict_entry[combobox] = data_dict[key]
                self.dict_entry_to_widget[id(data_dict[key])] = combobox
            else:  # leaf
                # Create a QLineEdit box for chaning the value of the 'leaf' (simple parameter in the dictionary)
                parameter_box = QtGui.QHBoxLayout()
                text_field = QtGui.QLineEdit(self)
                self.widget_to_dict_entry[text_field] = data_dict[key]
                # Use 'id()' to obtain a reference of data_dict[key]
                self.dict_entry_to_widget[id(data_dict[key])] = text_field
                # add everything to the vertical layout
                parameter_box.addWidget(label)
                parameter_box.addWidget(text_field)
                vbox.addLayout(parameter_box)
        return vbox

    def initUI(self):
        # Get parameters for the environment
        self.parameter_settings = {'classType_of_population': getDictFromBaseClass(CPopulation.CBasePopulation),
                                   'classType_of_environment': getDictFromBaseClass(CBaseEnvironment)}
        print("settings:")
        print(self.parameter_settings)

        hbox = self.get_layout_of_dict(self.parameter_settings)

        self.parentWidget = QtGui.QWidget()
        self.parentWidget.setLayout(hbox)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidget(self.parentWidget)
        hbox2 = QtGui.QVBoxLayout()
        hbox2.addWidget(self.scroll)

        self.create_settings_button = QtGui.QPushButton('Create Settings', self)
        self.create_settings_button.clicked.connect(self.on_create_settings_button_clicked)
        hbox2.addWidget(self.create_settings_button)

        self.setLayout(hbox2)
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('Create settings for the simulation:')
        self.show()

    def on_create_settings_button_clicked(self):
        """
        Save the settings in a to settings.CSimulationSettings compatible format
        """
        # Save first just every value of the layout in the corresponding dictionary 'self.parameter_settings' by using
        # 'self.widget_to_dict_entry'
        for widget in self.widget_to_dict_entry.keys():
            if type(widget) != QtGui.QComboBox:
                self.widget_to_dict_entry[widget].v = widget.text()
        # Now check what entries are selected in the comboboxes and retrieve from this the settings
        resulting_dict = self.create_dict_from_combobox_choice(self.parameter_settings)
        # Save these settings
        new_settings = settings.CSimulationSettings()
        new_settings.settings_dict = resulting_dict
        new_settings.save_settings_to_file('Vergleich.txt')
        # ToDo: More markers. It's not enough to just test for  list. What is, when you really need a list as a parameter?

    def create_dict_from_combobox_choice(self, sub_dict):
        """
        Create a dictionary compatible to settings.CSimulationSettings. This means for each combobox the selected
        key und subdirectory in the dictionary must be extracted
        """
        current_dict = {}  # create a new dictionary to store the data
        for key in sub_dict.keys():  # iterate over the input dictionary
            # if an entry is a list, the list entry selected in the combobox must be selected
            if type(sub_dict[key]) == list:
                # Get this entry with 'self.dict_entry_to_widget'
                selected_list_element = self.dict_entry_to_widget[id(sub_dict[key])].currentText()
                current_list = sub_dict[key]  # save for convenience this list
                for elem in current_list:  # now we select the entry corresponding to the combobox
                    # If the string representation of the first element of the current tuple matches the
                    # selected list element .....
                    if str(elem[0]) == selected_list_element:
                        # ... then deal with that 'subdictionary' in
                        current_dict[key] = elem[0]
                        # if no "classType_settings" is yet in 'current_dict', an entry is created
                        if "classType_settings" not in current_dict:
                            current_dict["classType_settings"] = {}
                        # Save the parameters of the corresponding combobox 'subsettings'
                        current_dict["classType_settings"][key] = self.create_dict_from_combobox_choice(elem[1])
            else:
                # We saved everything as a reference. Now we want the real value
                current_dict[key] = jsonpickle.decode(sub_dict[key].v)
        return current_dict


def main():
    app = QtGui.QApplication(sys.argv)
    ex = SettingsGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
