import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from common import *


class Entity(object):
    def __init__(self, name):
        self.name = name


class EntityDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(EntityDefinitionFrame, self).__init__(renderer, draw_to,
                                                    context, offset, widgets)
        self.text = 'Entity Definition'
        self.entities = self.context['entities']

        # define widgets
        self.entity_name_entry = Entry()
        self.entity_name_label = Label('Entity Name')
        self.entity_list = ScrolledList(300, 300, self.entities)
        self.add_button = Button('Add Entity')
        self.update_button = Button('Update Entity')
        self.remove_button = Button('Remove Entity')

        # build widget list
        append = self.widgets.append
        append(self.entity_name_entry)
        append(self.entity_name_label)
        append(self.entity_list)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)

        # set widget properties
        self.set_pos(self.entity_name_label, (10, 0))
        self.set_pos(self.entity_name_entry, (90, 0))
        self.set_pos(self.entity_list, (10, 60))
        self.set_pos(self.add_button, (320, 60))
        self.set_pos(self.update_button, (320, 95))
        self.set_pos(self.remove_button, (320, 130))
        
        # miscelaneous
        self.entity_list.selectionmode = SELECTION_SINGLE
        self.update_button.sensitive = False
        self.remove_button.sensitive = False

        # wire up GUI
        self.add_button.connect_signal(SIG_CLICKED, self._add_entity)
        self.update_button.connect_signal(SIG_CLICKED, self._update_entity)
        self.remove_button.connect_signal(SIG_CLICKED, self._remove_entity)
        self.entity_list.connect_signal(SIG_SELECTCHANGED, self._activate_controls)

    def _add_entity(self):
        name = self.entity_name_entry.text
        new_entity = Entity(name)
        entity_wrapper = Component(new_entity, lambda:new_entity.name)
        self.entities.append(new_entity)
        self.entity_list.items.append(entity_wrapper)
        self.entity_list.child.update_items()

    def _update_entity(self):
        selected_entity = self.entity_list.get_selected()[0]
        new_name = self.entity_name_entry.text
        selected_entity.component.name = new_name
        selected_entity.refresh_text()
        self.entity_list.child.update_items()

    def _remove_entity(self):
        selected_entity = self.entity_list.get_selected()[0]
        self.entities.remove(selected_entity.component)
        self.entity_list.items.remove(selected_entity)
        self.entity_list.child.update_items()

    def _activate_controls(self):
        entity_selection = self.entity_list.get_selected()
        if len(entity_selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
            self.context['chosen_entity'] = entity_selection[0].component
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False

    def activate(self):
        super(EntityDefinitionFrame, self).activate()
