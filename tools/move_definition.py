import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from animation_definition import Animation
from input_definition import Input
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
        self.text = t.format(inputs=len(self.inputs), 
                        frames=len(self.animation.frames))


class MoveDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(MoveDefinitionFrame, self).__init__(renderer, draw_to,
                                                  context, offset, widgets)
        self.text = 'Move Definition'
        self.moves = self.context['moves']
        self.inputs = self.context['inputs']
        self.current_ani = None

        # define widgets
        self.move_list = ScrolledList(200, 200, self.moves)
        self.ani_label = Label('Animation')
        self.ani_list = ScrolledList(200, 250, self.moves)
        self.chosen_input_label = Label('Chosen Inputs')
        self.chosen_input_list = ScrolledList(100, 250, self.inputs)
        self.avail_input_label = Label('Available Inputs')
        self.avail_input_list = ScrolledList(100, 250)
        self.add_input_button = Button('Add Input')
        self.remove_input_button = Button('Remove Input')
        self.add_button = Button('Add Move')
        self.update_button = Button('Update Move')
        self.remove_button = Button('Remove Move')

        # build widget list
        append = self.widgets.append
        append(self.move_list)
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
        self.avail_input_list.selectionmode = SELECTION_SINGLE
        self.chosen_input_list.selectionmode = SELECTION_SINGLE
        self.add_button.sensitive = False
        self.update_button.sensitive = False
        self.remove_button.sensitive = False
        self.add_input_button.sensitive = False
        self.remove_input_button.sensitive = False

        # wire up GUI
        self.add_input_button.connect_signal(SIG_CLICKED, self._select_input)
        self.remove_input_button.connect_signal(SIG_CLICKED, self._remove_input)
        self.avail_input_list.connect_signal(SIG_SELECTCHANGED,
                                             self._activate_input_controls)
        self.chosen_input_list.connect_signal(SIG_SELECTCHANGED,
                                              self._activate_input_controls)
        self.ani_list.connect_signal(SIG_SELECTCHANGED, self._select_animation)
        self.move_list.connect_signal(SIG_SELECTCHANGED, self._activate_controls)
        self.add_button.connect_signal(SIG_CLICKED, self._add_move)
        self.remove_button.connect_signal(SIG_CLICKED, self._remove_move)

    def _add_move(self):
        selected_ani = self.ani_list.get_selected()[0]
        selected_inputs = self.chosen_input_list.items
        inputs = list()
        for item in selected_inputs:
            copy_item = Input(item.name)
            inputs.append(copy_item)
        new_move = Move(inputs, selected_ani)
        self.move_list.items.append(new_move)
        self.context['moves'].append(new_move)
        self.context['components'].append(new_move)
        self.move_list.child.update_items()

    def _remove_move(self):
        selected_move = self.move_list.get_selected()[0]
        self.move_list.items.remove(selected_move)
        self.context['moves'].remove(selected_move)
        self.context['components'].remove(selected_move)
        self.move_list.child.update_items()

    def _activate_input_controls(self):
        selected_avail = self.avail_input_list.get_selected()
        selected_chosen = self.chosen_input_list.get_selected()
        if len(selected_avail) > 0:
            self.add_input_button.sensitive = True
        else:
            self.add_input_button.sensitive = False
        if len(selected_chosen) > 0:
            self.remove_input_button.sensitive = True
        else:
            self.remove_input_button.sensitive = False
        self.avail_input_list.child.update_items()
        self.chosen_input_list.child.update_items()

    def _select_animation(self):
        selected_ani = self.ani_list.get_selected()[0]
        self.current_ani = selected_ani
        self._activate_controls()

    def _activate_controls(self):
        selected_ani = self.ani_list.get_selected()
        selected_move = self.move_list.get_selected()
        if len(selected_ani) > 0:
            self.add_button.sensitive = True
        else:
            self.add_button.sensitive = False
        if len(selected_move) > 0:
            self.remove_button.sensitive = True
        else:
            self.remove_button.sensitive = False
        self.move_list.child.update_items()

    def _select_input(self):
        selected_input = self.avail_input_list.get_selected()[0]
        copy_input = Input(selected_input.name)
        self.chosen_input_list.items.append(copy_input)
        self.chosen_input_list.child.update_items()

    def _remove_input(self):
        selected_input = self.chosen_input_list.get_selected()[0]
        self.chosen_input_list.items.remove(selected_input)
        self.chosen_input_list.child.update_items()

    def activate(self):
        super(MoveDefinitionFrame, self).activate()
        # populate animation list
        items = ListItemCollection()
        # can't directly copy items over from one ScrolledLIst's
        # ListItemCollection to another, because of some hacky stuff
        # in the ocempgui library.  Can't properly mark each item as
        # dirty, so when the new ScrolledList's ListPortView tries to
        # update itself, it tries to redraw the ListItem's image, which
        # hasn't been defined for that ListPortView yet
        # Creating copies of each Frame is not the cleanest solution,
        # but it works
        for item in self.context['animations']:
            copy_ani = Animation(item.image_file, item.frames)
            items.append(copy_ani)
        self.ani_list.items = items
        self.ani_list.child.update_items()
        # populate available input list
        items = ListItemCollection()
        for item in self.context['inputs']:
            copy_input = Input(item.name)
            items.append(copy_input)
        self.avail_input_list.items = items
        self.avail_input_list.child.update_items()
