from PyQt4 import QtGui

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.graphics2d import GraphicsComponent


class GraphicDefinitionEditor(Editor):
    def __init__(self, context):
        super(GraphicDefinitionEditor, self).__init__(context, QtGui.QGroupBox('Graphics'))
        self.layout =  QtGui.QGridLayout()
        self.view_buttons_layout = QtGui.QVBoxLayout()
        self.graphic_file_name_field = QtGui.QLineEdit()
        self.graphic_file_button = QtGui.QPushButton('Choose Graphic')
        self.graphic_list_view = QtGui.QListWidget()
        self.add_graphic_button = QtGui.QPushButton('Add Graphic')
        self.remove_graphic_button = QtGui.QPushButton('Remove Graphic')
        self.graphic_file_viewer = QtGui.QLabel()
        self.graphic_name_field = QtGui.QLineEdit()
        self.graphic_name_label = QtGui.QLabel('Graphic Name')

        # setup layout
        self.layout.addWidget(self.graphic_file_name_field,0,0)
        self.layout.addWidget(self.graphic_file_button,0,1)
        self.layout.addWidget(self.graphic_list_view,1,0)
        self.view_buttons_layout.addWidget(self.add_graphic_button)
        self.view_buttons_layout.addWidget(self.remove_graphic_button)
        self.layout.addLayout(self.view_buttons_layout,1,1)
        self.layout.addWidget(self.graphic_file_viewer,0,2)

        self.group.setLayout(self.layout)

        # wire up event handlers
        self.graphic_file_button.clicked.connect(self.open_file_dialog)
        self.add_graphic_button.clicked.connect(self.add_graphic)
        self.remove_graphic_button.clicked.connect(self.remove_graphic)
        self.graphic_list_view.currentItemChanged.connect(self.select_graphic)

    def open_file_dialog(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self.group, 'Choose Graphic', '/home')
        graphic_file = open(file_name, 'r') 
        self.graphic_file_name_field.setText(file_name)

    def add_graphic(self):
        # add the new graphic to the UI
        file_name = self.graphic_file_name_field.text()
        graphic_name = self.graphic_name_field.text()
        widget_text = graphic_name if graphic_name else file_name
        graphic_component = GraphicsComponent(self.context.get('selected_entity'),
                                              None,
                                              file_name)
        component = Component(graphic_component)
        widget_component = WidgetItemComponent(widget_text, 
                                               component)

        self.graphic_list_view.addItem(widget_component)
        # render it to the label image holder
        self.show_graphic(file_name)

        # then add it to the application context
        entity = self.context.get('selected_entity')
        if entity:
            self.context[entity]['components']['graphic'].append(widget_component)

    def show_graphic(self, file_name):
        self.current_graphic = QtGui.QPixmap(file_name)
        self.graphic_file_viewer.setPixmap(self.current_graphic)

    def remove_graphic(self):
        # remove the selectd graphic item from the UI
        selected_index = self.graphic_list_view.currentRow()
        selected_item = self.graphic_list_view.currentItem()
        self.graphic_list_view.takeItem(selected_index)

        # then remove it from the application context
        entity = self.context.get('selected_entity')
        if entity:
            self.context[entity]['components']['graphic'].remove(selected_item)

    def select_graphic(self):
        selected_item = self.graphic_list_view.currentItem()
        # this function gets called when a graphic is removed,
        # so we need to make sure there is actually a selected item
        if selected_item:
            file_name = selected_item.component.component.file_name
            self.show_graphic(file_name)
