from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, UNIVERSE_ENTITY
from engine.execute import ExecutionComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class ExecutionDefinitionEditor(Editor):
    def __init__(self, context):
        super(ExecutionDefinitionEditor, self).__init__(context,
                                                        QtGui.QGroupBox('Execution'))
        # gui elements
        self.layout = QtGui.QGridLayout()
        self.exec_name_label = QtGui.QLabel('Execution Name')
        self.exec_name_field = QtGui.QLineEdit()
        self.binding_list_label = QtGui.QLabel('Select Binding')
        self.binding_list_view = QtGui.QListWidget()
        self.binding_layout = QtGui.QVBoxLayout()
        self.move_list_label = QtGui.QLabel('Select Moves')
        self.move_list_view = QtGui.QListWidget()
        self.move_layout = QtGui.QVBoxLayout()
        self.add_move_button = QtGui.QPushButton('Add Move')
        self.remove_move_button = QtGui.QPushButton('Remove Move')
        self.move_button_layout = QtGui.QVBoxLayout()
        self.selected_move_list = QtGui.QListWidget()
        self.exec_list_view = QtGui.QListWidget()
        self.add_exec_button = QtGui.QPushButton('Add Execution')
        self.remove_exec_button = QtGui.QPushButton('Remove Execution')
        self.exec_button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.layout.addWidget(self.exec_name_label,0,0)
        self.layout.addWidget(self.exec_name_field,0,1)
        self.binding_layout.addWidget(self.binding_list_label)
        self.binding_layout.addWidget(self.binding_list_view)
        self.layout.addLayout(self.binding_layout,1,0)
        self.move_layout.addWidget(self.move_list_label)
        self.move_layout.addWidget(self.move_list_view)
        self.layout.addWidget(self.move_list_view,1,1)
        self.move_button_layout.addWidget(self.add_move_button)
        self.move_button_layout.addWidget(self.remove_move_button)
        self.layout.addLayout(self.move_button_layout,1,2)
        self.layout.addWidget(self.selected_move_list,1,3)
        self.layout.addWidget(self.exec_list_view,2,0)
        self.exec_button_layout.addWidget(self.add_exec_button)
        self.exec_button_layout.addWidget(self.remove_exec_button)
        self.layout.addLayout(self.exec_button_layout,2,1)

        self.group.setLayout(self.layout)
