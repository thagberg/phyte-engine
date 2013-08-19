import animation
import move
import physics2d
import inputs
import engine
import entity
import graphics2d
from events import *

from bidict import bidict
from pygame import event
from threading import Lock

class ComponentFactory(object):

	def __init__(self, entities=None):
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
			new_event = event.Event(INPUTEVENT, subtype=ADDINPUTCOMPONENT, 
									device=device, component=component)
			event.post(new_event)

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
			component = graphics.GraphicsComponent(entity_id, surface, dest,
												   area, flgs)
			new_event = event.EVENT(GRAPHICSEVENT, subtype=ADDGRAPHICSCOMPONENT,
									component=component)
			event.post(new_event)

		return component




