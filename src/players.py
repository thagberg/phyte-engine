from system import System
from events import *
from collections import defaultdict

class MeterComponent(object):
	def __init__(self, entity_id, meter_type, value=0, sentinels=(0,0)):
		self.entity_id = entity_id
		self.meter_type = meter_type
		self.value = value
		self.sentinels = sentinels

class MeterSystem(System):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = defaultdict(dict) if components is None else components

	def handle_event(self, event):
		if event.type == ADDMETERCOMPONENT:
			self.components[event.entity_id][event.meter_type] = event.component
		elif event.type == REMOVEHEALTHCOMPONENT:
			try:
				del self.components[event.entity_id][event.meter_type]
			except KeyError, e:
				print "Cannot remove meter component for this entity and type"
		elif event.type == UPDATEMETER:
			m_comp = self.components[event.entity_id][event.meter_type]
			m_comp.value += event.change
			if m_comp.value <= m_comp.sentinels[0]:
				new_event = GameEvent(EMPTYMETER, entity_id=m_comp.entity_id,
									  component=m_comp)
				self.delegate(new_event)
			elif m_comp.value >= m_comp.sentinels[1]:
				new_event = GameEvent(FULLMETER, entity_id=m_comp.entity_id,
									  component=m_comp)
				self.delegate(new_event)

	def update(self, time):
		self.delta = time
		pass

