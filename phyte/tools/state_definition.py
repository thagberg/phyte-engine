import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from input_definition import Input
from common import *
from engine import events


class State(TextListItem):
    def __init__(self, rules, activation_event, deactivation_event, values):
        super(State, self).__init__()
        self.rules = rules
        self.activation_event = activation_event
        self.deactivation_event = deactivation_event
        self.values = values
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        pass
