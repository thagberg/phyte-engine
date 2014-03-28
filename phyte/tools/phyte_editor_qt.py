import sys
from collections import defaultdict

from PyQt4 import QtGui, QtCore

from entity_definition_qt import EntityDefinitionEditor
from graphic_definition_qt import GraphicDefinitionEditor
from editor_qt import EditorManager

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        top = QtGui.QGridLayout()
        self.context = defaultdict(object)
        self.editor_manager = EditorManager()
        entity_editor = EntityDefinitionEditor(self.context)
        graphic_editor = GraphicDefinitionEditor(self.context)

        self.editor_manager.add_editor('entity', entity_editor)
        self.editor_manager.add_editor('graphic', graphic_editor)

        top.addWidget(entity_editor.group, 0, 0)
        top.addWidget(graphic_editor.group,0, 0)

        self.editor_manager.show_editor('graphic')

        self.setLayout(top)

        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())

main()
