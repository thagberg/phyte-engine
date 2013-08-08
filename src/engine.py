from pygame import event

class SystemEntity(object):
	def __init__(self, system, event_types=None):
		self.system = system
		self.event_types = list() if event_types is None else event_types

class PygameEngine(object):
	def __init__(self, systems=None):
		self.systems = list() if systems is None else systems

	def install_system(self, system, event_types=None):
		new_system = SystemEntity(system, event_types)
		self.systems.append(new_system)

	def update(self, time, events):
		for entity in self.systems:
			# TODO: investigate more efficient ways of filtering
			#	the events list; possibly list comprehensions
			entity.system.update(time, 
				filter(lambda x: x.type in entity.event_types, events))
