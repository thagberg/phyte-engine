import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from input_definition import Input
from common import *


class Rule(TextListItem):
    def __init__(self, name, operator, value):
        super(Rule, self).__init__()
        self.name = name
        self.operator = operator
        self.value = value
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '{self.name} / {self.operator} / {self.value}'
        self.text = t.format(self)


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
        self.operators.append(Operator('lt'))
        '''self.operators = ListItemCollection([Operator('lt'),
                                             Operator('le'),
                                             Operator('eq'),
                                             Operator('ne'),
                                             Operator('ge'),
                                             Operator('gt'),
                                             Operator('in')])'''
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
        self.value_label = Label('Rule Label')
        self.value_entry = Entry()

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
