import sys
from collections import defaultdict

from PyQt4 import QtGui, QtCore

from entity_definition_qt import EntityDefinitionEditor
from graphic_definition_qt import GraphicDefinitionEditor

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        top = QtGui.QGridLayout()
        self.context = defaultdict(object)
        self.entity_editor = EntityDefinitionEditor(self.context)
        self.graphic_editor = GraphicDefinitionEditor(self.context)

        self.entity_editor.group.hide()
        #self.graphic_editor.group.hide()

        top.addWidget(self.entity_editor.group, 0, 0)
        top.addWidget(self.graphic_editor.group,0, 0)

        self.setLayout(top)

        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())

main()
