import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from common import *
from ..engine import inputs


class Input(TextListItem):
    def __init__(self, name):
        super(Input, self).__init__()
        self.name = name
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = 'Input {name}'
        self.text = t.format(name=self.name)


class InputDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(InputDefinitionFrame, self).__init__(renderer, draw_to,
                                                   context, offset, widgets)
        self.text = 'Input Definition'
        self.inputs = self.context['inputs']

        # define widgets
        self.name_label = Label('Input Name')
        self.name_entry = Entry()
        self.input_list = ScrolledList(100, 200, self.inputs)
        self.add_button = Button('Add Input')
        self.update_button = Button('Update Input')
        self.remove_button = Button('Remove Input')

        # build widget list
        append = self.widgets.append
        append(self.name_label)
        append(self.name_entry)
        append(self.input_list)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)

        # set widget properties
        self.set_pos(self.name_label, (10, 0))
        self.set_pos(self.name_entry, (80, 0))
        self.set_pos(self.input_list, (10, 40))
        self.set_pos(self.add_button, (120, 40))
        self.set_pos(self.update_button, (120, 75))
        self.set_pos(self.remove_button, (120, 110))

        # miscelaneous
        self.update_button.sensitive = False
        self.remove_button.sensitive = False

        # wire up GUI
        self.add_button.connect_signal(SIG_CLICKED, self._add_input)
        self.update_button.connect_signal(SIG_CLICKED, self._update_input)
        self.remove_button.connect_signal(SIG_CLICKED, self._remove_input)
        self.input_list.connect_signal(SIG_SELECTCHANGED, self._set_current_input)
        self.input_list.connect_signal(SIG_SELECTCHANGED, self._activate_controls)

    def _add_input(self):
        new_input = Input(self.name_entry.text)
        self.input_list.items.append(new_input)
        self.context['inputs'].append(new_input)
        self.context['components'].append(new_input)

    def _remove_input(self):
        selected = self.input_list.get_selected()[0]
        self.input_list.items.remove(selected)
        self.context['inputs'].remove(selected)

    def _update_input(self):
        selected = self.input_list.get_selected()[0]
        selected.name = self.name_entry.text
        selected.refresh_text()
        self.input_list.child.update_items()

    def _set_current_input(self):
        selected = self.input_list.get_selected()[0]
        self.name_entry.text = selected.name

    def _activate_controls(self):
        selected = self.input_list.get_selected()

        if len(selected) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False

    def activate(self):
        super(InputDefinitionFrame, self).activate()
        items = ListItemCollection()
        # can't directly copy items over from one ScrolledLIst's
        # ListItemCollection to another, because of some hacky stuff
        # in the ocempgui library.  Can't properly mark each item as
        # dirty, so when the new ScrolledList's ListPortView tries to
        # update itself, it tries to redraw the ListItem's image, which
        # hasn't been defined for that ListPortView yet
        # Creating copies of each Frame is not the cleanest solution,
        # but it works
        for item in self.context['inputs']:
            copy_input = Input(item.name)
            items.append(copy_input)
        self.input_list.items = items
        self.input_list.child.update_items()

    def update(self, events):
        pass
