from collections import defaultdict

from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from engine.entity import Entity
from common import Component, WidgetItemComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class EntityDefinitionEditor(Editor):
    def __init__(self, context):
        super(EntityDefinitionEditor, self).__init__(context, QtGui.QGroupBox('Entity'))
        if 'entities' not in self.context:
            self.context['entities'] = dict()
        # define gui elements
        self.layout = QtGui.QGridLayout()
        self.entity_name_field = QtGui.QLineEdit()
        self.entity_name_label =  QtGui.QLabel('Entity Name')
        self.add_entity_button = QtGui.QPushButton('Add Entity')
        self.entity_list_view = QtGui.QListWidget()

        # layout
        self.layout.addWidget(self.entity_name_label,0,0)
        self.layout.addWidget(self.entity_name_field,0,1)
        self.layout.addWidget(self.add_entity_button,0,2)
        self.layout.addWidget(self.entity_list_view,1,0)

        self.group.setLayout(self.layout)

        # register events
        self.add_entity_button.clicked.connect(self.add_entity)
        self.entity_list_view.currentItemChanged.connect(self.select_entity)

    def add_entity(self):
        entity_name = self.entity_name_field.text()
        new_entity = Entity(entity_name)
        new_entity_wrapper = Component(new_entity, entity_name)
        widget_component = WidgetItemComponent(entity_name, new_entity_wrapper)
        self.entity_list_view.addItem(widget_component)
        self.context['entities'][entity_name] = dict()
        self.context['entities'][entity_name]['entity'] = new_entity
        self.context['entities'][entity_name]['components'] = defaultdict(list)

    def select_entity(self, current, previous):
        self.context['selected_entity'] = current.text()
        new_event = Event('selected_entity',
                          entity=self.context['selected_entity'])
        EVENT_MANAGER.fire_event(new_event)
