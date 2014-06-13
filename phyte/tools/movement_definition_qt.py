from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, TreeWidgetItemComponent
from engine.movement import MovementComponent, VaryingMovementComponent
from engine.common import Vector2
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class Body(object):
    def __init__(self, parent, component):
        self.parent = parent
        self.component = component


class MovementDefinitionEditor(Editor):
    def __init__(self, context):
        super(MovementDefinitionEditor, self).__init__(context,
                                                       QtGui.QGroupBox('Movement'))
        # gui elements
        self.layout = QtGui.QGridLayout()
        self.move_name_label = QtGui.QLabel('Movement Name')
        self.move_name_field = QtGui.QLineEdit()
        self.velocity_type_group = QtGui.QButtonGroup()
        self.velocity_standard_type = QtGui.QRadioButton('Standard')
        self.velocity_pulse_type = QtGui.QRadioButton('Pulse')
        self.velocity_group = QtGui.QGroupBox('Velocity')
        self.velocity_x_label = QtGui.QLabel('X')
        self.velocity_x_field = QtGui.QLineEdit()
        self.velocity_y_label = QtGui.QLabel('Y')
        self.velocity_y_field = QtGui.QLineEdit()
        self.velocity_layout = QtGui.QGridLayout()
        self.body_label = QtGui.QLabel('Choose Body')
        self.body_tree_view = QtGui.QTreeWidget()
        self.body_layout = QtGui.QVBoxLayout()
        self.parent_label = QtGui.QLabel('Choose Parent')
        self.parent_list_view = QtGui.QListWidget()
        self.parent_layout = QtGui.QVBoxLayout()
        self.movement_list_view = QtGui.QListWidget()
        self.add_movement_button = QtGui.QPushButton('Add Movement')
        self.remove_movement_button = QtGui.QPushButton('Remove Movement')
        self.movement_button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.velocity_type_group.addButton(self.velocity_standard_type)
        self.velocity_type_group.addButton(self.velocity_pulse_type)
        self.layout.addWidget(self.move_name_label,0,0)
        self.layout.addWidget(self.move_name_field,0,1)
        self.velocity_layout.addWidget(self.velocity_standard_type,0,0)
        self.velocity_layout.addWidget(self.velocity_pulse_type,0,1)
        self.velocity_layout.addWidget(self.velocity_x_label,1,0)
        self.velocity_layout.addWidget(self.velocity_x_field,1,1)
        self.velocity_layout.addWidget(self.velocity_y_label,2,0)
        self.velocity_layout.addWidget(self.velocity_y_field,2,1)
        self.layout.addWidget(self.velocity_group,1,0)
        self.body_layout.addWidget(self.body_label)
        self.body_layout.addWidget(self.body_tree_view)
        self.layout.addLayout(self.body_layout,1,1)
        self.parent_layout.addWidget(self.parent_label)
        self.parent_layout.addWidget(self.parent_list_view)
        self.layout.addLayout(self.parent_layout,1,2)
        self.layout.addWidget(self.movement_list_view,2,0)
        self.movement_button_layout.addWidget(self.add_movement_button)
        self.movement_button_layout.addWidget(self.remove_movement_button)
        self.layout.addLayout(self.movement_button_layout,2,1)

        self.velocity_group.setLayout(self.velocity_layout)
        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_entity)
        EVENT_MAPPING.register_handler('added_component', self.add_component)
        EVENT_MAPPING.register_handler('removed_component', self.remove_component)

        # wire up events
        self.add_movement_button.clicked.connect(self.add_movement)
        self.remove_movement_button.clicked.connect(self.remove_movement)
        self.movement_list_view.currentItemChanged.connect(self.select_movement)

    def select_movement(self):
        '''
            update the visual state of the widget, which includes
            field values, radio buttons, selected list view items
            and selected tree view items
        '''
        selected_item = self.movement_list_view.currentItem()
        parent = selected_item.component.component.parent
        body = selected_item.component.component.body

        # set radio button states and x and y values based on
        # whether this movement component has a pulse velocity or 
        # standard velocity set
        if selected_item.component.component.pulse_velocity is not None:
            self.velocity_pulse_type.setChecked(True)
            x = selected_item.component.component.pulse_velocity.x
            y = selected_item.component.component.pulse_velocity.y
        else:
            self.velocity_standard_type.setChecked(True) 
            x = selected_item.component.component.velocity.x
            y = selected_item.component.component.velocity.y

        # update fields
        self.velocity_x_field.setText(str(x))
        self.velocity_y_field.setText(str(y))

        # find and select parent in parent list view
        for i in range(self.parent_list_view.count()):
            if self.parent_list_view.item(i).component.component == parent:
                # select this item
                self.parent_list_view.setCurrentRow(i)
                break

        # find and select the body in the body tree view
        for i in range(self.body_tree_view.topLevelItemCount()):
            tl_item = self.body_tree_view.topLevelItem(i)
            for j in range(tl_item.childCount()):
                child_item = tl_item.child(j)
                if child_item.component.component == body:
                    # expand parent and select this child item
                    tl_item.setExpanded(True)
                    child_item.setSelected(True)
                    break

    def add_movement(self):
        entity = self.context['selected_entity']
        name = str(self.move_name_field.text())
        standard = self.velocity_standard_type.isChecked()
        pulse = self.velocity_pulse_type.isChecked()
        parent = self.parent_list_view.currentItem()
        body= self.body_tree_view.currentItem().component
        x = float(self.velocity_x_field.text())
        y = float(self.velocity_y_field.text())
        velocity = Vector2(entity, [x, y])
        velocity_wrapper = Component(velocity, "{x}, {y}".format(x=x,y=y))
        # add this velocity vector component to context to make sure
        # its existence is known where it needs to be
        self.context['entities'][entity]['components']['vector'].append(velocity_wrapper)
        # fire event
        new_event = Event('added_component',
                          entity=entity,
                          component_type='vector',
                          component=velocity_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        if parent != None:
            parent = parent.component

        # create movement component object
        movement_component = MovementComponent(entity_id=entity,
                                               body=body,
                                               parent=parent,
                                               velocity=velocity_wrapper)
        movement_component_wrapper = Component(movement_component, name)
        widget_component = WidgetItemComponent(name, movement_component_wrapper)

        self.movement_list_view.addItem(widget_component)
        self.context['entities'][entity]['components']['movement'].append(movement_component_wrapper)

        # fire event
        new_event = Event('added_component',
                          entity=entity,
                          component_type='movement',
                          component=movement_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_movement(self):
        entity = self.context['selected_entity']
        selected_index = self.movement_list_view.currentRow()
        selected_item = self.movement_list_view.takeItem(selected_index)
        selected_component = selected_item.component

        # remove from context
        self.context['entities'][entity]['components']['movement'].remove(selected_component)

        # fire event
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='movement',
                          component=selected_component)
        EVENT_MANAGER.fire_event(new_event)

        # also clean up velocity vector
        velocity = selected_component.velocity
        self.context['entities'][entity]['components']['vector'].remove(velocity)
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='vector',
                          component=velocity)
        EVENT_MANAGER.fire_event(new_event)

    def update(self):
        entity = self.context['selected_entity']
        # first update movement list
        self.movement_list_view.clear()
        if entity and entity != '':
            for movement in self.context['entities'][entity]['components']['movement']:
                widget_component = WidgetItemComponent(movement.text, movement)
                self.movement_list_view.addItem(widget_component)

    def _find_bodies(self):
        entity = self.context['selected_entity']

        # first do a soft clear of the parent list view
        for i in range(self.parent_list_view.count()-1,-1,-1):
            item = self.parent_list_view.takeItem(i)

        # clear the body tree
        for i in range(self.body_tree_view.topLevelItemCount()-1,-1,-1):
            item = self.body_tree_view.takeTopLevelItem(i)
            # I think this is unnecessary since taking the top level item should clear its children
            #for j in range(item.childCount()-1,-1,-1):
            #    child_item = item.takeChild(j)

        # populate parent tree with existing movement components
        for component in self.context['entities'][entity]['components']['movement']:
            widget_item = WidgetItemComponent(component.text, component)
            self.parent_list_view.addItem(widget_item)

        # populate body tree with Vector2 components
        for comp_type, components in self.context['entities'][entity]['components'].iteritems():
            if comp_type == 'vector':
                for component in components:
                    tl_tree_item = TreeWidgetItemComponent(component.text, component)
                    self.body_tree_view.addTopLevelItem(tl_tree_item)
            for component in components:
                inner_comp = component.component
                for name in [x for x in dir(inner_comp) if not x.startswith('_')]:
                    QtCore.pyqtRemoveInputHook()
                    attr = inner_comp.__dict__[name]
                    if type(attr).__name__ == 'Component':
                        if attr.type_name == 'Vector2':
                            tl_tree_item = TreeWidgetItemComponent(component.text, inner_comp)
                            self.body_tree_view.addTopLevelItem(tl_tree_item)
                            tree_item = TreeWidgetItemComponent(name, attr)
                            tl_tree_item.addChild(tree_item)
                    if type(attr).__name__ == 'Vector2':
                        tl_tree_item = TreeWidgetItemComponent(component.text, inner_comp)
                        self.body_tree_view.addTopLevelItem(tl_tree_item)
                        tree_item = TreeWidgetItemComponent(name, attr)
                        tl_tree_item.addChild(tree_item)


    def set_entity(self, event):
        self._find_bodies()

    def add_component(self, event):
        self._find_bodies()

    def remove_component(self, event):
        self._find_bodies()
