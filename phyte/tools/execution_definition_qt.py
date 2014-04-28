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
        self.selected_move_list_view = QtGui.QListWidget()
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
        self.layout.addWidget(self.selected_move_list_view,1,3)
        self.layout.addWidget(self.exec_list_view,2,0)
        self.exec_button_layout.addWidget(self.add_exec_button)
        self.exec_button_layout.addWidget(self.remove_exec_button)
        self.layout.addLayout(self.exec_button_layout,2,1)

        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_entity)
        EVENT_MAPPING.register_handler('added_binding', self.added_binding)
        EVENT_MAPPING.register_handler('removed_binding', self.removed_binding)
        EVENT_MAPPING.register_handler('added_move', self.added_move)
        EVENT_MAPPING.register_handler('removed_move', self.removed_move)

        # wire up events
        self.add_move_button.clicked.connect(self.add_move)
        self.remove_move_button.clicked.connect(self.remove_move)
        self.add_exec_button.clicked.connect(self.add_exec)
        self.remove_exec_button.clicked.connect(self.remove_exec)
        self.exec_list_view.currentItemChanged.connect(self.select_exec)

    def add_move(self):
        selected_item = self.move_list_view.currentItem()
        selected_component = selected_item.component
        widget_component = WidgetItemComponent(selected_component.text,
                                               selected_component)
        self.selected_move_list_view.addItem(widget_component)

    def remove_move(self):
        selected_index = self.selected_move_list_view.currentRow()
        selected_item = self.selected_move_list_view.takeItem(selected_index)

    def add_exec(self):
        entity = self.context['selected_entity']
        exec_name = self.exec_name_field.text()
        binding = self.binding_list_view.currentItem().component
        # build list of selected moves
        moves = list()
        for i in range(self.selected_move_list_view.count()):
            item = self.selected_move_list_view.item(i)
            move = item.component
            moves.append(move)
        exec_component = ExecutionComponent(entity_id=entity,
                                            executables=moves,
                                            inputs=binding)
        exec_component_wrapper = Component(exec_component, exec_name)
        widget_component = WidgetItemComponent(exec_name, exec_component_wrapper)
        self.exec_list_view.addItem(widget_component)
        
        # add execution component to the application context
        self.context['entities'][entity]['components']['execution'].append(exec_component_wrapper)

        # fire event for adding new execution
        new_event = Event('added_execution',
                          execution_component=exec_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('added_component',
                          entity=entity,
                          component_type='execution',
                          component=exec_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_exec(self):
        entity = self.context['selected_entity']
        selected_index = self.exec_list_view.currentRow()
        selected_item = self.exec_list_view.takeItem(selected_index)
        selected_component = selected_item.component

        # remove execution component from the application context
        self.context['entities'][entity]['components']['execution'].remove(selected_component)

        # fire event for removing execution
        new_event = Event('removed_execution',
                          execution_component=selected_component)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='execution',
                          component=selected_component)
        EVENT_MANAGER.fire_event(new_event)

    def select_exec(self):
        pass

    def set_entity(self, event):
        entity = event.entity
        bindings = self.context['entities'][entity]['components']['binding']
        # do a "soft" clear of the list
        # if we actually call self.graphic_list_view.clear(),
        # the C++ Qt objects will be deleted
        for i in range(self.binding_list_view.count()-1,-1,-1):
            self.binding_list_view.takeItem(i)

        for binding in bindings:
            widget_component = WidgetItemComponent(binding.text, binding)
            self.binding_list_view.addItem(widget_component)

        execs = self.context['entities'][entity]['components']['execution']
        for i in range(self.exec_list_view.count()-1,-1,-1):
            self.exec_list_view.takeItem(i)

        for exec_comp in execs:
            widget_component = WidgetItemComponent(exec_comp.text, exec_comp)
            self.exec_list_view.addItem(widget_component)

    def added_binding(self, event):
        binding_component = event.binding_component
        widget_component = WidgetItemComponent(binding_component.text,
                                               binding_component)
        self.binding_list_view.addItem(widget_component)

    def removed_binding(self, event):
        binding_component = event.binding_component
        for i in range(self.binding_list_view.count()-1,-1,-1):
            comp = self.binding_list_view.item(i).component
            if comp == binding_component:
                self.binding_list_view.takeItem(i)
                return

    def added_move(self, event):
        move_component = event.move_component
        widget_component = WidgetItemComponent(move_component.text, move_component)
        self.move_list_view.addItem(widget_component)

    def removed_move(self, event):
        move_component = event.move_component

        # find the given move component and remove it
        for i in range(self.move_list_view.count()):
            item = self.move_list_view.item(i)
            component = item.component
            if component == move_component:
                self.move_list_view.takeItem(i)
                break
