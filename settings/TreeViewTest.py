__author__ = 'robert'

import sys
import CPopulation
from Environments.EnvironmentBase import CBaseEnvironment
from create_settings_with_gui import getDictFromBaseClass
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import settings
import jsonpickle

"""
Useful link for using QTreeView within python:
http://neurochannels.blogspot.de/2015/02/pyside-tree-model-vi-building-trees.html

"""

class WidgetFromDict(QWidget):

    def __init__(self, data_dictionary):
        QWidget.__init__(self)

        # --------------------------------------------
        self.parameters = data_dictionary
        self.data_dictionary = [('settings', data_dictionary)]
        print(self.data_dictionary)

        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)

        self.dict_to_item = {}

        self.model = QStandardItemModel()
        self.rootItem = self.model.invisibleRootItem()
        self.addItems(self.rootItem, self.data_dictionary)
        self.treeView.setModel(self.model)

        self.model.itemChanged.connect(self.on_item_changed)


        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels([self.tr("Parameter"), self.tr("Value")])

        # ---------------------------------------------

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)

    def on_item_changed(self, item):
        # print(item.checkState())
        if not item.isCheckable():
            rep = self.item_to_dict[item.index()]
            rep['v'] = item.text()
            print(str(self.data_dictionary))
        elif item.checkState() == 0: # item unchecked
            pass
        elif item.checkState() == 2: # item checked
            parent = item.parent()
            if parent == 0:
                print("1")
                print(str(item.text)+" has no parent")
            elif parent is not None:
                print("2")
                if hasattr(parent, 'selectedChild'):
                    if parent.selectedChild != item:
                        parent.selectedChild.setCheckState(0)
                parent.selectedChild = item
        # some useful stuff:
        # item.checkState()

    def addItems(self, parent, elements):
        for class_type, dictionary in elements:
            new_parent_key = QStandardItem(str(class_type))
            new_parent_key.setCheckable(True)
            parent.appendRow(new_parent_key)
            for key in dictionary.keys():
                if type(dictionary[key]) is list:
                    new_child = QStandardItem(key)
                    new_parent_key.appendRow(new_child)
                    self.addItems(new_child, dictionary[key])
                else:
                    new_child = QStandardItem(key)
                    # dictionary[key] is always from type Reference. The actual value is saved under the key 'v'
                    new_value = QStandardItem(str(dictionary[key]['v']))
                    new_parent_key.appendRow([new_child, new_value])
                    self.item_to_dict[new_value.index()] = dictionary[key]

    def openMenu(self, position):
        indexes = self.treeView.selectedIndexes()

        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()

        menu.addAction(self.tr("Edit Value"))
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def create_dict_from_selection(self, sub_dict=None):
        """
        Create a dictionary compatible to settings.CSimulationSettings. This means for each combobox the selected
        key und subdirectory in the dictionary must be extracted
        """
        if sub_dict is None:
            sub_dict = self.parameters
        print(sub_dict)

        current_dict = {}  # create a new dictionary to store the data
        for key in sub_dict.keys():  # iterate over the input dictionary
            # if an entry is a list, the list entry selected in the combobox must be selected
            if type(sub_dict[key]) == list:
                # Get this entry with 'self.dict_entry_to_widget'
                print("Test1 "+str(sub_dict[key]))
                selected_dict = self.get_selected_list_element(sub_dict[key])
                print("Test2 "+str(selected_dict))
                # current_list = sub_dict[key]  # save for convenience this list
                if "classType_settings" not in current_dict:
                     current_dict["classType_settings"] = {}
                current_dict["classType_settings"][key] = self.create_dict_from_selection(selected_dict)
                """
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
                """
            else:
                # We saved everything as a reference. Now we want the real value
                print("leaf: "+str(sub_dict[key]))
                current_dict[key] = jsonpickle.decode(sub_dict[key]['v'])
        return current_dict

    def get_selected_list_element(self, elements):
        for class_type, dictionary in elements:
            print("check state from "+str(class_type)+" is "+str(self.dict_to_item[str(class_type)].checkState()))
            if self.dict_to_item[str(class_type)].checkState() == 2:
                return dictionary
        return None

    def print_dict_to_item(self):
        for key in self.dict_to_item.keys():
            print(str(key)+" - "+str(self.dict_to_item[key].text()))
            print("check state from "+str(self.dict_to_item[key].text())+" is "+str(self.dict_to_item[key].checkState()))


class SettingsGui(QWidget):
    """
    Creates dynamically a gui for the settings of the simulation, where all implementations of
    CPopulation.CBasePopulation and CBaseEnvironment can be selected. To do that the 'inspect' module is used. The
    constructor of each class is iterated. For each parameter in the constructor that is by itself a derived class
    of any base class the necessary settings are recursively extracted.
    """
    def __init__(self):
        super(SettingsGui, self).__init__()
        self.initUI()

    def initUI(self):
        temp_settings = settings.CSimulationData('default_settings.txt')
        self.settings_widget = WidgetFromDict(temp_settings.settings_dict)

        hbox = QVBoxLayout()
        hbox.addWidget(self.settings_widget)

        self.create_settings_button = QPushButton('Create Settings', self)
        self.create_settings_button.clicked.connect(self.on_create_settings_button_clicked)
        hbox.addWidget(self.create_settings_button)

        self.set_as_default_button = QPushButton('Set as default', self)
        self.set_as_default_button.clicked.connect(self.on_set_as_default_button_clicked)
        hbox.addWidget(self.set_as_default_button)

        self.setLayout(hbox)
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('Create settings for the simulation:')
        self.show()

    def on_create_settings_button_clicked(self):
        """
        Save the settings in a to settings.CSimulationSettings compatible format
        """
        resulting_dict = self.settings_widget.create_dict_from_selection()
        # Check what entries are selected in the comboboxes and retrieve from this the settings
        # Save these settings
        new_settings = settings.CSimulationData(None)
        new_settings.settings_dict = resulting_dict
        new_settings.save_settings_to_file('settings.txt')
        print(new_settings.settings_dict)
        # ToDo: More markers. It's not enough to just test for  list. What is, when you really need a list as a parameter?

    def on_set_as_default_button_clicked(self):
        self.settings_widget.print_dict_to_item()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Take 'default_settings.txt' as template
    temp_settings = settings.CSimulationData('default_settings.txt')

    # window = Window(parameter_settings)
    # window = WidgetFromDict(temp_settings.settings_dict)
    window = SettingsGui()
    window.show()
    sys.exit(app.exec_())