from system import System
from events import *
from collections import defaultdict
import operator

def __reverse_contains(a, b):
    '''operator.contains function uses opposite parameter ordering,
    so we wrap the call up to maintain consistency in rule checking syntax'''
    return operator.contains(b, a)
    
OP_MAP = {
    'lt': operator.lt,
    'le': operator.le,
    'eq': operator.eq,
    'ne': operator.ne,
    'ge': operator.ge,
    'gt': operator.gt,
    'in': __reverse_contains
}


class RuleComponent(object):
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value


class StateComponent(object):
    def __init__(self, entity_id, rules, activation_event_type, 
                 deactivation_event_type, activation_component, 
                 rule_values):
        self.entity_id = entity_id
        self.rules = rules
        self.activation_event_type = activation_event_type
        self.deactivation_event_type = deactivation_event_type
        self.activation_component = activation_component
        self.rule_values = rule_values


class StateValueComponent(object):
    def __init__(self, entity_id, active=False):
        self.entity_id = entity_id
        self.active = active


class StateSystem(System):
    def __init__(self, factory, components=None): 
        super(StateSystem, self).__init__()
        self.factory = factory
        self.components = list() if components is None else components
        self.entity_mapping = defaultdict(list)

    def _add(self, component):
        self.components.append(component)
        self.entity_mapping[component.entity_id].append(component)

    def _remove(self, component):
        try:
            self.components.remove(component)
            self.entity_mapping[component.entity_id].remove(component)
        except ValueError as e:
            print "Not able to remove component from StateSystem: %s" % e.strerror

    def handle_event(self, event):
        if event.type == ADDSTATECOMPONENT:
            self._add(event.component)
            print "Added new StateComponent: %s" % event.component
        elif event.type == REMOVESTATECOMPONENT:
            self._remove(event.component)
            print "Removed StateComponent: %s" % event.component

    def _check_rule(self, rule, rule_values):
        retval = OP_MAP[rule.operator](rule_values, rule.value)
        return retval

    def update(self, time):
        self.delta = time
        for comp in self.components:
            pass_rule = True
            for rule in comp.rules:
                # check if rule_values satisfy rule
                if rule.name in comp.rule_values:
                    check_values = comp.rule_values[rule.name]
                    # rule value might actually be a function call that
                    # returns the value we want to check
                    if callable(check_values):
                        check_values = check_values()
                    pass_rule = self._check_rule(rule, check_values)
                # early-out if a rule was not met
                if not pass_rule:
                    break
            if pass_rule:
                event_type = comp.activation_event_type
            else:
                event_type = comp.deactivation_event_type
            # if rules are met, this state component will be active for
            # the next cycle.  Otherwise, it will be inactive
            sa_event = GameEvent(event_type,
                                 component=comp.activation_component)
            self.delegate(sa_event)
