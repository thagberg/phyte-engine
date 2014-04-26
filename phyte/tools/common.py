from PyQt4 import QtGui, Qt, QtCore

WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
PURPLE = (255, 0, 255, 255)
YELLOW = (255, 255, 0, 255)
BLACK = (0, 0, 0, 255)
TRANS = (0, 0, 0, 0)
GRAY = (225, 225, 225, 255)

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

ENTITY_ID = -1

UNIVERSE_ENTITY = 'universe'

class Component(object):
    def __init__(self, component, text):
        super(Component, self).__init__()
        self.component = component
        self.text = text
        self.type_name = self.component.__class__.__name__


class WidgetItemComponent(QtGui.QListWidgetItem):
    def __init__(self, item_text, component):
        super(WidgetItemComponent, self).__init__(item_text)
        self.component = component


class TreeWidgetItemComponent(QtGui.QTreeWidgetItem):
    def __init__(self, item_text, component):
        super(TreeWidgetItemComponent, self).__init__()
        self.component = component
        self.setText(0, item_text)


class ComponentListModel(QtCore.QAbstractListModel):
    def __init__(self, components=None, parent=None):
        super(ComponentListModel, self).__init__(parent)
        self.components = components if components else list()

    def rowCount(self, parent=Qt.QModelIndex()):
        return len(self.components)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.components):
            return Qt.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return self.components[index.row()].text

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid and role == QtCore.Qt.EditRole:
            self.components[index] = value
            self.dataChanged.emit(QtCore.QModelIndex(),
                                  QtCore.QModelIndex())
            return true

    def add_component(self, component):
        self.components.append(component)
        self.dataChanged.emit(QtCore.QModelIndex(),
                              QtCore.QModelIndex())

    def remove_component(self, component):
        try:
            self.components.remove(component)
            self.dataChanged.emit(QtCore.QModelIndex(),
                                  QtCore.QModelIndex())
        except:
            return None

