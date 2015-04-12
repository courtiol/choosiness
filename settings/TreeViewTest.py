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

        self.item_to_dict = {}

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
        if not item.isCheckable(): # check if item has children
            rep = self.item_to_dict[item.index()]
            rep['v'] = item.text()
            print(str(self.data_dictionary))
        elif item.checkState() == 0: # item unchecked; nothing needs to be done here (see checkState == 2)
            pass
        elif item.checkState() == 2: # item checked
            parent = item.parent() # take parent of the child
            if parent is None:
                parent = self.rootItem # invisible root is for some strange reason (bug?) never shown as parent in qt
            if parent == 0: # check if this parent exits
                print(str(item.text)+" has no parent")
            else: # when yes then ...
                if hasattr(parent, 'selectedChild') and (parent.selectedChild is not None): # check if it has already a child
                    if parent.selectedChild != item: # and if this child is not already this item
                        parent.selectedChild.setCheckState(0) # then set the check state of the previous item to
                        # to unchecked. (Only one item should be selected)
                parent.selectedChild = item # update the selected item of the parent
                print("selectedChild added to "+str(parent.text())+" "+str(parent))

    def addItems(self, parent, elements):
        for class_type, dictionary in elements: # elements is here a list of tuples. The second entry is always a
            # dictionary
            new_parent_key = QStandardItem(str(class_type)) # Create a checkable entry in the treeview
            new_parent_key.setCheckable(True)
            parent.appendRow(new_parent_key)

            if not hasattr(parent, 'children'):
                parent.children = []
            parent.children.append(new_parent_key)
            if not hasattr(parent, 'selectedChild'):
                parent.selectedChild = None

            for key in dictionary.keys(): # now take for every class type the corresponding dictionary
                if type(dictionary[key]) is list:
                    new_child = QStandardItem(key) # for each entry in the dictionary that is again a list
                    new_parent_key.appendRow(new_child)
                    if not hasattr(new_parent_key, 'children'):
                        new_parent_key.children = []
                    new_parent_key.children.append(new_child)
                    self.addItems(new_child, dictionary[key]) # perform a recursive step
                else: # otherwise just create an entry in the treeview ...
                    new_child = QStandardItem(key)
                    # dictionary[key] is always from type Reference. The actual value is saved under the key 'v'
                    new_value = QStandardItem(str(dictionary[key]['v'])) # ... with this value
                    new_parent_key.appendRow([new_child, new_value])
                    self.item_to_dict[new_value.index()] = dictionary[key]
                    if not hasattr(new_parent_key, 'children'):
                        new_parent_key.children = []
                    new_parent_key.children.append([new_child, new_value])

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

    def selectedChildtraversed(self, parent, selected_child):
        # print(str(parent)+" "+str(parent.text()))
        pass

    def unselectableChildTraversed(self, parent, child):
        pass

    def leafTraversed(self, leaf):
        new_child = leaf[0]
        new_value = leaf[1]
        # print("new_child: "+str(new_child.text())+", new_value: "+str(new_value.text()))

    def createDictFromUserChoice(self):
        resulting_dict = {}
        self.traverseTree(None, resulting_dict)
        return (resulting_dict['classType_settings'])['root']

    def traverseTree(self, root=None, parent_dict=None):
        """
        Create a dictionary compatible to settings.CSimulationSettings. This means for each combobox the selected
        key und subdirectory in the dictionary must be extracted
        """
        """
        We want to convert the user data is the following form:

        {
            "classType_settings":
            {
                "classType_of_environment":
                {
                    ...parameters
                }
            }
            "classType_of_environment":
            {

            }
        }
        """
        current_dict = {}
        if root is None:
            root = self.rootItem
        if parent_dict is None: # if parent_d
            parent_dict = {}
        if hasattr(root, 'selectedChild'): # if 'root' has a selected item then we need to create an classType_settings
            # entry and a classType_of_???? entry
            if root.selectedChild is not None: # The user selected an item. (he should always!)
                self.selectedChildtraversed(root, root.selectedChild)
                # child_dict = self.traverseTree(root.selectedChild, None)
                child_dict = self.traverseTree(root.selectedChild, current_dict) # get the settings of the selected child.

                class_name = ""
                if root == self.rootItem: # the root has no parameter text(). Therefore we need to deal with this case
                    # in a different way
                    class_name = "root"
                else:
                    class_name = str(root.text()) # otherwise take the label in the treeView

                if "classType_settings" not in parent_dict.keys(): # if there is no key 'classType_settings' create one.
                    parent_dict["classType_settings"] = {}
                (parent_dict["classType_settings"])[class_name] = child_dict # save the attributes in the parent dict
                current_dict = (root.selectedChild).text() # and the class name
        else:
            # otherwise iterate through all children
            if hasattr(root, 'children'):
                for child in root.children:
                    self.unselectableChildTraversed(root, child)
                    # temp_dict[str(child.text())] = "x"
                    childDict = self.traverseTree(child, current_dict) # get the dictionary starting in the current child
                    if hasattr(child, 'text'):
                        current_dict[child.text()] = childDict
                    else:
                        current_dict[str(child[0].text())] = childDict
            else:
                new_child = root[0]
                new_value = root[1]
                self.leafTraversed(root)

                current_dict = str(new_value.text())
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
        resulting_dict = self.settings_widget.createDictFromUserChoice()
        # Check what entries are selected in the comboboxes and retrieve from this the settings
        # Save these settings
        new_settings = settings.CSimulationData(None)
        new_settings.settings_dict = resulting_dict
        new_settings.save_settings_to_file('settings.txt')
        print(new_settings.settings_dict)

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