import animation
import move
import physics2d
import inputs
import engine
import entity
import graphics2d
import text
import common
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
			component = inputs.InputComponent(entity_id, bindings)
			new_event = GameEvent(ADDINPUTCOMPONENT, device=device, component=component)
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
            #TODO: add animation construction


		return component




