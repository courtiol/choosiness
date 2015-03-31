__author__ = 'robert'

import sys
import CPopulation
from Environments.EnvironmentBase import CBaseEnvironment
from create_settings_with_gui import getDictFromBaseClass
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import settings

"""
Useful link for using QTreeView within python:
http://neurochannels.blogspot.de/2015/02/pyside-tree-model-vi-building-trees.html

"""

class Window(QWidget):

    def __init__(self, data_dictionary):
        QWidget.__init__(self)

        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)

        self.model = QStandardItemModel()
        self.addItems(self.model, data_dictionary)
        self.treeView.setModel(self.model)

        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels([self.tr("Parameter"), self.tr("Value")])

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)

    def addItems(self, parent, elements):
        print("addItems")
        print(elements)
        for class_type, dictionary in elements:
            new_parent_key = QStandardItem(str(class_type))
            new_parent_key.setCheckable(True)
            parent.appendRow(new_parent_key)
            for key in dictionary.keys():
                if type(dictionary[key]) is list:
                    new_child = QStandardItem(key)
                    new_parent_key.appendRow(new_child)
                    self.addItems(new_child, dictionary[key])
                    # self.addItems(new_parent_key, dictionary[key])
                else:
                    new_child = QStandardItem(key)
                    # dictionary[key] is always from type Reference. The actual value is saved under the key 'v'
                    new_value = QStandardItem(str(dictionary[key]['v']))
                    new_parent_key.appendRow([new_child, new_value])

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # parameter_settings = {'classType_of_population': getDictFromBaseClass(CPopulation.CBasePopulation),
    #                                    'classType_of_environment': getDictFromBaseClass(CBaseEnvironment)}
    parameter_settings = getDictFromBaseClass(CPopulation.CBasePopulation)
    print("Parametersettings")
    print(parameter_settings)

    print("--------------------------------------------------------")
    temp_settings = settings.CSimulationData('default_settings.txt')
    dict_test = [('settings', temp_settings.settings_dict)]
    print(dict_test)
    print("--------------------------------------------------------")


    # window = Window(parameter_settings)
    window = Window(dict_test)
    window.show()
    sys.exit(app.exec_())