from collections import defaultdict

import dill as pickle
import yaml

from tools.common import Component
from tools import *


def save_config(context, file_name):
    config_file = file(file_name, 'w')
    clean_context = defaultdict(dict)

    # entities
    clean_context['entities'] = dict()
    for name, entity in context['entities'].iteritems():
        clean_context['entities'][name] = dict() 
        clean_entity = clean_context['entities'][name]
        clean_entity['components'] = defaultdict(list)
        # loop over each component type for this entity
        for component_type, components in entity['components'].iteritems():
            clean_entity['components'][component_type] = list()
            clean_comps = clean_entity['components'][component_type]
            for component in components:
                #TODO detect if this component is an array and
                # iterate over it properly if it is
                clean_component = component
                clean_comps.append(clean_component)

    # assets
    clean_context['assets'] = list()
    if 'assets' in context:
        for asset in context['assets']:
            clean_context['assets'].append(asset)

    # rules
    clean_context['rules'] = list()
    if 'rules' in context:
        for rule in context['rules']:
            clean_context['rules'].append(rule)

    # inputs
    clean_context['inputs'] = list()
    if 'inputs' in context:
        for inp in context['inputs']:
            clean_context['inputs'].append(inp)

    # serialize to file
    yaml.dump(clean_context, config_file)
    config_file.close() 


def open_config(file_name):
    config_file = open(file_name, 'r')
    context = yaml.load(config_file)
    usable_context = dict() 

    # entities
    usable_context['entities'] = dict()
    usable_context['selected_entity'] = ''
    for name, entity in context['entities'].iteritems():
        usable_context['entities'][name] = dict()
        usable_context['entities'][name]['components'] = defaultdict(list)
        for comp_type in entity['components']:
            for component in entity['components'][comp_type]:
                #good_component = Component(component.component, component.text)
                good_component = component
                usable_context['entities'][name]['components'][comp_type].append(good_component)

    # assets
    usable_context['assets'] = list()
    if 'assets' in context:
        for asset in context['assets']:
            usable_context['assets'].append(asset)

    # rules
    usable_context['rules'] = list()
    if 'rules' in context:
        for rule in context['rules']:
            usable_context['rules'].append(rule)

    # inputs
    usable_context['inputs'] = list()
    if 'inputs' in context:
        for inp in context['inputs']:
            usable_context['inputs'].append(inp)

    config_file.close()
    return usable_context
