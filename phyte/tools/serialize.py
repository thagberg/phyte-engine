import dill as pickle
from collections import defaultdict


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
                clean_component = component.component
                clean_comps.append(clean_component)

    # assets
    clean_context['assets'] = list()
    for asset in context['assets']:
        clean_context['assets'].append(asset.component)

    # rules
    clean_context['rules'] = list()
    for rule in context['rules']:
        clean_context['rules'].append(rule.component)

    # pickle and save to file
    pickle.dump(clean_context, config_file)
    config_file.close() 

def open_config(file_name):
    new_context = dict()
    return new_context
