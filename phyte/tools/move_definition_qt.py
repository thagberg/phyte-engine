from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.move import MoveComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class MoveDefinitionEditor(Editor):
    def __init__(self, context):
        super(MoveDefinitionEditor, self).__init__(context,
                                                   QtGui.QGroupBox('Move'))
