__author__ = 'robert'

#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore
import inspect
import jsonpickle

# import these classes for settings
import settings
import CPopulation
from Environments.EnvironmentBase import CBaseEnvironment
import Environments.Environment2D
import Environments.EnvironmentSoup
import Environments.Environment2DFaster
import CIndividual

# ---------------------------------------
def getDictFromClass(class_type):
    dict = {}
    # Get the signature of the constructor
    signature_of_constructor = inspect.signature(class_type) #
    # iterate over the arguments
    for parameter_name, _ in signature_of_constructor.parameters.items():
        # if the current parameter is a class....
        if signature_of_constructor.parameters[parameter_name].annotation != inspect._empty \
                    and inspect.isclass(signature_of_constructor.parameters[parameter_name].annotation):
            dict[parameter_name] = getDictFromBaseClass(signature_of_constructor.parameters[parameter_name].annotation)
        elif parameter_name != 'classType_settings':
            dict[parameter_name] = Reference('placeholder')
    return(dict)

def getDictFromBaseClass(base_class_type):
    subclasses = get_subclasses(base_class_type)
    list = []
    for subclass in subclasses:
        list.append((subclass, getDictFromClass(subclass)))
    print(list)
    return list

#-------------------------------------------
class Reference():
    def __init__(self, v):
        self.v = v
    def __str__(self):
        return str(self.v)
    # ToDo: Remove after debugging
    def __repr__(self):
        return str(self.v)
#-------------------------------------------

data = {'a':Reference("1"), 'population':[('p1', {'s':Reference('0.1'), 'Individual':[('CI1',{}), ('CI2',{})]}), ('p2',{'l':Reference('1')})], 'environments':[('env1', {'e':Reference('0.9')}), ('env2', {'d':Reference('0')})]}
# ---------------------------------------


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

class Settings_Gui(QtGui.QWidget):

    def __init__(self):
        super(Settings_Gui, self).__init__()
        self.widget_to_dict_entry = {}
        self.dict_entry_to_widget = {}

        self.initUI()

    def get_stacked_layout(self, list_of_dicts):
        stacked_layout = QtGui.QStackedLayout()
        combobox = QtGui.QComboBox(self)
        dict_name_in_combobox_to_layout = {}
        # iterate over dictionaries in the list
        index = 0
        for name, item_dict in list_of_dicts:
            combobox.addItem(str(name))
            new_hbox = self.get_layout_of_dict(item_dict)
            parentWidget = QtGui.QWidget()
            parentWidget.setLayout(new_hbox)
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
            label = QtGui.QLabel(str(key), self)
            if type(data_dict[key]) == list:  # inner node
                combobox, stacked_layout = self.get_stacked_layout(data_dict[key])
                hbox = QtGui.QVBoxLayout()
                hbox.addWidget(label)
                hbox.addWidget(combobox)
                vbox.addLayout(hbox)
                vbox.addLayout(stacked_layout)
                self.widget_to_dict_entry[combobox] = data_dict[key]
                self.dict_entry_to_widget[id(data_dict[key])] = combobox
            else:  # leaf
                parameter_box = QtGui.QHBoxLayout()
                text_field = QtGui.QLineEdit(self)
                # Use the following small trick to obtain a reference of data_dict[key]
                self.widget_to_dict_entry[text_field] = data_dict[key]
                self.dict_entry_to_widget[id(data_dict[key])] = text_field
                parameter_box.addWidget(label)
                parameter_box.addWidget(text_field)
                vbox.addLayout(parameter_box)
        return vbox

    def initUI(self):
        # Get parameters for the environment
        self.parameter_settings = {'classType_of_population':getDictFromBaseClass(CPopulation.CBasePopulation), 'classType_of_environment':getDictFromBaseClass(CBaseEnvironment)}
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
        self.create_settings_button.clicked.connect(self.onCreateSettingsButtonClicked)
        hbox2.addWidget(self.create_settings_button)

        self.setLayout(hbox2)
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('Create settings for the simulation:')
        self.show()

    def onCreateSettingsButtonClicked(self):
        for widget in self.widget_to_dict_entry.keys():
            if type(widget) != QtGui.QComboBox:
                self.widget_to_dict_entry[widget].v = widget.text()
        print(self.parameter_settings)
        resulting_dict = self.create_dict_from_combobox_choice(self.parameter_settings)
        print(resulting_dict)
        new_settings = settings.CSimulationSettings()
        new_settings.settings_dict = resulting_dict
        new_settings.save_settings_to_file('Vergleich.txt')
        # ToDo: More markers. It's not enough to just test for  list. What is, when you really need a list as a parameter?

    def create_dict_from_combobox_choice(self, sub_dict):
        current_dict={}
        for key in sub_dict.keys():
            if type(sub_dict[key]) == list:
                selected_list_element = self.dict_entry_to_widget[id(sub_dict[key])].currentText()
                current_list = sub_dict[key]
                for elem in current_list:
                    # If the string representation of the first element of the current tuple matches the
                    # selected list element .....
                    if str(elem[0]) == selected_list_element:
                        # ... then deal with that 'subdictionary' in
                        current_dict[key] = elem[0]
                        if "classType_settings" not in current_dict:
                            current_dict["classType_settings"] = {}
                        current_dict["classType_settings"][key] = self.create_dict_from_combobox_choice(elem[1])
            else:
                # We saved everything as a reference. Now we want the real value
                current_dict[key] = jsonpickle.decode(sub_dict[key].v)
        return current_dict


def main():
    print(jsonpickle.encode(None))
    app = QtGui.QApplication(sys.argv)
    ex = Settings_Gui()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

"""
Notes:
# Get subclasses
for sc in CIndividual.CBaseIndividual.__subclasses__():
    print(sc.__name__)
"""
