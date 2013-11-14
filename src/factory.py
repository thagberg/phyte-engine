import animation
import move
import physics2d
import inputs
import engine
import entity
import graphics2d
import text
import common
import debug
import player
import execute
import state
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
            bindings = dict() if not 'bindings' in props else props['bindings']
            inp_buffer = None if not 'inp_buffer' in props else props['inp_buffer']
            component = inputs.InputComponent(entity_id, bindings)
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
            dest = None if not 'dest' in props else props['dest']
            area = None if not 'area' in props else props['area']
            flgs = None if not 'flags' in props else props['flags']
            component = graphics2d.GraphicsComponent(entity_id, surface, dest,
                                                   area, flgs)
            new_event = GameEvent(ADDGRAPHICSCOMPONENT, component=component)
            self.delegate(new_event)

        # TextComponent
        elif type == 'text':
            entity_id = props['entity_id']
            c_text = props['text']
            style = props['style']
            graphic = props['graphic'] if 'graphic' in props else None
            loc = props['loc'] if 'loc' in props else [0,0]
            component = text.TextComponent(entity_id=entity_id, text=c_text, 
                                           loc=loc, graphic=graphic, 
                                           style=style)
            new_event = GameEvent(ADDTEXTCOMPONENT, component=component)
            self.delegate(new_event)

        # LocationComponent
        elif type == 'loc':
            entity_id = props['entity_id']
            point = props['point']
            component = common.LocationComponent(entity_id=entity_id, point=point)  

        # MovementComponent
        elif type == 'movement':
            entity_id = props['entity_id']
            walk_speed = props['walk_speed']
            back_speed = props['back_speed']
            jump_height = props['jump_height']
            component = common.MovementComponent(entity_id=entity_id,
                                                 walk_speed=walk_speed,
                                                 back_speed=back_speed,
                                                 jump_height=jump_height)

        # VelocityComponent
        elif type == 'vel':
            entity_id = props['entity_id']
            vel = props['vel']
            component = common.VelocityComponent(entity_id=entity_id, vel=vel)

        # HitboxComponent
        elif type == 'hit':
            entity_id = props['entity_id']
            rect = props['rect']
            hit_active = props['hit_active'] if 'hit_active' in props else False
            hurt_active = props['hurt_active'] if 'hurt_active' in props else False
            push_active = props['push_active'] if 'push_active' in props else False
            expired = props['expired'] if 'expired' in props else False
            damage = props['damage'] if 'damage' in props else 0
            stun = props['stun'] if 'stun' in props else 0
            hitstun = props['hitstun'] if 'hitstun' in props else 0
            if 'push' in props:
                push = props['push']
            else:
                push = self.create_component('vel', (0,0))
            component = physics2d.HitboxComponent(entity_id=entity_id, rect=rect,
                                                  hit_active=hit_active,
                                                  hurt_active=hurt_active,
                                                  push_active=push_active,
                                                  expired=expired, damage=damage,
                                                  stun=stun, hitstun=hitstun,
                                                  push=push)

        # FrameComponent
        elif type == 'fra':
            entity_id = props['entity_id']
            hitboxes = props['hitboxes']
            force = props['force']
            crop = props['crop']
            repeat = props['repeat']
            push_box = props['push_box']
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
            c_text = None if not 'text' in props else props['text']
            rect = None if not 'rect' in props else props['rect']
            line = None if not 'line' in props else props['line']
            ellipse = None if not 'ellipse' in props else props['ellipse']
            circle = None if not 'circle' in props else props['circle']
            arc = None if not 'arc' in props else props['arc']
            style = None if not 'style' in props else props['style']
            get_value = None if not 'get_value' in props else props['get_value']
            component = debug.DebugComponent(entity_id=entity_id, text=c_text,
                                             get_value=get_value, rect=rect, 
                                             line=line, ellipse=ellipse, 
                                             circle=circle, arc=arc, style=style)
            new_event = GameEvent(ADDDEBUGCOMPONENT, component=component)
            self.delegate(new_event)

        # PlayerComponent
        elif type == 'pla':
            entity_id = props['entity_id']
            location = props['location']
            b_moves = None if not 'buffered_moves' in props else props['buffered_moves']
            i_moves = None if not 'immediate_moves' in props else props['immediate_moves']
            p_inputs = None if not 'inputs' in props else props['inputs']
            graphic = None if not 'graphic' in props else props['graphic']
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
            rules = None if not 'rules' in props else props['rules']
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

        return component
