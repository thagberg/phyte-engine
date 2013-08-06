import animation
import move
import physics2d
import inputs
import engine

from events import *
from pygame import event

class ComponentFactory(object):

	def __init__(self, entities=None):
		# entities are stored in list for contiguous memory allocation
		self.entities = list() if entities is None else entities
		# append None to entities if no other elements currently exist
		#     this allows us to always be able to use index of None to find
		#     the first open entity id
		if len(self.entities) == 0:
			self.entities.append(None)

	def _get_new_entity_id(self):
		return self.entities.index(None)

	def create_component(self, type, **props):

		# InputComponent
		if type == 'input'
			device = props['device']
			entity_id = props['entity_id']
			bindings = dict()
			if 'bindings' in props:
				for name, key in props['bindings']:
					bindings[name] = inputs.BindingComponent(entity_id, key)
			component = inputs.InputComponent(entity_id, bindings)
			new_event = event.Event(ADDINPUTCOMPONENT, device=device, component=component)
			event.post(new_event)




