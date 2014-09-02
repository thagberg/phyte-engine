from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, TreeWidgetItemComponent
from engine.movement import MovementComponent, VaryingMovementComponent, BodyComponent
from engine.common import Vector2
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class BodyDefinitionEditor(Editor):
    def __init__(self, context):
        super(BodyDefinitionEditor, self).__init__(context,
                                                   QtGui.QGroupBox('Body'))
        # gui elements
        self.layout = QtGui.QGridLayout()
        self.body_name_label = QtGui.QLabel('Body Name')
        self.body_name_field = QtGui.QLineEdit()
        self.position_label = QtGui.QLabel('Position')
        self.position_list_view = QtGui.QListWidget()
        self.position_layout = QtGui.QVBoxLayout()
        self.body_list_view = QtGui.QListWidget()
        self.add_body_button = QtGui.QPushButton('Add Body')
        self.update_body_button = QtGui.QPushButton('Update Body')
        self.remove_body_button = QtGui.QPushButton('Remove Body')
        self.button_layout = QtGui.QVBoxLayout()

        # setup layout
        self.layout.addWidget(self.body_name_label,0,0)
        self.layout.addWidget(self.body_name_field,0,1)
        self.position_layout.addWidget(self.position_label)
        self.position_layout.addWidget(self.position_list_view)
        self.layout.addLayout(self.position_layout,1,0)
        self.layout.addWidget(self.body_list_view,2,0)
        self.button_layout.addWidget(self.add_body_button)
        self.button_layout.addWidget(self.update_body_button)
        self.button_layout.addWidget(self.remove_body_button)
        self.layout.addLayout(self.button_layout,2,1)

        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_entity)
        EVENT_MAPPING.register_handler('vector_added', self.add_vector)
        EVENT_MAPPING.register_handler('vector_removed', self.remove_vector)

        # wire up events
        self.add_body_button.clicked.connect(self.add_body)
        self.update_body_button.clicked.connect(self.update_body)
        self.remove_body_button.clicked.connect(self.remove_body)
        self.body_list_view.currentItemChanged.connect(self.select_body)

    def add_body(self):
        entity = self.context['selected_entity']
        name = str(self.body_name_field.text())
        selected_pos = self.position_list_view.currentItem().component
        velocity = Vector2(entity_id=entity, vec=(0, 0))
        velocity_component = Component(velocity, str(velocity))
        self.context['entities'][entity]['components']['vector'].append(velocity_component)

        # create body component object
        body_component = BodyComponent(entity_id=entity,
                                       body=selected_pos,
                                       velocity=velocity_component)
        body_component_wrapper = Component(body_component, name)
        widget_item = WidgetItemComponent(name, body_component_wrapper)
        self.body_list_view.addItem(widget_item)
        self.context['entities'][entity]['components']['body'].append(body_component_wrapper)

        # fire event
        new_event = Event('added_component',
                          entity=entity,
                          component_type='body',
                          component=body_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)


    def update_body(self):
        pass

    def remove_body(self):
        entity = self.context['selected_entity']
        selected_index = self.body_list_view.currentRow()
        selected_item = self.body_list_view.takeItem(selected_index)
        selected_component = selected_item.component

        # remove from context
        self.context['entities'][entity]['components']['body'].remove(selected_component)

        # fire event
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='body',
                          component=selected_component)
        EVENT_MANAGER.fire_event(new_event)

    def select_body(self):
        pass

    def set_entity(self, event):
        entity = event.entity

        # clear the body list
        self.body_list_view.clear()

        # clear the position list
        self.position_list_view.clear()

        # populate body list
        for component in self.context['entities'][entity]['components']['body']:
            widget_item = WidgetItemComponent(component.text, component)
            self.body_list_view.addItem(widget_item)

        # populate position list
        for component in self.context['entities'][entity]['components']['vector']:
            widget_item = WidgetItemComponent(component.text, component)
            self.position_list_view.addItem(widget_item)

    def add_vector(self, event):
        vector_component = event.vector_component
        widget_item = WidgetItemComponent(vector_component.text, 
                                          vector_component)
        self.position_list_view.addItem(widget_item)

    def remove_vector(self, event):
        vector_component = event.vector_component
        count = self.position_list_view.count()
        for i in xrange(count-1,-1,-1):
            current_vector = self.position_list_view.item(i)
            if current_vector.component == vector_component:
                self.position_list_view.takeItem(i)

    def update(self):
        entity = self.context['selected_entity']

        # clear boxes
        self.body_list_view.clear()
        self.position_list_view.clear()
        # if we have an entity, repopulate boxes
        if entity and entity != '':
            # populate body list
            for component in self.context['entities'][entity]['components']['body']:
                widget_item = WidgetItemComponent(component.text, component)
                self.body_list_view.addItem(widget_item)

            # populate position list
            for component in self.context['entities'][entity]['components']['vector']:
                widget_item = WidgetItemComponent(component.text, component)
                self.position_list_view.addItem(widget_item)
