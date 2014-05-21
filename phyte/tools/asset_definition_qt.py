from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.graphics2d import GraphicsComponent
from engine.common import AssetComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class AssetDefinitionEditor(Editor):
    def __init__(self, context):
        super(AssetDefinitionEditor, self).__init__(context, QtGui.QGroupBox('Assets'))
        # setup gui stuff
        self.outer_layout = QtGui.QHBoxLayout()
        self.layout =  QtGui.QGridLayout()
        self.view_buttons_layout = QtGui.QVBoxLayout()
        self.asset_file_name_field = QtGui.QLineEdit()
        self.asset_file_button = QtGui.QPushButton('Choose Asset')
        self.add_asset_button = QtGui.QPushButton('Add Asset')
        self.remove_asset_button = QtGui.QPushButton('Remove Asset')
        self.asset_file_viewer = QtGui.QLabel()
        self.asset_name_field = QtGui.QLineEdit()
        self.asset_name_label = QtGui.QLabel('Asset Name')
        self.asset_list_view = QtGui.QListWidget()
        self.view_area = QtGui.QScrollArea()

        # setup layout
        self.outer_layout.addLayout(self.layout)
        self.outer_layout.addWidget(self.view_area)
        self.layout.addWidget(self.asset_file_name_field,0,0)
        self.layout.addWidget(self.asset_file_button,0,1)
        self.layout.addWidget(self.asset_list_view,1,0)
        self.view_buttons_layout.addWidget(self.add_asset_button)
        self.view_buttons_layout.addWidget(self.remove_asset_button)
        self.layout.addLayout(self.view_buttons_layout,1,1)
        # setup view area layout
        self.view_area.setWidgetResizable(True)
        self.view_area.setWidget(self.asset_file_viewer)

        self.group.setLayout(self.outer_layout)

        # wire up gui event handlers
        self.asset_file_button.clicked.connect(self.open_file_dialog)
        self.add_asset_button.clicked.connect(self.add_asset)
        self.remove_asset_button.clicked.connect(self.remove_asset)
        self.asset_list_view.currentItemChanged.connect(self.select_asset)

    def open_file_dialog(self):
        file_name = str(QtGui.QFileDialog.getOpenFileName(self.group, 'Choose Asset', '/home'))
        asset_file = open(file_name, 'r') 
        self.asset_file_name_field.setText(file_name)

    def add_asset(self):
        # add the new graphic to the UI
        file_name = str(self.asset_file_name_field.text())
        asset_name = str(self.asset_name_field.text())
        asset_name = asset_name if asset_name else file_name
        asset_component = AssetComponent(file_name, None)
        asset_component_wrapper = Component(asset_component, asset_name)
        widget_component = WidgetItemComponent(asset_name, asset_component_wrapper)
        self.asset_list_view.addItem(widget_component)

        # render it to the label image holder
        self.show_asset(file_name)

        # then add it to the application context
        if 'assets' not in self.context:
            self.context['assets'] = list()
        self.context['assets'].append(asset_component_wrapper)

        # fire off an event
        new_event = Event('asset_added',
                          asset_component=asset_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def show_asset(self, file_name):
        self.current_asset = QtGui.QPixmap(file_name)
        self.asset_file_viewer.setPixmap(self.current_asset)

    def remove_asset(self):
        # remove the selectd graphic item from the UI
        selected_index = self.asset_list_view.currentRow()
        selected_item = self.asset_list_view.currentItem()
        self.asset_list_view.takeItem(selected_index)

        # then remove it from the application context
        self.context['assets'].remove(selected_item.component)

        # fire off an event
        new_event = Event('asset_removed',
                          asset_component=selected_item.component)
        EVENT_MANAGER.fire_event(new_event)

    def select_asset(self):
        selected_item = self.asset_list_view.currentItem()
        # this function gets called when a graphic is removed,
        # so we need to make sure there is actually a selected item
        if selected_item:
            file_name = selected_item.component.component.file_name
            self.show_asset(file_name)

    def update(self):
        self.asset_list_view.clear()
        for asset in self.context['assets']:
            widget_component = WidgetItemComponent(asset.text, asset)
            self.asset_list_view.addItem(widget_component)
