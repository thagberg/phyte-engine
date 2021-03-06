from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, TreeWidgetItemComponent
from engine.graphics2d import GraphicsComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class GraphicDefinitionEditor(Editor):
    def __init__(self, context):
        super(GraphicDefinitionEditor, self).__init__(context, QtGui.QGroupBox('Graphics'))
        # setup gui stuff
        self.layout = QtGui.QGridLayout()
        self.view_buttons_layout = QtGui.QVBoxLayout()
        self.add_graphic_button = QtGui.QPushButton('Add Graphic')
        self.remove_graphic_button = QtGui.QPushButton('Remove Graphic')
        self.update_graphic_button = QtGui.QPushButton('Update Graphic')
        self.graphic_name_field = QtGui.QLineEdit()
        self.graphic_name_label = QtGui.QLabel('Graphic Name')
        self.graphic_file_viewer = QtGui.QLabel()
        self.graphic_list_view = QtGui.QListWidget()
        self.graphic_buttons_layout = QtGui.QVBoxLayout()
        self.asset_list_view = QtGui.QListWidget()
        self.asset_list_label = QtGui.QLabel('Choose Asset')
        self.asset_list_layout = QtGui.QVBoxLayout()
        self.anchor_label = QtGui.QLabel('Choose Anchor Body')
        self.anchor_list_view = QtGui.QListWidget()
        self.anchor_layout = QtGui.QVBoxLayout()

        # setup layout
        self.asset_list_layout.addWidget(self.asset_list_label)
        self.asset_list_layout.addWidget(self.asset_list_view)
        self.layout.addLayout(self.asset_list_layout,0,0)
        self.layout.addWidget(self.graphic_name_label,0,1)
        self.layout.addWidget(self.graphic_name_field,0,2)
        self.anchor_layout.addWidget(self.anchor_label)
        self.anchor_layout.addWidget(self.anchor_list_view)
        self.layout.addLayout(self.anchor_layout,1,0)
        self.layout.addWidget(self.graphic_list_view,2,0)
        self.graphic_buttons_layout.addWidget(self.add_graphic_button)
        self.graphic_buttons_layout.addWidget(self.update_graphic_button)
        self.graphic_buttons_layout.addWidget(self.remove_graphic_button)
        self.layout.addLayout(self.graphic_buttons_layout,2,1)

        self.group.setLayout(self.layout)

        # wire up event handlers
        self.add_graphic_button.clicked.connect(self.add_graphic)
        self.update_graphic_button.clicked.connect(self.update_graphic)
        self.remove_graphic_button.clicked.connect(self.remove_graphic)
        self.graphic_list_view.currentItemChanged.connect(self.select_graphic)

        # events
        EVENT_MAPPING.register_handler('selected_entity', self.set_graphics)
        EVENT_MAPPING.register_handler('asset_added', self.add_asset)
        EVENT_MAPPING.register_handler('asset_removed', self.remove_asset)
        EVENT_MAPPING.register_handler('added_component', self.add_component)
        EVENT_MAPPING.register_handler('removed_component', self.remove_component)

    def add_graphic(self):
        # add the new graphic to the UI
        selected_asset = self.asset_list_view.currentItem()
        selected_component = selected_asset.component
        file_name = selected_component.component.file_name
        graphic_name = str(self.graphic_name_field.text())
        selected_anchor = self.anchor_list_view.currentItem().component
        graphic_component = GraphicsComponent(entity_id=self.context.get('selected_entity'),
                                              surface=selected_component.component.surface,
                                              file_name=file_name,
                                              dest=selected_anchor)
        graphic_component_wrapper = Component(graphic_component, graphic_name)
        widget_component = WidgetItemComponent(graphic_name, graphic_component_wrapper)
        self.graphic_list_view.addItem(widget_component)

        # render it to the label image holder
        self.show_graphic(file_name)

        # then add it to the application context
        entity_name = self.context.get('selected_entity')
        if entity_name:
            self.context['entities'][entity_name]['components']['graphic'].append(graphic_component_wrapper)

        # fire off an event
        new_event = Event('graphic_added',
                          graphic_component=graphic_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('added_component',
                          entity=entity_name,
                          component_type='graphic',
                          component=graphic_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)


    def show_graphic(self, file_name):
        self.current_graphic = QtGui.QPixmap(file_name)
        self.graphic_file_viewer.setPixmap(self.current_graphic)

    def update_graphic(self):
        selected_index = self.graphic_list_view.currentRow()
        selected_item = self.graphic_list_view.currentItem()
        selected_component = selected_item.component

        selected_component.text = str(self.graphic_name_field.text())
        selected_item.setText(selected_component.text)
        selected_component.component.dest = self.anchor_list_view.currentItem().component

    def remove_graphic(self):
        # remove the selectd graphic item from the UI
        selected_index = self.graphic_list_view.currentRow()
        selected_item = self.graphic_list_view.currentItem()
        self.graphic_list_view.takeItem(selected_index)

        # then remove it from the application context
        entity = self.context.get('selected_entity')
        if entity:
            self.context['entities'][entity]['components']['graphic'].remove(selected_item.component)

        # fire off an event
        new_event = Event('graphic_removed',
                          graphic_component=graphic_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='graphic',
                          component=graphic_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def select_graphic(self):
        selected_item = self.graphic_list_view.currentItem()
        if not selected_item: return
        selected_component = selected_item.component
        name = selected_component.text
        anchor = selected_component.component.dest
        # set the name field
        self.graphic_name_field.setText(name)
        # this function gets called when a graphic is removed,
        # so we need to make sure there is actually a selected item
        if selected_item:
            file_name = selected_component.component.file_name
            self.show_graphic(file_name)

        # fire event for selecting a graphic
        new_event = Event('selected_graphic',
                          graphic_component=selected_component,
                          entity=selected_component.component.entity_id)
        EVENT_MANAGER.fire_event(new_event)

        anchor = selected_component.component.dest
        # select the proper anchor
        for i in xrange(self.anchor_list_view.count()):
            item = self.anchor_list_view.item(i)
            component = item.component
            if component == anchor:
                self.anchor_list_view.setCurrentRow(i)
                break

    def set_graphics(self, event):
        entity = event.entity
        available_graphics = self.context['entities'][entity]['components']['graphic']
        # do a "soft" clear of the list
        # if we actually call self.graphic_list_view.clear(),
        # the C++ Qt objects will be deleted
        for i in range(self.graphic_list_view.count()-1,-1,-1):
            self.graphic_list_view.takeItem(i)

        for graphic in available_graphics:
            widget_component = WidgetItemComponent(graphic.text, graphic)
            self.graphic_list_view.addItem(widget_component)

        # clear and populate anchor list
        self.anchor_list_view.clear()        
        available_anchors = self.context['entities'][entity]['components']['body']
        for anchor in available_anchors:
            widget_component = WidgetItemComponent(anchor.text, anchor)
            self.anchor_list_view.addItem(widget_component)

    def add_asset(self, event):
        asset_component = event.asset_component
        widget_component = WidgetItemComponent(asset_component.text,
                                               asset_component)
        self.asset_list_view.addItem(widget_component)

    def remove_asset(self, event):
        asset_component = event.asset_component
        count = self.asset_list_view.count()
        for i in xrange(count-1, -1, -1):
            current_asset = self.asset_list_view.item(i)
            if current_asset.component == asset_component:
                self.asset_list_view.takeItem(i)

    def add_vector(self, event):
        vector_component = event.vector_component
        widget_component = WidgetItemComponent(vector_component.text,
                                               vector_component)
        self.vector_list_view.addItem(widget_component)

    def remove_vector(self, event):
        vector_component = event.vector_component
        count = self.vector_list_view.count()
        for i in xrange(count-1,-1,-1):
            current_vector = self.vector_list_view.item(i)
            if current_vector.component == vector_component:
                self.vector_list_view.takeItem(i)

    def update(self):
        entity = self.context['selected_entity']
        self.graphic_list_view.clear()
        self.asset_list_view.clear()
        for asset in self.context['assets']:
            widget_component = WidgetItemComponent(asset.text, asset)
            self.asset_list_view.addItem(widget_component)
        if entity and entity != '':
            for graphic in self.context['entities'][entity]['components']['graphic']:
                widget_component = WidgetItemComponent(graphic.text, graphic)
                self.graphic_list_view.addItem(widget_component)
    
    def add_component(self, event):
        entity = event.entity
        component_type = event.component_type
        component = event.component
        if component_type == 'body':
            widget_item = WidgetItemComponent(component.text, component)
            self.anchor_list_view.addItem(widget_item)

    def remove_component(self, event):
        entity = event.entity
        component_type = event.component_type
        component = event.component
        if component_type == 'body':
            for i in xrange(self.anchor_list_view.count()):
                item = self.anchor_list_view.item(i)
                anchor = item.component
                if anchor == component:
                    self.anchor_list_view.removeItemWidget(item)
                    break
