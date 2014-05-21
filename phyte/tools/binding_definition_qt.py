from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, UNIVERSE_ENTITY
from engine.inputs import Input, InputComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class BindingDefinitionEditor(Editor):
    def __init__(self, context):
        super(BindingDefinitionEditor, self).__init__(context,
                                                      QtGui.QGroupBox('Binding'))
        self.current_binding = None
        self.layout = QtGui.QGridLayout()
        self.binding_name_label = QtGui.QLabel('Binding Name')
        self.binding_name_field = QtGui.QLineEdit()
        self.inp_list_view = QtGui.QListWidget()
        self.selected_inp_list_view = QtGui.QListWidget()
        self.inp_layout = QtGui.QHBoxLayout()
        self.inp_button_layout = QtGui.QVBoxLayout()
        self.binding_list_view = QtGui.QListWidget()
        self.add_inp_button = QtGui.QPushButton('Add Input')
        self.remove_inp_button = QtGui.QPushButton('Remove Input')
        self.add_binding_button = QtGui.QPushButton('Add Binding')
        self.remove_binding_button = QtGui.QPushButton('Remove Binding')
        self.edit_binding_button = QtGui.QPushButton('Edit Binding')
        self.button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.layout.addWidget(self.binding_name_label,0,0)
        self.layout.addWidget(self.binding_name_field,0,1)
        self.inp_layout.addWidget(self.inp_list_view)
        self.inp_button_layout.addWidget(self.add_inp_button)
        self.inp_button_layout.addWidget(self.remove_inp_button)
        self.inp_layout.addLayout(self.inp_button_layout)
        self.inp_layout.addWidget(self.selected_inp_list_view)
        self.layout.addLayout(self.inp_layout,1,0,1,2)
        self.layout.addWidget(self.binding_list_view,2,0)
        self.button_layout.addWidget(self.add_binding_button)
        self.button_layout.addWidget(self.remove_binding_button)
        self.button_layout.addWidget(self.edit_binding_button)
        self.layout.addLayout(self.button_layout,2,1)

        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_bindings)
        EVENT_MAPPING.register_handler('added_input', self.new_input)
        EVENT_MAPPING.register_handler('removed_input', self.removed_input)

        # wire up events
        self.add_inp_button.clicked.connect(self.add_input)
        self.remove_inp_button.clicked.connect(self.remove_input)
        self.add_binding_button.clicked.connect(self.add_binding)
        self.remove_binding_button.clicked.connect(self.remove_binding)
        self.edit_binding_button.clicked.connect(self.edit_binding)
        self.binding_list_view.currentItemChanged.connect(self.select_binding)

    def add_input(self):
        selected_item = self.inp_list_view.currentItem()
        selected_component = selected_item.component
        widget_component = WidgetItemComponent(selected_component.text,
                                               selected_component)
        self.selected_inp_list_view.addItem(widget_component)

    def remove_input(self):
        selected_index = self.selected_inp_list_view.currentRow()
        selected_item = self.selected_inp_list_view.takeItem(selected_index)
        selected_component = selected_item.component

    def add_binding(self):
        entity = self.context['selected_entity']
        binding_name = str(self.binding_name_field.text())
        # begin by building the bindings dictionary
        bindings = dict()
        for i in range(self.selected_inp_list_view.count()):
            input_comp = self.selected_inp_list_view.item(i).component
            key= input_comp.text
            bindings[key] = input_comp

        binding_comp = InputComponent(entity_id=entity,
                                      bindings=bindings)
        binding_comp_wrapper = Component(binding_comp, binding_name)
        widget_component = WidgetItemComponent(binding_name, binding_comp_wrapper)
        self.binding_list_view.addItem(widget_component)

        # add the component to the application context
        self.context['entities'][entity]['components']['binding'].append(binding_comp_wrapper)

        # fire event for adding new binding
        new_event = Event('added_binding',
                          binding_component=binding_comp_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('added_component',
                          entity=entity,
                          component_type='binding',
                          component=binding_comp_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_binding(self):
        entity = self.context['selected_entity']
        selected_index = self.binding_list_view.currentRow()
        selected_item = self.binding_list_view.takeItem(selected_index)
        selected_component = selected_item.component

        # remove the component from the application context
        self.context['entities'][entity]['components']['binding'].remove(selected_component)

        # fire event for removing binding
        new_event = Event('removed_binding',
                          binding_component=selected_component)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='binding',
                          component=selected_component)
        EVENT_MANAGER.fire_event(new_event)

    def select_binding(self):
        selected_item = self.binding_list_view.currentItem()
        if selected_item is not None:
            selected_component = selected_item.component
            self.current_binding = selected_component

            # do a soft clear of the selected inputs
            for i in range(self.selected_inp_list_view.count()-1,-1,-1):
                item = self.selected_inp_list_view.takeItem(i)

            # repopulate with the bound inputs for this binding component
            for key, comp in self.current_binding.component.bindings.iteritems():
                widget_component = WidgetItemComponent(key, comp)
                self.selected_inp_list_view.addItem(widget_component)

    def set_bindings(self, event):
        entity = event.entity
        available_bindings = self.context['entities'][entity]['components']['binding']
        # do a "soft" clear of the list
        # if we actually call self.graphic_list_view.clear(),
        # the C++ Qt objects will be deleted
        for i in range(self.binding_list_view.count()-1,-1,-1):
            self.binding_list_view.takeItem(i)

        for binding in available_bindings:
            widget_component = WidgetItemComponent(binding.text, binding)
            self.binding_list_view.addItem(widget_component)
    
    def new_input(self, event):
        widget_component = WidgetItemComponent(event.input_component.text, 
                                               event.input_component)
        self.inp_list_view.addItem(widget_component) 

    def removed_input(self, event):
        for i in range(self.inp_list_view.count()-1,-1,-1):
            item = self.inp_list_view.item(i)
            inp = item.component
            if event.input_component == inp:
                self.inp_list_view.takeItem(i)

    def edit_binding(self):
        bindings = dict()
        for i in range(self.selected_inp_list_view.count()):
            input_comp = self.selected_inp_list_view.item(i).component
            key= input_comp.text
            bindings[key] = input_comp

    def update(self):
        # first update input list
        self.inp_list_view.clear()
        for inp in self.context['inputs']:
            widget_component = WidgetItemComponent(inp.text, inp)
            self.inp_list_view.addItem(widget_component)

        # then update binding list
        entity = self.context['selected_entity']
        self.binding_list_view.clear()
        if entity and entity != '':
            for bind in self.context['entities'][entity]['components']['binding']:
                widget_component = WidgetItemComponent(binding.text, binding)
                self.binding_list_view.addItem(widget_component)
