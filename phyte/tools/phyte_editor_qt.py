import sys

from PyQt4 import QtGui, QtCore

from entity_definition_qt import EntityDefinitionEditor
from graphic_definition_qt import GraphicDefinitionEditor
from animation_definition_qt import AnimationDefinitionEditor
from asset_definition_qt import AssetDefinitionEditor
from frame_definition_qt import FrameDefinitionEditor
from hitbox_definition_qt import HitboxDefinitionEditor
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
        asset_editor = AssetDefinitionEditor(self.context)
        frame_editor = FrameDefinitionEditor(self.context)
        hitbox_editor = HitboxDefinitionEditor(self.context)

        # add editors to editor manager
        self.editor_manager.add_editor('entity', entity_editor)
        self.editor_manager.add_editor('graphic', graphic_editor)
        self.editor_manager.add_editor('animation', animation_editor)
        self.editor_manager.add_editor('asset', asset_editor)
        self.editor_manager.add_editor('frame', frame_editor)
        self.editor_manager.add_editor('hitbox', hitbox_editor)

        # set up editor view
        entity_editor_item = QtGui.QListWidgetItem('Entity')
        graphic_editor_item = QtGui.QListWidgetItem('Graphic')
        animation_editor_item = QtGui.QListWidgetItem('Animation')
        asset_editor_item = QtGui.QListWidgetItem('Asset')
        frame_editor_item = QtGui.QListWidgetItem('Frame')
        hitbox_editor_item = QtGui.QListWidgetItem('Hitbox')

        self.editor_item_map[entity_editor_item] = 'entity'
        self.editor_item_map[graphic_editor_item] = 'graphic'
        self.editor_item_map[animation_editor_item] = 'animation'
        self.editor_item_map[asset_editor_item] = 'asset'
        self.editor_item_map[frame_editor_item] = 'frame'
        self.editor_item_map[hitbox_editor_item] = 'hitbox'
        self.editor_selector_view.addItem(entity_editor_item)
        self.editor_selector_view.addItem(graphic_editor_item)
        self.editor_selector_view.addItem(animation_editor_item)
        self.editor_selector_view.addItem(asset_editor_item)
        self.editor_selector_view.addItem(frame_editor_item)
        self.editor_selector_view.addItem(hitbox_editor_item)

        # set up layout
        self.splitter = QtGui.QSplitter()
        holder_widget = QtGui.QWidget()
        holder_widget.setLayout(editor_switcher)
        editor_switcher.addWidget(entity_editor)
        editor_switcher.addWidget(graphic_editor)
        editor_switcher.addWidget(animation_editor)
        editor_switcher.addWidget(asset_editor)
        editor_switcher.addWidget(frame_editor)
        editor_switcher.addWidget(hitbox_editor)
        self.splitter.addWidget(self.editor_selector_view)
        self.splitter.addWidget(holder_widget)
        top.addWidget(self.splitter,0,0)

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
