from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, UNIVERSE_ENTITY
from engine.state import RuleComponent, OP_MAP
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class RuleDefinitionEditor(Editor):
    def __init__(self, context):
        super(RuleDefinitionEditor, self).__init__(context,
                                                   QtGui.QGroupBox('Rule'))
        if 'rules' not in self.context:
            self.context['rules'] = list()
        # gui elements
        self.layout = QtGui.QGridLayout()
        self.rule_name_label = QtGui.QLabel('Rule Name')
        self.rule_name_field = QtGui.QLineEdit()
        self.operator_label = QtGui.QLabel('Choose Operator')
        self.operator_list_view = QtGui.QComboBox()
        self.operator_layout = QtGui.QVBoxLayout()
        self.value_label = QtGui.QLabel('Rule Value')
        self.value_field = QtGui.QLineEdit()
        self.rule_list_view = QtGui.QListWidget()
        self.add_rule_button = QtGui.QPushButton('Add Rule')
        self.remove_rule_button = QtGui.QPushButton('Remove Rule')
        self.rule_button_layout = QtGui.QVBoxLayout()

        # set up layout
        self.layout.addWidget(self.rule_name_label,0,0)
        self.layout.addWidget(self.rule_name_field,0,1)
        self.operator_layout.addWidget(self.operator_label)
        self.operator_layout.addWidget(self.operator_list_view)
        self.layout.addLayout(self.operator_layout,1,0)
        self.layout.addWidget(self.value_label,1,1)
        self.layout.addWidget(self.value_field,1,2)
        self.layout.addWidget(self.rule_list_view,2,0)
        self.rule_button_layout.addWidget(self.add_rule_button)
        self.rule_button_layout.addWidget(self.remove_rule_button)
        self.layout.addLayout(self.rule_button_layout,2,1)

        self.group.setLayout(self.layout)
            
        # add operators
        self.operator_list_view.addItems(OP_MAP.keys())

        # wire up events
        self.add_rule_button.clicked.connect(self.add_rule)
        self.remove_rule_button.clicked.connect(self.remove_rule)
        self.rule_list_view.currentItemChanged.connect(self.select_rule)

    def add_rule(self):
        rule_name = self.rule_name_field.text()
        operator = str(self.operator_list_view.itemText(self.operator_list_view.currentIndex()))
        value = self.value_field.text()
        try:
            value = float(value)
        except ValueError:
            pass
        # create rule component
        rule_component = RuleComponent(rule_name, operator, value)
        rule_component_wrapper = Component(rule_component, rule_name)
        widget_component = WidgetItemComponent(rule_name,
                                               rule_component_wrapper)
        self.rule_list_view.addItem(widget_component)

        # add the rule component to the application context
        self.context['rules'].append(rule_component_wrapper)

        # fire event for adding rule
        new_event = Event('added_rule',
                          rule_component=rule_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_rule(self):
        selected_index = self.rule_list_view.currentRow()
        selected_item = self.rule_list_view.takeItem(selected_index)
        selected_component = selected_item.component

        # remove rule from application context
        for comp in self.context['rules']:
            if comp == selected_component:
                self.context['rules'].remove(comp)
                break

        # fire event for removing rule
        new_event = Event('removed_rule',
                          rule_component=selected_component)
        EVENT_MANAGER.fire_event(new_event)

    def select_rule(self):
        selected_item = self.rule_list_view.currentItem()
        if selected_item is not None:
            selected_component = selected_item.component

            # set field values
            self.rule_name_field.setText(selected_component.text)
            self.value_field.setText(str(selected_component.component.value))
            index = self.operator_list_view.findText(selected_component.component.operator)
            self.operator_list_view.setCurrentIndex(index)
