import animation
import move
import physics2d
import inputs
import game_engine
import entity
import graphics2d
import text
import common
import debug
import player
import execute
import state
import movement
from events import *

from bidict import bidict
from pygame import event
from threading import Lock

class ComponentFactory(object):

    def __init__(self, delegate, entities=None):
        self.delegate = delegate
        # entities are stored in list for contiguous memory allocation
        self.entities = list() if entities is None else entities
        # use this lock whenever adding or deleting from/to the entity list
        self.entities_lock = Lock()
        # append None to entities if no other elements currently exist
        #     this allows us to always be able to use index of None to find
        #     the first open entity id
        if len(self.entities) == 0:
            self.entities.append(None)

    def _get_new_entity_id(self):
        return self.entities.index(None)

    def create_entity(self):
        with self.entities_lock:
            entity_id = self._get_new_entity_id()
            new_entity = entity.Entity(entity_id)
            self.entities.append(new_entity)
        return new_entity

    def remove_entity(self, entity_id):
        with self.entities_lock:
            self.entities[entity_id] = None

    def get_entity(self, entity_id):
        ret = None
        try:
            ret = self.entities[entity_id]
        except Exception as e:
            print "No entity for this id: %s" % entity_id
        return ret

    def get_entities_with_types(self, types):
        e = filter(lambda x: all(t in x.components.keys() for t in types),
                   self.entities)
        return e

    def create_component(self, type, **props):
        component = None

        # InputComponent
        if type == 'input':
            device = props['device']
            entity_id = props['entity_id']
            # TODO: convert bindings to a bidict
            bindings = props.get('bindings', dict())
            mirror_bindings = props.get('mirror_bindings', dict())
            inp_buffer = props.get('inp_buffer', None)
            component = inputs.InputComponent(entity_id, 
                                              bindings, 
                                              mirror_bindings, 
                                              inp_buffer)
            new_event = GameEvent(ADDINPUTCOMPONENT, device=device, component=component,
                                  inp_buffer=inp_buffer)
            self.delegate(new_event)

        # InputBufferComponent
        elif type == 'inbuf':
            entity_id = props['entity_id']
            expire_time = props['expire_time']
            component = inputs.InputBufferComponent(entity_id=entity_id,
                                                    expire_time=expire_time)
            new_event = GameEvent(ADDINPUTBUFFERCOMPONENT, component=component)
            self.delegate(new_event)

        # BindingComponent
        elif type == 'binding':
            entity_id = props['entity_id']

        # GraphicsComponent
        elif type == 'graphics':
            entity_id = props['entity_id']
            surface = props['surface']
            dest = props.get('dest')
            area = props.get('area')
            flgs = props.get('flags')
            active = props.get('active', False)
            component = graphics2d.GraphicsComponent(entity_id=entity_id, 
                                                     surface=surface, 
                                                     dest=dest,
                                                     area=area, 
                                                     flags=flgs, 
                                                     active=active)
            new_event = GameEvent(ADDGRAPHICSCOMPONENT, component=component)
            self.delegate(new_event)

        # TextComponent
        elif type == 'text':
            entity_id = props['entity_id']
            c_text = props['text']
            style = props['style']
            graphic = props['graphic'] if 'graphic' in props else None
            loc = props['loc'] if 'loc' in props else [0,0]
            loc = common.Vector2(entity_id=entity_id, vec=loc)
            active = props.get('active', False)
            component = text.TextComponent(entity_id=entity_id, text=c_text, 
                                           loc=loc, graphic=graphic, 
                                           style=style,
                                           active=active)
            new_event = GameEvent(ADDTEXTCOMPONENT, component=component)
            self.delegate(new_event)

        # LocationComponent
        elif type == 'loc':
            entity_id = props['entity_id']
            point = props['point']
            component = common.LocationComponent(entity_id=entity_id, point=point)  

        # VelocityComponent
        elif type == 'vel':
            entity_id = props['entity_id']
            vel = props['vel']
            component = common.VelocityComponent(entity_id=entity_id, vel=vel)

        # Vector2
        elif type == 'vec2':
            entity_id = props.get('entity_id')
            vec = props['vec']
            component = common.Vector2(entity_id=entity_id, vec=vec)

        # BoxComponent
        elif type == 'hit':
            entity_id = props['entity_id']
            rect = props['rect']
            hit_active = props.get('hit_active', False)
            hurt_active = props.get('hurt_active', False)
            solid = props.get('solid', False)
            expired = props.get('expired', False)
            damage = props.get('damage', 0)
            stun = props.get('stun', 0)
            hitstun = props.get('hitstun', 0)
            if 'push' in props:
                push = props['push']
            else:
                push = self.create_component('vel', 
                                             entity_id=entity_id,
                                             vel=(0,0))
            moveable = props.get('moveable', False)
            component = common.BoxComponent(entity_id=entity_id, 
                                            rect=rect,
                                            hitactive=hit_active,
                                            hurtactive=hurt_active,
                                            solid=solid,
                                            expired=expired, 
                                            damage=damage,
                                            stun=stun, 
                                            hitstun=hitstun,
                                            push=push,
                                            moveable=moveable)

        # FrameComponent
        elif type == 'fra':
            entity_id = props['entity_id']
            crop = props['crop']
            repeat = props['repeat']
            hitboxes = props.get('hitboxes')
            force = props.get('force')
            push_box = props.get('push_box')
            component = animation.FrameComponent(entity_id=entity_id,
                                                 hitboxes=hitboxes, force=force,
                                                 crop=crop, repeat=repeat,
                                                 push_box=push_box)
        # AnimationComponent
        elif type == 'ani':
            entity_id = props['entity_id']
            frames = props['frames']
            loop = props['loop']
            graphic = props['graphic']
            component = animation.AnimationComponent(entity_id=entity_id,
                                                     frames=frames,
                                                     loop=loop,
                                                     graphic=graphic)
            new_event = GameEvent(ADDANIMATIONCOMPONENT, component=component)
            self.delegate(new_event)

        # DebugComponent
        elif type == 'deb':
            entity_id = props['entity_id']
            c_text = props.get('text')
            rect = props.get('rect')
            line = props.get('line')
            ellipse = props.get('ellipse')
            circle = props.get('circle')
            arc = props.get('arc')
            style = props.get('style')
            get_value = props.get('get_value')
            active = props.get('active', False)
            component = debug.DebugComponent(entity_id=entity_id, text=c_text,
                                             get_value=get_value, rect=rect, 
                                             line=line, ellipse=ellipse, 
                                             circle=circle, arc=arc, style=style,
                                             active=active)
            new_event = GameEvent(ADDDEBUGCOMPONENT, component=component)
            self.delegate(new_event)

        # PlayerComponent
        elif type == 'pla':
            entity_id = props['entity_id']
            location = props['location']
            b_moves = props.get('buffered_moves')
            i_moves = props.get('immediate_moves')
            p_inputs = props.get('inputs')
            graphic = props.get('graphic')
            input_device = -1 if not 'input_device' in props else props['input_device']    
            component = player.PlayerComponent(entity_id=entity_id,
                                               location=location,
                                               buffered_moves=b_moves,
                                               immediate_moves=i_moves,
                                               inputs=p_inputs, graphic=graphic,
                                               input_device=input_device)
            new_event = GameEvent(ADDPLAYERCOMPONENT, component=component)
            self.delegate(new_event)

        # MoveComponent
        elif type == 'move':
            entity_id = props['entity_id']
            name = props['name']
            m_animation = props['animation']
            m_inputs = props['inputs']
            rules = props.get('rules')
            component = move.MoveComponent(entity_id=entity_id, name=name,
                                           animation=m_animation, inputs=m_inputs,
                                           rules=rules)
            new_event = GameEvent(ADDMOVECOMPONENT, component=component)
            self.delegate(new_event)

        # ExecutionComponent
        elif type == 'exe':
            entity_id = props['entity_id']
            if 'executables' in props:
                executables = props['executables']
            else:
                executables = None
            mirror = False
            active = False
            e_input = props['inputs']
            component = execute.ExecutionComponent(entity_id=entity_id,
                                                   executables=executables,
                                                   inputs=e_input,
                                                   mirror=mirror, active=active)
            new_event = GameEvent(ADDEXECUTIONCOMPONENT, component=component)
            self.delegate(new_event)

        # BufferedExecutionComponent
        elif type == 'bexe':
            entity_id = props['entity_id']
            if 'executables' in props:
                executables = props['executables']
            else:
                executables = None
            mirror = False
            active = False
            component = execute.ExecutionComponent(entity_id=entity_id,
                                                   executables=executables,
                                                   mirror=mirror, active=active)
            new_event = GameEvent(ADDBUFFEREDEXECUTIONCOMPONENT, 
                                  component=component)
            self.delegate(new_event)

        # RuleComponent
        elif type == 'rule':
            name = props['name']
            operator = props['operator']
            value = props['value']    
            component = state.RuleComponent(name=name, operator=operator,
                                            value=value)

        # StateComponent
        elif type == 'state':
            entity_id = props['entity_id']
            rules = props['rules']
            aet = props['activation_event_type']
            daet = props['deactivation_event_type']
            ac = props['activation_component']
            rule_values = props['rule_values']
            component = state.StateComponent(entity_id=entity_id, rules=rules,
                                             activation_event_type=aet,
                                             deactivation_event_type=daet,
                                             activation_component=ac,
                                             rule_values=rule_values)
            new_event = GameEvent(ADDSTATECOMPONENT, component=component)
            self.delegate(new_event)

        # StateValueComponent
        elif type == 'stateval':
            entity_id = props['entity_id']
            active = props['active']
            component = state.StateValueComponent(entity_id=entity_id,
                                                  active=active)    

        # MovementComponent
        elif type == 'movement':
            entity_id = props['entity_id']
            body = props['body']
            velocity = props.get('velocity')
            pulse_velocity = props.get('pulse_velocity')
            parent = props.get('parent')
            component = movement.MovementComponent(entity_id=entity_id,
                                                   body=body,
                                                   velocity=velocity,
                                                   pulse_velocity=pulse_velocity,
                                                   parent=parent)
            new_event = GameEvent(ADDMOVEMENTCOMPONENT, component=component)
            self.delegate(new_event)

        # VaryingMovementComponent
        elif type == 'varmovement':
            entity_id = props['entity_id']
            body = props['body']
            velocity_func = props.get('velocity_func')
            parent = props.get('parent')
            component = movement.VaryingMovementComponent(entity_id=entity_id,
                                                          body=body,
                                                          velocity_func=velocity_func,
                                                          parent=parent)
            new_event = GameEvent(ADDMOVEMENTCOMPONENT, component=component)
            self.delegate(new_event)

        # Incidental MovementComponent
        elif type == 'incmovement':
            entity_id = props['entity_id']
            body = props['body']
            velocity = props.get('velocity')
            component = movement.MovementComponent(entity_id=entity_id,
                                                   body=body,
                                                   velocity=velocity)
            new_event = GameEvent(APPLYINCIDENTALMOVEMENTCOMPONENT,
                                  component=component)
            self.delegate(new_event)

        # PhysicsComponent
        elif type == 'physics':
            entity_id = props['entity_id']
            box = props['box']
            body = props['body']
            active_type = props.get('active', False)
            if active_type:
                event_type = ADDPHYSICSCOMPONENTACTIVE
            else:
                event_type = ADDPHYSICSCOMPONENT
            component = physics2d.PhysicsComponent(entity_id=entity_id,
                                                   box=box,
                                                   body=body)
            new_event = GameEvent(event_type, component=component)
            self.delegate(new_event)

        return component
