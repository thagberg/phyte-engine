class System(object):
	def __init__(self):
		self.delegate = None

	def attach_delegate(self, delegate):
		self.delegate = delegate