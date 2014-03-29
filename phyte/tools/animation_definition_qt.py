from PyQt4 import QtGui

from editor_qt import Editor
from common import Component
from engine.animation import AnimationComponent


class AnimationDefinitionEditor(Editor):
    def __init__(self, context):
        super(AnimationDefinitionEditor, self).__init__(context,
                                                        QtGui.QGroupBox('Animation'))
        self.layout = QtGui.QGridLayout()
        self.animation_name_field = QtGui.QLineEdit()
        self.animation_name_label = QtGui.QLabel('Animation Name')
        self.animation_list_view = QtGui.QListWidget()
        self.add_animation_button = QtGui.QPushButton('Add Animation')
        self.remove_animation_button = QtGui.QPushButton('Remove Animation')
        self.animation_buttons_layout = QtGui.QVBoxLayout()
        self.graphic_list_view = QtGui.QListWidget()
        self.graphic_list_label = QtGui.QLabel('Choose Graphic')
        self.graphic_list_layout = QtGui.QVBoxLayout()

        # setup layout
        self.graphic_list_layout.addWidget(self.graphic_list_label)
        self.graphic_list_layout.addWidget(self.graphic_list_view)
        self.layout.addLayout(self.graphic_list_layout,0,0)
        self.layout.addWidget(self.animation_name_label,0,1)
        self.layout.addWidget(self.animation_name_field,0,2)
        self.layout.addWidget(self.animation_list_view,1,0)
        self.animation_buttons_layout.addWidget(self.add_animation_button)
        self.animation_buttons_layout.addWidget(self.remove_animation_button)
        self.layout.addLayout(self.animation_buttons_layout,1,1)

        self.group.setLayout(self.layout)

        # wire up event handlers
        self.add_animation_button.clicked.connect(self.add_animation)
        self.remove_animation_button.clicked.connect(self.remove_animation)
        self.graphic_list_view.currentItemChanged.connect(self.select_graphic)
        self.animation_list_view.currentItemChanged.connect(self.select_animation)

    def add_animation(self):
        pass

    def remove_animation(self):
        pass

    def select_graphic(self):
        pass

    def select_animation(self):
        pass
