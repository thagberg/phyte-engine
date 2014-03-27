from PyQt4 import QtGui

from editor_qt import Editor
from common import Component
from engine.graphics2D import GraphicsComponent


class GraphicDefinitionEditor(Editor):
    def __init__(self, context):
        super(GraphicDefinitionEditor, self).__init__(context)
        self.group = QtGui.QGroupBox('Graphics')
        self.layout =  QtGui.QGridLayout()
        self.graphic_file_name_field = QtGui.QLineEdit()
        self.graphic_file_button = QtGui.QPushButton('Choose Graphic')
        self.graphic_list_view = QtGui.QListWidget()
        self.add_graphic_button = QtGui.QPushButton('Add Graphic')
        self.remove_graphic_button = GtQui.QPushButton('Remove Graphic')

        # setup layout
        self.layout.addWidget(self.graphic_file_name_field,0,0)
        self.layout.addWidget(self.graphic_file_button,0,1)
        self.layout.addWidget(self.graphic_list_view,1,0)
        self.layout.addWidget(self.add_graphic_button,2,0)
        self.layout.addWidget(self.remove_graphic_button,2,1)

        self.graphic_file_button.clicked.connect(self.open_file_dialog)
        self.add_graphic_button.clicked.connect(self.add_graphic)
        self.remove_graphic_button.clicked.connect(self.remove_graphic)

    def open_file_dialog(self):
        file_name = QtGui.QFileDIalog.getOpenFileName(self, 'Choose Graphic', '/home')
        graphic_file = open(file_name, 'r') 
        self.graphic_file_name_field.setText(file_name)

    def add_graphic(self):
        file_name = self.graphic_file_name_field.getText()
        graphic_item = QtGui.QListWidgetItem()
        self.graphic_list_view.addItem(graphic_item)

    def remove_graphic(self):
        pass
