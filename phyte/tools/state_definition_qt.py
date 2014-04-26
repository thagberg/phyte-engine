from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from engine.state import StateComponent
from common import Component, WidgetItemComponent, TreeWidgetItemComponent, UNIVERSE_ENTITY
from engine import events
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class StateDefinitionEditor(Editor):
    def __init__(self, context):
        super(StateDefinitionEditor, self).__init__(context,
                                                    QtGui.QGroupBox('State'))
        # gui elements
        self.layout = QtGui.QGridLayout()
        self.state_name_label = QtGui.QLabel('State Name')
        self.state_name_field = QtGui.QLineEdit()
        self.activation_label = QtGui.QLabel('Activation Events')
        self.activation_list_view = QtGui.QListWidget()
        self.activation_layout = QtGui.QVBoxLayout()
        self.deactivation_label = QtGui.QLabel('Deactivation Events')
        self.deactivation_list_view = QtGui.QListWidget()
        self.deactivation_layout = QtGui.QVBoxLayout()
        self.activation_component_label = QtGui.QLabel('Activation Component')
        self.activation_component_tree_view = QtGui.QTreeWidget()
        self.activation_component_layout = QtGui.QVBoxLayout()
        self.rule_list_label = QtGui.QLabel('Rules')
        self.rule_list_view = QtGui.QListWidget()
        self.rule_list_layout = QtGui.QVBoxLayout()
        self.rule_value_label = QtGui.QLabel('Rule Value')
        self.rule_value_field = QtGui.QLineEdit()
        self.rule_value_component_label = QtGui.QLabel('Or Pick a Component Value')
        self.rule_value_component_tree_view = QtGui.QTreeWidget()
        self.rule_value_layout = QtGui.QVBoxLayout()
        self.selected_rule_list_view = QtGui.QListWidget()
        self.add_rule_button = QtGui.QPushButton('Add Rule and Value')
        self.remove_rule_button = QtGui.QPushButton('Remove Rule and Value')
        self.rule_button_layout = QtGui.QVBoxLayout()
        self.state_list_view = QtGui.QListWidget()
        self.add_state_button = QtGui.QPushButton('Add State')
        self.remove_state_button = QtGui.QPushButton('Remove State')
        self.state_button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.layout.addWidget(self.state_name_label,0,0)
        self.layout.addWidget(self.state_name_field,0,1)
        self.activation_layout.addWidget(self.activation_label)
        self.activation_layout.addWidget(self.activation_list_view)
        self.layout.addLayout(self.activation_layout,1,0)
        self.deactivation_layout.addWidget(self.deactivation_label)
        self.deactivation_layout.addWidget(self.deactivation_list_view)
        self.layout.addLayout(self.deactivation_layout,1,1)
        self.activation_component_layout.addWidget(self.activation_component_label)
        self.activation_component_layout.addWidget(self.activation_component_tree_view)
        self.layout.addLayout(self.activation_component_layout,1,2,1,2)
        self.rule_list_layout.addWidget(self.rule_list_label)
        self.rule_list_layout.addWidget(self.rule_list_view)
        self.layout.addLayout(self.rule_list_layout,2,0)
        self.rule_value_layout.addWidget(self.rule_value_label)
        self.rule_value_layout.addWidget(self.rule_value_field)
        self.rule_value_layout.addWidget(self.rule_value_component_label)
        self.rule_value_layout.addWidget(self.rule_value_component_tree_view)
        self.layout.addLayout(self.rule_value_layout,2,1)
        self.rule_button_layout.addWidget(self.add_rule_button)
        self.rule_button_layout.addWidget(self.remove_rule_button)
        self.layout.addLayout(self.rule_button_layout,2,2)
        self.layout.addWidget(self.selected_rule_list_view,2,3)
        self.layout.addWidget(self.state_list_view,3,0)
        self.state_button_layout.addWidget(self.add_state_button)
        self.state_button_layout.addWidget(self.remove_state_button)
        self.layout.addLayout(self.state_button_layout,3,1,1,1)

        self.group.setLayout(self.layout)

        # populate event lists
        for name in (x for x in dir(events) if not x.startswith('_')):
            value = events.__dict__[name]
            activation_component = Component(value, name)
            deactivation_component = Component(value, name)
            a_widget_component = WidgetItemComponent(name, activation_component)
            d_widget_component = WidgetItemComponent(name, deactivation_component)
            self.activation_list_view.addItem(a_widget_component)
            self.deactivation_list_view.addItem(d_widget_component)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_entity)
        EVENT_MAPPING.register_handler('added_component', self.add_component)
        EVENT_MAPPING.register_handler('removed_component', self.remove_component)
        EVENT_MAPPING.register_handler('added_rule', self.rule_added)
        EVENT_MAPPING.register_handler('removed_rule', self.rule_removed)

        # wire up events
        self.add_rule_button.clicked.connect(self.add_rule)
        self.remove_rule_button.clicked.connect(self.remove_rule)
        self.add_state_button.clicked.connect(self.add_state)
        self.remove_state_button.clicked.connect(self.remove_state)
        self.state_list_view.currentItemChanged.connect(self.select_state)

    def set_entity(self, event):
        entity = event.entity

        # first do a soft clear of the tree view
        for i in range(self.activation_component_tree_view.topLevelItemCount()-1,-1,-1):
            item = self.activation_component_tree_view.takeTopLevelItem(i)
            for j in range(item.childCount()-1,-1,-1):
                child_item = item.takeChild(j)

        # repopulate the tree with the current entity's components
        tl_items = self.context[entity]['components'].keys()
        # component types represent the top level tree items
        for item in tl_items:
            components = self.context[entity]['components'][item]
            tl_tree_item = TreeWidgetItemComponent(item, components)
            self.activation_component_tree_view.addTopLevelItem(tl_tree_item)
            # the components should all be listed under their respective 
            # component type
            for component in components:
                tree_item = TreeWidgetItemComponent(component.text, component)
                tl_tree_item.addChild(tree_item)

        # now do this same stuff for the rule value component tree
        rule_value_tree = self.rule_value_component_tree_view
        # clear it out first
        for i in range(rule_value_tree.topLevelItemCount()-1,-1,-1):
            item = rule_value_tree.takeTopLevelItem(i)
            for j in range(item.childCount()-1,-1,-1):
                child_item = item.takeChild(j)
                for k in range(child_item.childCount()-1,-1,-1):
                    grand_child_item = child_item.takeChild(k)

        # then repopulate the tree with components and component properties
        tl_items = self.context[entity]['components'].keys()
        for item in tl_items:
            components = self.context[entity]['components'][item]
            tl_tree_item = TreeWidgetItemComponent(item, components)
            rule_value_tree.addTopLevelItem(tl_tree_item)
            for component in components:
                component_item = TreeWidgetItemComponent(component.text, component)
                tl_tree_item.addChild(component_item)
                # then add a child item for each non-private attribute of 
                # this component
                for name in (x for x in dir(component.component) if not x.startswith('_')):
                    attr = component.component.__dict__[name]
                    component_attr_item = TreeWidgetItemComponent(name, attr)
                    component_item.addChild(component_attr_item)

    def add_component(self, event):
        # TODO: optimize this process.  To save time, right
        #       now I am just completely wiping out and rebuilding
        #       the tree every time a component is added
        self.set_entity(event)

    def remove_component(self, event):
        # TODO: optimize this process.  To save time, right
        #       now I am just completely wiping out and rebuilding
        #       the tree every time a component is removed
        self.set_entity(event)

    def add_rule(self):
        selected_item = self.rule_list_view.currentItem()
        selected_component = selected_item.component
        rule_name = selected_component.text

        # determine the rule value for this rule
        rule_value = self.rule_value_field.text()
        rule_text = '{name} - {value}'.format(name=rule_name, value=rule_value)
        # if no value is entered in the rule value field,
        # we then look for a chosen component property
        if rule_value is None or rule_value == '':
            component_item = self.rule_value_component_tree_view.currentItem()
            component_text = component_item.text()
            component = component_item.component
            rule_value = lambda: component
            if component_item.parentWidget() != 0:
                component_text = '{a}.{b}'.format(a=component_item.parentWidget().text(),
                                                  b=component_text)
            rule_text = '{name} - {value}'.format(name=rule_name,
                                                  value=component_text)

        widget_component = WidgetItemComponent(rule_text, rule_value)
        self.selected_rule_list_view.addItem(widget_component)

    def remove_rule(self):
        pass

    def add_state(self):
        pass

    def remove_state(self):
        pass

    def select_state(self):
        pass

    def rule_added(self, event):
        rule_component = event.rule_component
        widget_component = WidgetItemComponent(rule_component.text, rule_component)
        self.rule_list_view.addItem(widget_component)

    def rule_removed(self, event):
        rule_component = event.rule_component
        # search for the specified component and do a soft remove
        for i in range(self.rule_list_view.coun()-1,-1,-1):
            item = self.rule_list_view.item(i)
            component = item.component
            if component == rule_component:
                self.rule_list_view.takeItem(i)
                break
