from PyQt4 import QtGui, QtCore
from pygame import Rect

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.physics2d import PhysicsComponent
from engine.common import BoxComponent, Vector2
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class PhysicsDefinitionEditor(Editor):
    def __init__(self, context):
        super(PhysicsDefinitionEditor, self).__init__(context, QtGui.QGroupBox('Physics'))
        self.entity = None
        # set up gui
        self.layout = QtGui.QGridLayout()
        self.name_label = QtGui.QLabel('Physics Object Name')
        self.name_field = QtGui.QLineEdit()
        self.x_label = QtGui.QLabel('X')
        self.x_field = QtGui.QLineEdit()
        self.y_label = QtGui.QLabel('Y')
        self.y_field = QtGui.QLineEdit()
        self.w_label = QtGui.QLabel('Width')
        self.w_field = QtGui.QLineEdit()
        self.h_label = QtGui.QLabel('Height')
        self.h_field = QtGui.QLineEdit()
        self.physics_list_view = QtGui.QListWidget()
        self.add_physics_button = QtGui.QPushButton('Add Physics Object')
        self.remove_physics_button = QtGui.QPushButton('Remove Physics Object')
        self.button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.layout.addWidget(self.name_label,0,0)
        self.layout.addWidget(self.name_field,0,1)
        self.layout.addWidget(self.x_label,1,0)
        self.layout.addWidget(self.x_field,1,1)
        self.layout.addWidget(self.w_label,1,2)
        self.layout.addWidget(self.w_field,1,3)
        self.layout.addWidget(self.y_label,2,0)
        self.layout.addWidget(self.y_field,2,1)
        self.layout.addWidget(self.h_label,2,2)
        self.layout.addWidget(self.h_field,2,3)
        self.layout.addWidget(self.physics_list_view,3,0)
        self.button_layout.addWidget(self.add_physics_button)
        self.button_layout.addWidget(self.remove_physics_button)
        self.layout.addLayout(self.button_layout,3,1)

        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_entity)

        # wire up events
        self.add_physics_button.clicked.connect(self.add_physics)
        self.remove_physics_button.clicked.connect(self.remove_physics)

    def add_physics(self):
        name = str(self.name_field.text())
        x = int(self.x_field.text())
        y = int(self.y_field.text())
        w = int(self.w_field.text())
        h = int(self.h_field.text())
        rect = Rect(0,0,w,h)
        rect_wrapper = Component(rect, str(rect))
        anchor = Vector2(self.entity, (x, y))
        anchor_wrapper = Component(anchor, str(anchor))
        self.context['entities'][self.entity]['components']['vector'].append(anchor_wrapper)
        box_component = BoxComponent(entity_id=self.entity,
                                     rect=rect,
                                     anchor=anchor_wrapper,
                                     hitactive=False,
                                     hurtactive=False,
                                     blockactive=False,
                                     solid=True)
        box_wrapper = Component(box_component, str(rect))
        # add this box to the application context and fire respective events
        self.context['entities'][self.entity]['components']['hitbox'].append(box_wrapper)
        new_event = Event('added_component',
                         entity=self.entity,
                         component_type='hitbox',
                         component=box_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        physics_component = PhysicsComponent(entity_id=self.entity,
                                             box=box_wrapper,
                                             body=rect_wrapper)
        physics_wrapper = Component(physics_component, name)
        widget_component = WidgetItemComponent(physics_wrapper.text,
                                               physics_wrapper)
        self.physics_list_view.addItem(widget_component)
        self.context['entities'][self.entity]['components']['physics'].append(physics_wrapper)
        new_event = Event('added_component',
                          entity=self.entity,
                          component_type='physics',
                          component=physics_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('physics_added',
                          physics_component=physics_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_physics(self):
        selected_index = self.physics_list_view.currentRow()
        selected_item = self.physics_list_view.takeItem(selected_index)
        selected_component = selected_item.component
        self.context['entities'][self.entity]['components']['physics'].remove(selected_component)
        new_event = Event('removed_component',
                          entity=self.entity,
                          component_type='physics',
                          component=selected_component)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('physics_removed',
                          physics_component=selected_component)
        EVENT_MANAGER.fire_event(new_event)
        # remove any hitboxes and concomitant components
        box = selected_component.component.body
        self.context['entities'][self.entity]['components']['hitbox'].remove(box)
        anchor = box.component.anchor
        self.context['entities'][self.entity]['components']['vector'].remove(anchor)

    def set_entity(self, event):
        entity = event.entity
        self.entity = entity

        # soft clear physics object list
        for i in range(self.physics_list_view.count()-1,-1,-1):
            self.physics_list_view.takeItem(i)

        available_physics = self.context['entities'][entity]['components']['physics']
        for phys in available_physics:
            widget_component = WidgetItemComponent(phys.text, phys)
            self.physics_list_view.addItem(widget_component)

    def update(self):
        entity = self.context['selected_entity']

        self.physics_list_view.clear()
