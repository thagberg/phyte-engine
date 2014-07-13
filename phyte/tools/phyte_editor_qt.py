import sys

from PyQt4 import QtGui, QtCore

from tools.entity_definition_qt import EntityDefinitionEditor
from tools.graphic_definition_qt import GraphicDefinitionEditor
from tools.animation_definition_qt import AnimationDefinitionEditor
from tools.asset_definition_qt import AssetDefinitionEditor
from tools.frame_definition_qt import FrameDefinitionEditor
from tools.hitbox_definition_qt import HitboxDefinitionEditor
from tools.move_definition_qt import MoveDefinitionEditor
from tools.input_definition_qt import InputDefinitionEditor
from tools.binding_definition_qt import BindingDefinitionEditor
from tools.execution_definition_qt import ExecutionDefinitionEditor
from tools.rule_definition_qt import RuleDefinitionEditor
from tools.state_definition_qt import StateDefinitionEditor
from tools.movement_definition_qt import MovementDefinitionEditor
from tools.vector_definition_qt import VectorDefinitionEditor
from tools.physics_definition_qt import PhysicsDefinitionEditor
from tools.debug_definition_qt import DebugDefinitionEditor
from tools.editor_qt import EditorManager
from tools.event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER
from tools import serialize

class PhyteEditor(QtGui.QMainWindow):
    def __init__(self):
        super(PhyteEditor, self).__init__()
        self.initUI()

    def initUI(self):
        top = QtGui.QGridLayout()
        editor_switcher = QtGui.QGridLayout()
        self.center_widget = QtGui.QWidget()
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
        move_editor = MoveDefinitionEditor(self.context)
        input_editor = InputDefinitionEditor(self.context)
        binding_editor = BindingDefinitionEditor(self.context)
        execution_editor = ExecutionDefinitionEditor(self.context)
        rule_editor = RuleDefinitionEditor(self.context)
        state_editor = StateDefinitionEditor(self.context)
        movement_editor = MovementDefinitionEditor(self.context)
        vector_editor = VectorDefinitionEditor(self.context)
        physics_editor = PhysicsDefinitionEditor(self.context)
        debug_editor = DebugDefinitionEditor(self.context)

        # set up menu bar
        save_action = QtGui.QAction('Save', self)
        open_action = QtGui.QAction('Open', self)
        exit_action = QtGui.QAction('Exit', self)
        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)
        save_action.triggered.connect(self.save_config)
        open_action.triggered.connect(self.open_config)

        # add editors to editor manager
        self.editor_manager.add_editor('entity', entity_editor)
        self.editor_manager.add_editor('graphic', graphic_editor)
        self.editor_manager.add_editor('animation', animation_editor)
        self.editor_manager.add_editor('asset', asset_editor)
        self.editor_manager.add_editor('frame', frame_editor)
        self.editor_manager.add_editor('hitbox', hitbox_editor)
        self.editor_manager.add_editor('move', move_editor)
        self.editor_manager.add_editor('input', input_editor)
        self.editor_manager.add_editor('binding', binding_editor)
        self.editor_manager.add_editor('execution', execution_editor)
        self.editor_manager.add_editor('rule', rule_editor)
        self.editor_manager.add_editor('state', state_editor)
        self.editor_manager.add_editor('movement', movement_editor)
        self.editor_manager.add_editor('vector', vector_editor)
        self.editor_manager.add_editor('physics', physics_editor)
        self.editor_manager.add_editor('debug', debug_editor)

        # set up editor view
        entity_editor_item = QtGui.QListWidgetItem('Entity')
        graphic_editor_item = QtGui.QListWidgetItem('Graphic')
        animation_editor_item = QtGui.QListWidgetItem('Animation')
        asset_editor_item = QtGui.QListWidgetItem('Asset')
        frame_editor_item = QtGui.QListWidgetItem('Frame')
        hitbox_editor_item = QtGui.QListWidgetItem('Hitbox')
        move_editor_item = QtGui.QListWidgetItem('Move')
        input_editor_item = QtGui.QListWidgetItem('Input')
        binding_editor_item = QtGui.QListWidgetItem('Binding')
        execution_editor_item = QtGui.QListWidgetItem('Execution')
        rule_editor_item = QtGui.QListWidgetItem('Rule')
        state_editor_item = QtGui.QListWidgetItem('State')
        movement_editor_item = QtGui.QListWidgetItem('Movement')
        vector_editor_item = QtGui.QListWidgetItem('Vector')
        physics_editor_item = QtGui.QListWidgetItem('Physics')
        debug_editor_item = QtGui.QListWidgetItem('Debug')

        self.editor_item_map[entity_editor_item] = 'entity'
        self.editor_item_map[graphic_editor_item] = 'graphic'
        self.editor_item_map[animation_editor_item] = 'animation'
        self.editor_item_map[asset_editor_item] = 'asset'
        self.editor_item_map[frame_editor_item] = 'frame'
        self.editor_item_map[hitbox_editor_item] = 'hitbox'
        self.editor_item_map[move_editor_item] = 'move'
        self.editor_item_map[input_editor_item] = 'input'
        self.editor_item_map[binding_editor_item] = 'binding'
        self.editor_item_map[execution_editor_item] = 'execution'
        self.editor_item_map[rule_editor_item] = 'rule'
        self.editor_item_map[state_editor_item] = 'state'
        self.editor_item_map[movement_editor_item] = 'movement'
        self.editor_item_map[vector_editor_item] = 'vector'
        self.editor_item_map[physics_editor_item] = 'physics'
        self.editor_item_map[debug_editor_item] = 'debug'
        self.editor_selector_view.addItem(entity_editor_item)
        self.editor_selector_view.addItem(graphic_editor_item)
        self.editor_selector_view.addItem(animation_editor_item)
        self.editor_selector_view.addItem(asset_editor_item)
        self.editor_selector_view.addItem(frame_editor_item)
        self.editor_selector_view.addItem(hitbox_editor_item)
        self.editor_selector_view.addItem(move_editor_item)
        self.editor_selector_view.addItem(input_editor_item)
        self.editor_selector_view.addItem(binding_editor_item)
        self.editor_selector_view.addItem(execution_editor_item)
        self.editor_selector_view.addItem(rule_editor_item)
        self.editor_selector_view.addItem(state_editor_item)
        self.editor_selector_view.addItem(movement_editor_item)
        self.editor_selector_view.addItem(vector_editor_item)
        self.editor_selector_view.addItem(physics_editor_item)
        self.editor_selector_view.addItem(debug_editor_item)

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
        editor_switcher.addWidget(move_editor)
        editor_switcher.addWidget(input_editor)
        editor_switcher.addWidget(binding_editor)
        editor_switcher.addWidget(execution_editor)
        editor_switcher.addWidget(rule_editor)
        editor_switcher.addWidget(state_editor)
        editor_switcher.addWidget(movement_editor)
        editor_switcher.addWidget(vector_editor)
        editor_switcher.addWidget(physics_editor)
        editor_switcher.addWidget(debug_editor)
        self.splitter.addWidget(self.editor_selector_view)
        self.splitter.addWidget(holder_widget)
        top.addWidget(self.splitter,0,0)

        # wire up event handlers
        self.editor_selector_view.currentItemChanged.connect(self.select_editor)

        self.center_widget.setLayout(top)
        self.setCentralWidget(self.center_widget)

        self.show()

    def select_editor(self):
        selected_item = self.editor_selector_view.currentItem()
        selected_editor = self.editor_item_map[selected_item]
        self.editor_manager.show_editor(selected_editor)

    def save_config(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save Configuration')
        serialize.save_config(self.context, file_name)

    def open_config(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open Configuration File')
        new_context = serialize.open_config(file_name)
        self.context = new_context
        # fire off event
        new_event = Event('set_context',
                          context=self.context)
        EVENT_MANAGER.fire_event(new_event)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = PhyteEditor()
    app.exec_()


if __name__ == "__main__":
    sys.exit(main())
