import pygame
import yaml

import events
from engine import physics2d
from tools import common as t_common

def load(file_name, factory):
    config_file = open(file_name, 'r')
    context = yaml.load(config_file)
    game_context = dict()
    entity_mapping = dict()
    create = factory.create_component # simple alias to keep things clean

    # create assets
    asset_map = dict()
    for asset in [x.component for x in context['assets']]:
        if asset.file_name not in asset_map:
            surface = pygame.image.load(asset.file_name)
            asset_map[asset.file_name] = surface

    # some hacky shit, used to create a map between editor components
    # and runtime components to ensure that inter-component dependencies
    # are maintained.
    # TODO: figure out a better way to do this so that we aren't
    # temporarily holding 2 copies of each component in memory...
    component_map = dict()

    for inp in context['inputs']:
        pass

    # create all of the necessary entities
    for name, entity in context['entities'].iteritems():
        new_entity = factory.create_entity()
        entity_id = new_entity.entity_id
        entity_mapping[name] = new_entity

        # to prevent problems, we have to deserialize components in a
        # certain order based on component type
        # this prevents issues related to component dependencies
        en_comps = entity['components']

        for component in en_comps['vector']:
            inner_comp = component.component
            new_component = create('vec2',
                                   entity_id=entity_id,
                                   vec=[inner_comp.x, inner_comp.y])
            component_map[component] = new_component

        for component in en_comps['hitbox']:
            inner_comp = component.component
            new_component = create('hit',
                                   entity_id=entity_id,
                                   rect=inner_comp.rect,
                                   hit_active=inner_comp.hitactive,
                                   hurt_active=inner_comp.hurtactive,
                                   solid=inner_comp.solid,
                                   expired=inner_comp.expired,
                                   damage=inner_comp.damage,
                                   stun=inner_comp.stun,
                                   hitstun=inner_comp.hitstun,
                                   push=inner_comp.push,
                                   moveable=inner_comp.moveable)
            component_map[component] = new_component
            # a solid hitbox should have a concomitant physics component
            if new_component.solid:
                physics_comp = physics2d.PhysicsComponent(entity_id=entity_id,
                                                          box=component,
                                                          body=None)
                physics_comp = t_common.Component(physics_comp, component.text)
                en_comps['physics'].append(physics_comp)

        for component in en_comps['frame']:
            inner_comp = component.component
            hitboxes = [component_map[x] for x in inner_comp.hitboxes]
            new_component = create('fra',
                                   entity_id=entity_id,
                                   crop=inner_comp.crop,
                                   repeat=inner_comp.repeat,
                                   hitboxes=hitboxes,
                                   force=inner_comp.force,
                                   push_box=inner_comp.push_box)
            component_map[component] = new_component

        for component in en_comps['graphic']:
            inner_comp = component.component
            dest = component_map[inner_comp.dest]
            new_component = create('graphics',
                                   entity_id=entity_id,
                                   surface=asset_map[inner_comp.file_name],
                                   dest=dest,
                                   area=inner_comp.area,
                                   flgs=inner_comp.flags,
                                   #active=inner_comp.active)
                                   active=True)
            component_map[component] = new_component

        for component in en_comps['animation']:
            inner_comp = component.component

            # first make sure that all of the frames for
            # this animation have already been processed
            for frame in [x for x in inner_comp.frames if component_map.get(x, None) is None]:
                frame_comp = frame.component
                hitboxes = [component_map[x] for x in frame_comp.hitboxes]
                new_component = create('fra',
                                       entity_id=entity_id,
                                       crop=frame_comp.crop,
                                       repeat=frame_comp.repeat,
                                       hitboxes=hitboxes,
                                       force=frame_comp.force,
                                       push_box=frame_comp.push_box)
                component_map[frame] = new_component
                
            frames = [component_map[x] for x in inner_comp.frames]
            graphic = component_map[inner_comp.graphic]
            new_component = create('ani',
                                   entity_id=entity_id,
                                   frames=frames,
                                   loop=inner_comp.loop,
                                   graphic=graphic)
            component_map[component] = new_component

        for component in en_comps['rule']:
            inner_comp = component.component
            new_component = create('rule',
                                   entity_id=entity_id,
                                   operator=inner_comp.operator,
                                   name=inner_comp.name,
                                   value=inner_comp.value)
            component_map[component] = new_component

        for component in en_comps['move']:
            inner_comp = component.component
            animation = component_map[inner_comp.animation]
            inps = list()
            for inp_list in [x.component for x in inner_comp.inputs]:
                inps.append([x.component.name for x in inp_list])
            rules = [component_map[x] for x in inner_comp.rules]
            new_component = create('move',
                                   entity_id=entity_id,
                                   name=inner_comp.name,
                                   animation=animation,
                                   inputs=inps,
                                   rules=rules)
            component_map[component] = new_component

        for component in en_comps['binding']:
            inner_comp = component.component
            clean_bindings = dict()
            for name, key in inner_comp.bindings.iteritems():
                clean_bindings[name] = key.component.key.component.key
            mirror_bindings = dict()
            for name, inp in inner_comp.mirror_bindings.iteritems():
                if inp is not None:
                    mirror_bindings[key] = inp.component.name
            new_component = create('input',
                                   entity_id=entity_id,
                                   device=-1,
                                   bindings=clean_bindings,
                                   mirror_bindings=mirror_bindings)
            component_map[component] = new_component

        for component in en_comps['execution']:
            inner_comp = component.component
            executables = [component_map[x] for x in inner_comp.executables]
            #executables = inner_comp.executables
            inputs = component_map[inner_comp.inputs]
            new_component = create('exe',
                                   entity_id=entity_id,
                                   executables=executables,
                                   inputs=inputs)
            component_map[component] = new_component

        for component in en_comps['physics']:
            inner_comp = component.component
            rect = component_map[inner_comp.box].rect
            box = create('hit',
                         entity_id=entity_id,
                         rect=rect,
                         hit_active=False,
                         hurt_active=False,
                         block_active=False,
                         solid=True,
                         damage=0,
                         stun=0,
                         hitstun=0,
                         push=None,
                         moveable=False)
            component_map[inner_comp.box] = box
            new_component = create('physics',
                                   entity_id=entity_id,
                                   box=box,
                                   body=inner_comp.body,
                                   active=False)
            component_map[component] = new_component

        for component in en_comps['movement']:
            inner_comp = component.component
            body = component_map[inner_comp.body]
            velocity = component_map.get(inner_comp.velocity, None)
            pulse_velocity = component_map.get(inner_comp.pulse_velocity, None)
            parent = component_map.get(inner_comp.parent, None)
            new_component = create('movement',
                                   entity_id=entity_id,
                                   body=body,
                                   velocity=velocity,
                                   pulse_velocity=pulse_velocity,
                                   parent=parent)
            component_map[component] = new_component

        for component in en_comps['text']:
            inner_comp = component.component
            text = inner_comp.text
            loc = component_map.get(inner_comp.loc, None)
            graphic = component_map.get(inner_comp.graphic, None)
            style = inner_comp.style
            cleaned_style = {x:y.component for x,y in style.iteritems()}
            new_component = create('text',
                                   entity_id=entity_id,
                                   text=text,
                                   loc=loc,
                                   graphic=graphic,
                                   style=cleaned_style)
            component_map[component] = new_component

        for component in en_comps['debug']:
            def _make_get_value(comp, attr):
                '''
                    Doing this in a function in order to trick
                    Python's block scoping so that the returned lambda
                    doesn't get overwritten on every new debug component.
                    Otherwise, the lambda shares the name scope of this
                    loop, and will "notice" that lambda_comp and lambda_attr
                    are changing on each iteration, and thus every single
                    debug component will use the same get_value attribute
                '''
                return lambda: getattr(comp, attr)

            inner_comp = component.component
            active = True
            text = component_map.get(inner_comp.text, None)
            rect = component_map.get(inner_comp.rect, None)
            style = inner_comp.style
            cleaned_style = {x:y.component for x,y in style.iteritems()}
            lambda_comp = component_map.get(inner_comp.get_value.component, None)
            lambda_attr = inner_comp.get_value.attr
            get_value = _make_get_value(lambda_comp, lambda_attr)
            new_component = create('deb',
                                   entity_id=entity_id,
                                   active=active,
                                   text=text,
                                   rect=rect,
                                   style=cleaned_style,
                                   get_value=get_value)
            component_map[component] = new_component

        for component in en_comps['state']:
            def _make_rule_value_lambda(comp, attr):
                '''
                    See help for _make_get_value in debug component
                    deserializer
                '''
                return lambda: getattr(comp, attr)

            inner_comp = component.component
            activation_comp = component_map[inner_comp.activation_component]
            aet = events.__dict__[inner_comp.activation_event_type]
            daet = events.__dict__[inner_comp.deactivation_event_type]
            # because of the awkwardness of pickling lambda functions,
            # need to generate the lambda at load-time
            rule_values = dict()
            for name, rule_value in inner_comp.rule_values.iteritems():
                if rule_value.__class__.__name__ == 'LambdaDef':
                    #rule_values[name] = rule_value.get_lambda()
                    temp_comp = component_map[rule_value.component]
                    rule_values[name] = _make_rule_value_lambda(temp_comp, rule_value.attr)
                else:
                    try:
                        rule_values[name] = float(rule_value)
                    except ValueError:
                        rule_values[name] = rule_value
            rules = [x.component for x in inner_comp.rules]
            new_component = create('state',
                                   entity_id=entity_id,
                                   rules=rules,
                                   activation_event_type=aet,
                                   deactivation_event_type=daet,
                                   activation_component=activation_comp,
                                   rule_values=rule_values)
            component_map[component] = new_component
