from PyQt4 import QtGui, QtCore

from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER

class Editor(QtGui.QWidget):
    def __init__(self, context, group=None):
        super(Editor, self).__init__()
        self.context = context
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        self.group = group if group is not None else QtGui.QGroupBox('Editor')
        self.layout.addWidget(self.group)
        self.setLayout(self.layout)
        self.hide()

        # internal events
        EVENT_MAPPING.register_handler('set_context', self.set_context)

    def set_context(self, event):
        self.context = event.context
        self.update()

    def update(self):
        pass


class EditorManager(object):
    def __init__(self):
        self.editor_map = dict()

    def add_editor(self, name, editor):
        self.editor_map[name] = editor

    def remove_editor(self, name):
        self.editor_map.pop(name, None)

    def show_editor(self, name):
        if name in self.editor_map:
            for key, editor in self.editor_map.iteritems():
                if key == name:
                    editor.show()
                else:
                    editor.hide()
