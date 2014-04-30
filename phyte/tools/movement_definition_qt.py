from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.movement import MovementComponent, VaryingMovementComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class MovementDefinitionEditor(Editor):
    def __init__(self, context):
        super(MovementDefinitionEditor, self).__init__(context,
                                                       QtGui.QGroupBox('Movement'))
        # gui elements
        self.layout = QtGui.QGridLayout()
