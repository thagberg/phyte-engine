from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.move import MoveComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class MoveDefinitionEditor(Editor):
    def __init__(self, context):
        super(MoveDefinitionEditor, self).__init__(context,
                                                   QtGui.QGroupBox('Move'))
        self.selected_animation = None

        # gui elements
        self.layout = QtGui.QGridLayout()
        self.move_name_label = QtGui.QLabel('Move Name')
        self.move_name_field = QtGui.QLineEdit()
        self.ani_picker_label = QtGui.QLabel('Choose Animation')
        self.ani_list_view = QtGui.QListWidget()
        self.ani_picker_layout = QtGui.QVBoxLayout()
        self.inp_picker_label = QtGui.QLabel('Choose Inputs')
        self.inp_list_view = QtGui.QListWidget()
        self.selected_inp_list_view = QtGui.QListWidget()
        self.inp_layout = QtGui.QHBoxLayout()
        self.inp_select_layout = QtGui.QVBoxLayout()
        self.add_inps_button = QtGui.QPushButton('Add Inputs')
        self.remove_inps_button = QtGui.QPushButton('Remove Inputs')
        self.inps_button_layout = QtGui.QVBoxLayout()
        self.move_list_view = QtGui.QListWidget()
        self.add_move_button = QtGui.QPushButton('Add Move')
        self.remove_move_button = QtGui.QPushButton('Remove Move')
        self.move_button_layout = QtGui.QVBoxLayout()

        # misc
        self.inp_list_view.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        # set up layout
        self.layout.addWidget(self.move_name_label,0,0)
        self.layout.addWidget(self.move_name_field,0,1)
        self.ani_picker_layout.addWidget(self.ani_picker_label)
        self.ani_picker_layout.addWidget(self.ani_list_view)
        self.layout.addLayout(self.ani_picker_layout,1,0)
        self.inp_select_layout.addWidget(self.inp_picker_label)
        self.inp_select_layout.addWidget(self.inp_list_view)
        self.inp_layout.addLayout(self.inp_select_layout)
        self.inps_button_layout.addWidget(self.add_inps_button)
        self.inps_button_layout.addWidget(self.remove_inps_button)
        self.inp_layout.addLayout(self.inps_button_layout)
        self.inp_layout.addWidget(self.selected_inp_list_view)
        self.layout.addLayout(self.inp_layout,1,1)
        self.layout.addWidget(self.move_list_view,2,0)
        self.move_button_layout.addWidget(self.add_move_button)
        self.move_button_layout.addWidget(self.remove_move_button)
        self.layout.addLayout(self.move_button_layout,2,1)

        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('added_input', self.new_input)
        EVENT_MAPPING.register_handler('removed_input', self.removed_input)
        EVENT_MAPPING.register_handler('selected_entity', self.set_animations)
        EVENT_MAPPING.register_handler('added_animation', self.add_animation)
        EVENT_MAPPING.register_handler('removed_animation', self.remove_animation)


        # wire up events
        self.ani_list_view.currentItemChanged.connect(self.select_animation)
        self.add_inps_button.clicked.connect(self.add_inputs)
        self.remove_inps_button.clicked.connect(self.remove_inputs)
        self.add_move_button.clicked.connect(self.add_move)
        self.remove_move_button.clicked.connect(self.remove_move)

    def select_animation(self, current, previous):
        if current is not None:
            self.selected_animation = current.component

    def add_inputs(self):
        # possible multiple selection
        selected_items = self.inp_list_view.selectedItems()
        widget_component = None
        if len(selected_items) > 0:
            # if multiple items selected, join each component's
            # text together, and use the list of components as the
            # component
            text = ' + '.join([str(x.text()) for x in selected_items])
            agg_comp = Component([x.component for x in selected_items],
                                 text)
            widget_component = WidgetItemComponent(text, agg_comp)
        elif len(selected_items) == 1:
            # if just one item selected, follow the normal process
            comp = Component(selected_items[0].component,
                             selected_items[0].text)
            widget_component = WidgetItemComponent(comp.text, comp)
        else:
            return

        # then add the widget item to the selected inputs list
        self.selected_inp_list_view.addItem(widget_component)
        #TODO add these inputs to the currently selected move

    def remove_inputs(self):
        selected_index = self.selected_inp_list_view.currentRow()
        selected_input = self.selected_inp_list_view.takeItem(selected_index)
        #TODO remove this input from the currently selected move

    def add_move(self):
        move_name = self.move_name_field.text()
        entity = self.context['selected_entity']
        selected_animation = self.ani_list_view.currentItem().component
        # build a list of the chosen inputs
        inputs = list()
        for i in range(self.selected_inp_list_view.count()):
            item = self.selected_inp_list_view.item(i)
            inp_component = item.component
            inputs.append(inp_component)

        # construct the move component
        move = MoveComponent(entity_id=entity,
                             name=move_name,
                             animation=selected_animation,
                             inputs=inputs)
        move_component_wrapper = Component(move, move_name)
        widget_component = WidgetItemComponent(move_name, move_component_wrapper)
        self.move_list_view.addItem(widget_component)

        # add the move component to the application context
        self.context['entities'][entity]['components']['move'].append(move_component_wrapper)

        # fire event for adding new move
        new_event = Event('added_move',
                          move_component=move_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('added_component',
                          entity=entity,
                          component_type='move',
                          component=move_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_move(self):
        entity = self.context['selected_entity']
        selected_index = self.move_list_view.currentRow()
        selected_item = self.move_list_view.takeItem(selected_index)

        # remove the move component from the application context
        self.context['entities'][entity]['components']['move'].remove(selected_item.component)

        # fire event for removing move
        new_event = Event('removed_move',
                          move_component=selected_item.component)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='move',
                          component=selected_item.component)
        EVENT_MANAGER.fire_event(new_event)

    def new_input(self, event):
        widget_component = WidgetItemComponent(event.input_component.text, 
                                               event.input_component)
        self.inp_list_view.addItem(widget_component) 

    def set_animations(self, event):
        entity = event.entity
        available_animations = self.context['entities'][entity]['components']['animation']
        # do a "soft" clear of the list
        # if we actually call self.graphic_list_view.clear(),
        # the C++ Qt objects will be deleted
        for i in range(self.ani_list_view.count()-1,-1,-1):
            self.ani_list_view.takeItem(i)

        for animation in available_animations:
            widget_component = WidgetItemComponent(animation.text, animation)
            self.ani_list_view.addItem(widget_component)

    def add_animation(self, event):
        ani_component = event.animation_component
        widget_component = WidgetItemComponent(ani_component.text, ani_component)
        self.ani_list_view.addItem(widget_component)

    def remove_animation(self, event):
        for i in range(self.ani_list_view.count()-1,-1,-1):
            widget_component = self.ani_list_view.item(i)
            if widget_component.component == event.animation_component:
                self.ani_list_view.takeItem(i)

    def removed_input(self, event):
        for i in range(self.inp_list_view.count()-1,-1,-1):
            item = self.inp_list_view.item(i)
            inp = item.component
            if event.input_component == inp:
                self.inp_list_view.takeItem(i)

    def update(self):
        entity = self.context['selected_entity']
        self.move_list_view.clear()
        if entity and entity != '':
            for move in self.context[entity]['components']['move']:
                widget_component = WidgetItemComponent(move.text, move)
                self.move_list_view.addItem(widget_component)
