from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.animation import AnimationComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class AnimationDefinitionEditor(Editor):
    def __init__(self, context):
        super(AnimationDefinitionEditor, self).__init__(context,
                                                        QtGui.QGroupBox('Animation'))
        self.outer_layout = QtGui.QHBoxLayout()
        self.layout = QtGui.QGridLayout()
        self.animation_name_field = QtGui.QLineEdit()
        self.animation_name_label = QtGui.QLabel('Animation Name')
        self.animation_list_view = QtGui.QListWidget()
        self.add_animation_button = QtGui.QPushButton('Add Animation')
        self.remove_animation_button = QtGui.QPushButton('Remove Animation')
        self.animation_buttons_layout = QtGui.QVBoxLayout()
        self.graphic_viewer = QtGui.QGraphicsView()
        self.current_graphic = None
        self.graphic_item = None

        # frame properties
        self.graphic_viewer.setScene(QtGui.QGraphicsScene())
        self.frame_rect = QtCore.QRect()
        self.dragging = False

        # events
        EVENT_MAPPING.register_handler('selected_graphic', self.set_animations)

        # setup layout
        self.outer_layout.addLayout(self.layout)
        self.outer_layout.addWidget(self.graphic_viewer)
        self.layout.addWidget(self.animation_name_label,0,0)
        self.layout.addWidget(self.animation_name_field,0,1)
        self.layout.addWidget(self.animation_list_view,1,0)
        self.animation_buttons_layout.addWidget(self.add_animation_button)
        self.animation_buttons_layout.addWidget(self.remove_animation_button)
        self.layout.addLayout(self.animation_buttons_layout,1,1)

        self.group.setLayout(self.outer_layout)

        # wire up gui event handlers
        self.add_animation_button.clicked.connect(self.add_animation)
        self.remove_animation_button.clicked.connect(self.remove_animation)
        self.animation_list_view.currentItemChanged.connect(self.select_animation)

    def add_animation(self):
        animation_name = self.animation_name_field.text()
        entity = self.context['selected_entity']
        animation_component = AnimationComponent(entity_id=entity,
                                                 graphic=self.selected_graphic)
        animation_component_wrapper = Component(animation_component, 
                                                animation_name)
        widget_component = WidgetItemComponent(animation_name, 
                                               animation_component_wrapper)
        self.animation_list_view.addItem(widget_component)

        # add new component to the application context
        context_animations = self.context['entities'][entity]['components']['animation']
        context_animations.append(animation_component_wrapper)

        # fire event for adding an animation
        new_event = Event('added_animation',
                          animation_component=animation_component_wrapper,
                          entity=animation_component_wrapper.component.entity_id)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('added_component',
                          entity=entity,
                          component_type='animation',
                          component=animation_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_animation(self):
        entity = self.context['selected_entity']
        selected_index = self.animation_list_view.currentRow()
        selected_animation = self.animation_list_view.takeItem(selected_index)
        self.animation_list_view.takeItem(selected_index)

        # remove the animation from the application context
        inner_ani_component = selected_animation.component
        self.context['entities'][entity]['components']['animation'].remove(inner_ani_component)

        # fire event for removing an animation
        new_event = Event('removed_animation',
                          animation_component=inner_ani_component,
                          entity=inner_ani_component.component.entity_id)
        EVENT_MANAGER.fire_event(new_event)
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='animation',
                          component=animation_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def select_animation(self):
        selected_item = self.animation_list_view.currentItem()
        # this function gets called when an animation is removed,
        # so we need to make sure there is actually a selected item
        if selected_item:
            selected_component = selected_item.component
            file_name = selected_component.component.graphic.component.file_name
            self.show_graphic(file_name)

            # fire event for selecting an animation
            new_event = Event('selected_animation',
                              animation_component=selected_component,
                              entity=selected_component.component.entity_id)
            EVENT_MANAGER.fire_event(new_event)

    def show_graphic(self, file_name):
        # first clear anything currently being rendered
        if self.graphic_item:
            self.graphic_viewer.scene().removeItem(self.graphic_item)

        # then create the new graphic from the given file name and render it
        self.current_graphic = QtGui.QPixmap(file_name)
        self.graphic_item = QtGui.QGraphicsPixmapItem(self.current_graphic)
        self.graphic_viewer.scene().addItem(self.graphic_item)

    def set_animations(self, event):
        entity = event.entity
        graphic = event.graphic_component
        self.selected_graphic = graphic
        animations = self.context['entities'][entity]['components']['animation']
        animations = [x for x in animations if x.component.graphic.component == graphic.component]

        # do a soft clear of the animation list
        for i in range(self.animation_list_view.count()-1,-1,-1):
            self.animation_list_view.takeItem(i)

        for animation in animations:
            animation_wrapper = WidgetItemComponent(animation.text, animation)
            self.animation_list_view.addItem(animation_wrapper)

    def update(self):
        entity = self.context['selected_entity']
        self.animation_list_view.clear()
        if entity and entity != '':
            for animation in self.context[entity]['components']['animation']:
                widget_component = WidgetItemComponent(animation.text, animation)
                self.animation_list_view.addItem(widget_component)
