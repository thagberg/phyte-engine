import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from input_definition import Input
from common import *
from ..engine import events


class Rule(TextListItem):
    def __init__(self, name, operator, value):
        super(Rule, self).__init__()
        self.name = name
        self.operator = operator
        self.value = value
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '{self.name} / {self.operator.text} / {self.value}'
        self.text = t.format(self=self)


class Operator(TextListItem):
    def __init__(self, name):
        super(Operator, self).__init__()
        self.name = name
        self.text = self.name


class RuleDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(RuleDefinitionFrame, self).__init__(renderer, draw_to,
                                                  context, offset, widgets)
        self.text = 'Rule Definition'
        self.rules = self.context['rules']
        self.operators = ListItemCollection()

        # define widgets
        self.rule_list = ScrolledList(200, 300, self.rules)
        self.add_button = Button('Add Rule')
        self.update_button = Button('Update Rule')
        self.remove_button = Button('Remove Rule')
        self.name_label = Label('Rule Name')
        self.name_entry = Entry()
        self.operator_label = Label('Operators')
        self.operator_list = ScrolledList(50, 100, self.operators)
        self.value_label = Label('Rule Value')
        self.value_entry = Entry()
        self.operator_list.child.update_items()

        # build widget list
        append = self.widgets.append
        append(self.rule_list)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)
        append(self.name_label)
        append(self.name_entry)
        append(self.operator_label)
        append(self.operator_list)
        append(self.value_label)
        append(self.value_entry)

        # set properties
        self.set_pos(self.name_label, (10, 0))
        self.set_pos(self.name_entry, (70, 0))
        self.set_pos(self.operator_label, (180, 0))
        self.set_pos(self.operator_list, (180, 30))
        self.set_pos(self.value_label, (260, 0))
        self.set_pos(self.value_entry, (330, 0))
        self.set_pos(self.rule_list, (10, 175))
        self.set_pos(self.add_button, (230, 175))
        self.set_pos(self.update_button, (230, 215))
        self.set_pos(self.remove_button, (230, 255))

        # miscelaneous
        self.add_button.sensitive = False
        self.update_button.sensitive = False
        self.remove_button.sensitive = False
        self.rule_list.selectionmode = SELECTION_SINGLE
        self.operator_list.selectionmode = SELECTION_SINGLE

        # wire up GUI
        self.add_button.connect_signal(SIG_CLICKED, self._add_rule)
        self.update_button.connect_signal(SIG_CLICKED, self._update_rule)
        self.remove_button.connect_signal(SIG_CLICKED, self._remove_rule)
        self.rule_list.connect_signal(SIG_SELECTCHANGED, self._set_current_rule)
        self.rule_list.connect_signal(SIG_SELECTCHANGED, self._activate_controls)
        self.operator_list.connect_signal(SIG_SELECTCHANGED, self._activate_controls)

    def _add_rule(self):
        selected_op = self.operator_list.get_selected()[0]
        rule_name = self.name_entry.text
        rule_value = self.value_entry.text
        new_rule = Rule(rule_name, selected_op, rule_value)
        self.rule_list.items.append(new_rule)
        self.context['rules'].append(new_rule)
        self.context['components'].append(new_rule)
        self.rule_list.child.update_items()

    def _update_rule(self):
        selected_rule = self.rule_list.get_selected()[0]
        selected_rule.name = self.name_entry.text
        selected_rule.operator = self.operator_list.get_selected()[0]
        selected_rule.value = self.operator_entry.text
        selected_rule.refresh_text()
        self.rule_list.update_items()
        self._activate_controls()

    def _remove_rule(self):
        selected_rule = self.rule_list.get_selected()[0]
        self.rule_list.items.remove(selected_rule)
        self.context['rules'].remove(selected_rule)
        self.context['components'].remove(selected_rule)
        self.rule_list.child.update_items()
        self._activate_controls()

    def _set_current_rule(self):
        selected_rule = self.rule_list.get_selected()[0]
        self.name_entry.text = selected_rule.name
        self.value_entry.text = selected_rule.value

    def _activate_controls(self):
        selected_rule = self.rule_list.get_selected()
        selected_operator = self.operator_list.get_selected()
        if len(selected_rule) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
        if len(selected_operator) > 0:
            self.add_button.sensitive = True
        else:
            self.add_button.sensitive = False
            self.remove_button.sensitive = False

    def activate(self):
        super(RuleDefinitionFrame, self).activate()
        append = self.operator_list.items.append
        append(Operator('lt'))
        append(Operator('le'))
        append(Operator('eq'))
        append(Operator('ne'))
        append(Operator('ge'))
        append(Operator('gt'))
        append(Operator('in'))
        self.operator_list.child.update_items()
