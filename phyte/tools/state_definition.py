import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from rule_definition import Rule
from input_definition import Input
from common import *
from engine import events


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


class Event(TextListItem):
    def __init__(self, name, value):
        super(Event, self).__init__()
        self.name = name
        self.value = value
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '{self.name}: {self.value}'
        self.text = t.format(self=self)


class StateDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(StateDefinitionFrame, self).__init__(renderer, draw_to, context,
                                                   offset, widgets)
        self.text = 'State Definition'
        self.activation_events = ListItemCollection()
        self.deactivation_events = ListItemCollection()
        self.available_rules = ListItemCollection()
        self.chosen_rules = ListItemCollection()
        self.available_components = ListItemCollection()
        self.component_properties = ListItemCollection()
        self.states = self.context['states']
        self.current_state = None
        self.current_rule = None

        # define widgets
        self.activation_events_list = ScrolledList(300, 300, 
                                                   self.activation_events)
        self.deactivation_events_list = ScrolledList(300, 300,
                                                     self.deactivation_events)
        self.available_rules_list = ScrolledList(175, 200, 
                                                 self.available_rules)
        self.chosen_rules_list = ScrolledList(175, 200,
                                              self.chosen_rules)
        self.available_components_list = ScrolledList(175, 200,
                                                      self.available_components)
        self.component_properties_list = ScrolledList(175, 200,
                                                      self.component_properties)
        self.states_list = ScrolledList(250, 300, self.states)
        self.add_button = Button('Add State')
        self.update_button = Button('Update State')
        self.remove_button = Button('Remove State')
        self.rule_value_entry = Entry()
        self.rule_value_label = Label('Rule Value')
        self.activation_events_label = Label('Choose Activation Event')
        self.deactivation_events_label = Label('Choose Deactivation Event')
        self.available_rules_label = Label('Choose Rule')
        self.add_rule_button = Button('Add')
        self.remove_rule_button = Button('Remove')
        self.available_components_label = Label('Choose Component')
        self.component_properties_label = Label('Choose Property')

        # build widget list
        append = self.widgets.append
        append(self.activation_events_list)
        append(self.deactivation_events_list)
        append(self.activation_events_label)
        append(self.deactivation_events_label)
        append(self.available_rules_list)
        append(self.chosen_rules_list)
        append(self.states_list)
        append(self.rule_value_entry)
        append(self.rule_value_label)
        append(self.available_rules_label)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)
        append(self.add_rule_button)
        append(self.remove_rule_button)
        append(self.available_components_list)
        append(self.component_properties_list)
        append(self.available_components_label)
        append(self.component_properties_label)

        # set properties
        self.set_pos(self.activation_events_label, (10, 0))
        self.set_pos(self.activation_events_list, (10, 30))
        self.set_pos(self.deactivation_events_label, (320, 0))
        self.set_pos(self.deactivation_events_list, (320, 30))
        self.set_pos(self.rule_value_label, (630, 0))
        self.set_pos(self.rule_value_entry, (690, 0))
        self.set_pos(self.available_rules_label, (630, 30))
        self.set_pos(self.available_rules_list, (630, 50))
        self.set_pos(self.add_rule_button, (815, 50))
        self.set_pos(self.remove_rule_button, (815, 80))
        self.set_pos(self.chosen_rules_list, (875, 50))
        self.set_pos(self.states_list, (10, 350))
        self.set_pos(self.add_button, (280, 350))
        self.set_pos(self.update_button, (280, 390))
        self.set_pos(self.remove_button, (280, 430))
        self.set_pos(self.available_components_label, (380, 350))
        self.set_pos(self.available_components_list, (380, 390))
        self.set_pos(self.component_properties_label, (580, 350))
        self.set_pos(self.component_properties_list, (580, 390))

        # miscellaneous
        self.activation_events_list.selectionmode = SELECTION_SINGLE
        self.deactivation_events_list.selectionmode = SELECTION_SINGLE
        self.available_rules_list.selectionmode = SELECTION_SINGLE
        self.chosen_rules_list.selectionmode = SELECTION_SINGLE
        self.available_components_list.selectionmode = SELECTION_SINGLE
        self.component_properties_list.selectionmode = SELECTION_SINGLE
        self.update_button.sensitive = False
        self.remove_button.sensitive = False
        self.add_rule_button.sensitive = False
        self.remove_rule_button.sensitive = False

        # wire up GUI
        self.available_rules_list.connect_signal(SIG_SELECTCHANGED,
                                                 self._activate_controls)
        self.chosen_rules_list.connect_signal(SIG_SELECTCHANGED,
                                              self._activate_controls)
        self.states_list.connect_signal(SIG_SELECTCHANGED, 
                                       self._activate_controls)
        self.states_list.connect_signal(SIG_SELECTCHANGED,
                                       self._select_current_state)
        self.available_components_list.connect_signal(SIG_SELECTCHANGED,
                                                      self._select_component)
        self.add_button.connect_signal(SIG_CLICKED, self._add_state)
        self.update_button.connect_signal(SIG_CLICKED, self._update_state)
        self.remove_button.connect_signal(SIG_CLICKED, self._remove_state)
        self.add_rule_button.connect_signal(SIG_CLICKED, self._add_rule)
        self.remove_rule_button.connect_signal(SIG_CLICKED, self._remove_rule)

    def _select_component(self):
        comp_selection = self.available_components_list.get_selected()[0]
        self.component_properties_list.items = ListItemCollection()
        items = self.component_properties_list.items
        for name in [x for x in dir(comp_selection) if not x.startswith('_')]:
            new_text = TextListItem()
            new_text.text = name
            items.append(new_text)
        self.component_properties_list.child.update_items()

    def _add_rule(self):
        rule_selection = self.available_rules_list.get_selected()[0]
        copy_rule = Rule(rule_selection.name, 
                         rule_selection.operator,
                         rule_selection.value)
        self.chosen_rules_list.items.append(copy_rule)
        self.chosen_rules_list.child.update_items()

    def _remove_rule(self):
        rule_selection = self.chosen_rules_list.get_selected()[0]
        self.chosen_rules_list.items.remove(rule_selection)
        self.chosen_rules_list.child.update_items()
        self._activate_controls()

    def _update_state(self):
        pass

    def _remove_state(self):
        state_selection = self.states_list.get_selected()[0]
        self.states.remove(state_selection)
        self.states_list.items.remove(state_selection)
        self.states_list.child.update_items()

    def _select_current_state(self):
        state_selection = self.states_list.get_selected()[0]
        self.current_state = state_selection

    def _add_state(self):
        pass

    def _activate_controls(self):
        state_selection = self.states_list.get_selected()
        avail_rule_selection = self.available_rules_list.get_selected()
        chosen_rule_selection = self.chosen_rules_list.get_selected()
        
        if len(state_selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False
        if len(avail_rule_selection) > 0:
            self.add_rule_button.sensitive = True
        else:
            self.add_rule_button.sensitive = False
        if len(chosen_rule_selection) > 0:
            self.remove_rule_button.sensitive = True
        else:
            self.remove_rule_button.sensitive = False

        self.states_list.child.update_items()
        self.available_rules_list.child.update_items()
        self.chosen_rules_list.child.update_items()

    def activate(self):
        super(StateDefinitionFrame, self).activate()
        if len(self.activation_events_list.items) == 0:
            # get all "public" properties of the events module
            for name in (x for x in dir(events) if not x.startswith('_')):
                value = events.__dict__[name]
                new_event = Event(name, value)
                # can't share ListItem's between ListItemCollections...
                new_deac_event = Event(name, value)
                self.activation_events_list.items.append(new_event)
                self.deactivation_events_list.items.append(new_deac_event)
            self.activation_events_list.child.update_items()
            self.deactivation_events_list.child.update_items()
        if len(self.available_rules_list.items) == 0:
            for rule in self.context['rules']:
                copy_rule = Rule(rule.name, rule.operator, rule.value)
                self.available_rules.append(copy_rule)
                self.available_rules_list.items.append(copy_rule)
            self.available_rules_list.child.update_items()
        if len(self.available_components_list.items) == 0:
            for comp in self.context['components']:
                copy_comp = Component(comp)
                self.available_components_list.items.append(copy_comp)
            self.available_components_list.child.update_items()
