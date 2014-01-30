import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from input_definition import Input
from common import *
from ..engine import events


class State(TextListItem):
    def __init__(self, rules, activation_name, activation_value,
                 deactivation_name, deactivation_value, rule_values):
        super(State, self).__init__()
        self.rules = rules
        self.activation_name = activation_name
        self.activation_value = activation_value
        self.deactivation_name = deactivation_name
        self.deactivation_value = deactivation_value
        self.rule_values = rule_values
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '{self.activation_name}: {self.activation_value} / {len(self.rules)}'
        self.text = t.format(self=self)


class StateDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(StateDefinitionFrame, self).__init__(renderer, draw_to, context,
                                                   offset, widgets)
        self.text = 'State Definition'
