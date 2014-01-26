import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from common import *


class Move(TextListItem):
    def __init__(self, inputs=None, animation=None):
        super(Move, self).__init__()
        self.inputs = list() if inputs is None else inputs
        self.animation = animation
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '{inputs} inputs - {frames} frames'
        return t.format(inputs=len(self.inputs), 
                        frames=len(self.animation.frames))


class MoveDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(MoveDefinitionFrame, self).__init__(renderer, draw_to,
                                                  context, offset, widgets)
        self.text = 'Move Definition'
        self.moves = self.context['moves']
        self.inputs = self.context['inputs']

        # define widgets
        self.move_list = ScrolledList(200, 200, self.moves)
        self.ani_label = Label('Animation')
        self.ani_list = ScrolledList(200, 100, self.moves)
        self.chosen_input_label = Label('Chosen Inputs')
        self.chosen_input_list = ScrolledList(100, 100, self.inputs)
        self.avail_input_label = Label('Available Inputs')
        self.avail_input_list = ScrolledList(100, 100)
        self.add_input_button = Button('Add Input')
        self.remove_input_button = Button('Remove Input')
        self.add_button = Button('Add Move')
        self.update_button = Button('Update Move')
        self.remove_button = Button('Remove Move')

        # build widget list
        append = self.widgets.append
        append(self.ani_label)
        append(self.ani_list)
        append(self.chosen_input_label)
        append(self.chosen_input_list)
        append(self.avail_input_label)
        append(self.avail_input_list)
        append(self.add_input_button)
        append(self.remove_input_button)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)

        # set properties
        self.set_pos(self.ani_label, (10, 0))
        self.set_pos(self.ani_list, (10, 30))
        self.set_pos(self.avail_input_label, (230, 0))
        self.set_pos(self.avail_input_list, (230, 30))
        self.set_pos(self.add_input_button, (340, 30))
        self.set_pos(self.remove_input_button, (340, 60))
        self.set_pos(self.chosen_input_label, (440, 0))
        self.set_pos(self.chosen_input_list, (440, 30))
        self.set_pos(self.move_list, (10, 400))
        self.set_pos(self.add_button, (230, 400))
        self.set_pos(self.update_button, (230, 440))
        self.set_pos(self.remove_button, (230, 480))

        # miscenalenous
        self.ani_list.selectionmode = SELECTION_SINGLE
