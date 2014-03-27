import sys

from PyQt4 import QtGui, QtCore

from entity_definition_qt import EntityDefinitionEditor

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        top = QtGui.QGridLayout()
        self.context = dict()
        self.entity_editor = EntityDefinitionEditor(self.context)

        top.addWidget(self.entity_editor.group, 0, 0)

        self.setLayout(top)

        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())

main()