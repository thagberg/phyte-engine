from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, UNIVERSE_ENTITY
from engine.inputs import Input
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class InputDefinitionEditor(Editor):
    def __init__(self, context):
        super(InputDefinitionEditor, self).__init__(context,
                                                   QtGui.QGroupBox('Input'))
        if 'inputs' not in self.context:
            self.context['inputs'] = list()
        self.layout = QtGui.QGridLayout()
        self.input_name_label = QtGui.QLabel('Input Name')
        self.input_name_field = QtGui.QLineEdit()
        self.input_list_view = QtGui.QListWidget()
        self.add_input_button = QtGui.QPushButton('Add Input')
        self.remove_input_button = QtGui.QPushButton('Remove Input')
        self.button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.layout.addWidget(self.input_name_label,0,0)
        self.layout.addWidget(self.input_name_field,0,1)
        self.layout.addWidget(self.input_list_view,1,0)
        self.button_layout.addWidget(self.add_input_button)
        self.button_layout.addWidget(self.remove_input_button)
        self.layout.addLayout(self.button_layout,1,1)

        self.group.setLayout(self.layout)

        # wire up events
        self.add_input_button.clicked.connect(self.add_input)
        self.remove_input_button.clicked.connect(self.remove_input)

    def add_input(self):
        inp_name = self.input_name_field.text()
        inp = Input(name=inp_name)
        inp_wrapper = Component(inp, inp_name)
        widget_component = WidgetItemComponent(inp_name, inp_wrapper)
        self.input_list_view.addItem(widget_component)

        # add input to the application context
        self.context['inputs'].append(inp_wrapper)

        # fire event for adding new input
        new_event = Event('added_input',
                          input_component=inp_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_input(self):
        selected_index = self.input_list_view.currentRow()
        selected_input = self.input_list_view.takeItem(selected_index)

        # remove the input from the application context
        self.context['inputs'].remove(selected_input.component)
