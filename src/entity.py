class Entity(object):

	def __init__(self, entity_id, components=None):
		self.entity_id = entity_id
		self.components = list() if components is None else components

	def add_component(self, component):
		self.components.append(component)

	def remove_component(self, component):
		self.components.remove(component)