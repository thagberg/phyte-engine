from PyQt4 import QtGui, QtCore

from event import Event, EVENT_QUEUE

class Editor(QtGui.QWidget):
    def __init__(self, context, group=None):
        super(Editor, self).__init__()
        self.context = context
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        self.group = group if group is not None else QtGui.QGroupBox('Editor')
        self.layout.addWidget(self.group)
        self.setLayout(self.layout)
        self.hide()


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
