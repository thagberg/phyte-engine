class System(object):
	def __init__(self):
		self.delegate = None
        self.delta = 0

	def attach_delegate(self, delegate):
		self.delegate = delegate

    def _add(self, component):
        pass

    def _remove(self, component):
        pass
