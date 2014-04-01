import sys

from PyQt4 import QtGui, QtCore

from entity_definition_qt import EntityDefinitionEditor
from graphic_definition_qt import GraphicDefinitionEditor
from animation_definition_qt import AnimationDefinitionEditor
from editor_qt import EditorManager

class PhyteEditor(QtGui.QWidget):
    def __init__(self):
        super(PhyteEditor, self).__init__()
        self.initUI()

    def initUI(self):
        top = QtGui.QGridLayout()
        editor_switcher = QtGui.QGridLayout()
        self.context = dict()
        self.editor_selector_view = QtGui.QListWidget()
        self.editor_item_map = dict()
        self.editor_manager = EditorManager()
        entity_editor = EntityDefinitionEditor(self.context)
        graphic_editor = GraphicDefinitionEditor(self.context)
        animation_editor = AnimationDefinitionEditor(self.context)

        # add editors to editor manager
        self.editor_manager.add_editor('entity', entity_editor)
        self.editor_manager.add_editor('graphic', graphic_editor)
        self.editor_manager.add_editor('animation', animation_editor)

        # set up editor view
        entity_editor_item = QtGui.QListWidgetItem('Entity')
        graphic_editor_item = QtGui.QListWidgetItem('Graphic')
        animation_editor_item = QtGui.QListWidgetItem('Animation')

        self.editor_item_map[entity_editor_item] = 'entity'
        self.editor_item_map[graphic_editor_item] = 'graphic'
        self.editor_item_map[animation_editor_item] = 'animation'
        self.editor_selector_view.addItem(entity_editor_item)
        self.editor_selector_view.addItem(graphic_editor_item)
        self.editor_selector_view.addItem(animation_editor_item)

        # set up layout
        self.splitter = QtGui.QSplitter()
        holder_widget = QtGui.QWidget()
        holder_widget.setLayout(editor_switcher)
        editor_switcher.addWidget(entity_editor)
        editor_switcher.addWidget(graphic_editor)
        editor_switcher.addWidget(animation_editor)
        self.splitter.addWidget(self.editor_selector_view)
        self.splitter.addWidget(holder_widget)
        top.addWidget(self.splitter,0,0)
        #top.addWidget(self.editor_selector_view,0,0)
        #top.addWidget(entity_editor.group, 0, 1)
        #top.addWidget(graphic_editor.group,0, 1)
        #top.addWidget(animation_editor.group,0,1)

        # wire up event handlers
        self.editor_selector_view.currentItemChanged.connect(self.select_editor)

        self.setLayout(top)

        self.show()

    def select_editor(self):
        selected_item = self.editor_selector_view.currentItem()
        selected_editor = self.editor_item_map[selected_item]
        self.editor_manager.show_editor(selected_editor)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = PhyteEditor()

    sys.exit(app.exec_())

main()
