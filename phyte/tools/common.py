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


class ComponentListModel(Qt.QAbstractListModel):
    def __init__(self, parent=None):
        super(ComponentListModel, self).__init__(parent)

    def rowCount(self, parent=Qt.QModelIndex()):
        pass

    def data(self, index, role=QtCore.Qt.DisplayRole):
        pass
