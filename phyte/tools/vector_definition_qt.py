from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.common import Vector2
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class VectorDefinitionEditor(Editor):
    def __init__(self, context):
        super(VectorDefinitionEditor, self).__init__(context, QtGui.QGroupBox('Vectors'))
        # setup gui stuff
        self.layout = QtGui.QGridLayout()
        self.vector_name_label = QtGui.QLabel('Vector Name')
        self.vector_name_field = QtGui.QLineEdit()
        self.x_label = QtGui.QLabel('X')
        self.x_field = QtGui.QLineEdit()
        self.y_label = QtGui.QLabel('Y')
        self.y_field = QtGui.QLineEdit()
        self.vector_list_view = QtGui.QListWidget()
        self.add_vector_button = QtGui.QPushButton('Add Vector')
        self.remove_vector_button = QtGui.QPushButton('Remove Vector')
        self.button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.layout.addWidget(self.vector_name_label,0,0)
        self.layout.addWidget(self.vector_name_field,0,1)
        self.layout.addWidget(self.x_label,1,0)
        self.layout.addWidget(self.x_field,1,1)
        self.layout.addWidget(self.y_label,2,0)
        self.layout.addWidget(self.y_field,2,1)
        self.layout.addWidget(self.vector_list_view,3,0)
        self.button_layout.addWidget(self.add_vector_button)
        self.button_layout.addWidget(self.remove_vector_button)
        self.layout.addLayout(self.button_layout,3,1)

        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_entity)

        # wire up events
        self.add_vector_button.clicked.connect(self.add_vector)
        self.remove_vector_button.clicked.connect(self.remove_vector)

    def update(self):
        entity = self.context['selected_entity']
        self.vector_list_view.clear()
        if entity is not None and entity != '':
            for vector in self.context['entities'][entity]['components']['vector']:
                widget_component = WidgetItemComponent(vector.text, vector)
                self.vector_list_view.addItem(widget_component)

    def add_vector(self):
        entity = self.context['selected_entity']
        x = float(self.x_field.text())
        y = float(self.y_field.text())
        name = str(self.vector_name_field.text())
        vector = Vector2(entity, [x, y])
        vector_wrapper = Component(vector, name)
        widget_component = WidgetItemComponent(vector_wrapper.text, vector_wrapper)
        self.vector_list_view.addItem(widget_component)
        self.context['entities'][entity]['components']['vector'].append(vector_wrapper)
        new_event = Event('added_component',
                          entity=entity,
                          component_type='vector',
                          component=vector_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('vector_added',
                          vector_component=vector_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_vector(self):
        entity = self.context['selected_entity']
        selected_index = self.vector_list_view.currentRow()
        selected_item = self.vector_list_view.takeItem(selected_index)
        selected_component = selected_item.component
        self.context['entities'][entity]['components']['vector'].remove(selected_component)
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='vector',
                          component=selected_component)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('vector_removed',
                          vector_component=selected_component)
        EVENT_MANAGER.fire_event(new_event)

    def set_entity(self, event):
        entity = event.entity
        # soft clear the vector list
        for i in range(self.vector_list_view.count()-1,-1,-1):
            item = self.vector_list_view.takeItem(i)

        # then repopulate
        for vector in self.context['entities'][entity]['components']['vector']:
            widget_component = WidgetItemComponent(vector.text, vector)
            self.vector_list_view.addItem(widget_component)
