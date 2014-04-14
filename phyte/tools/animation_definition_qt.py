from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.animation import AnimationComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


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
        self.graphic_viewer = QtGui.QGraphicsView()
        self.frame_painter = QtGui.QPainter()
        self.current_graphic = None
        self.graphic_item = None

        # frame properties
        self.graphic_viewer.setScene(QtGui.QGraphicsScene())
        self.frame_rect = QtCore.QRect()
        self.dragging = False

        # special graphic_viewer settings
        self.graphic_viewer.mousePressEvent = self.image_click
        self.graphic_viewer.mouseReleaseEvent = self.image_release
        self.graphic_viewer.mouseMoveEvent = self.image_drag
        self.frame_painter.begin(self.graphic_viewer)
        self.frame_painter.setPen(QtCore.Qt.red)

        # events
        EVENT_MAPPING.register_handler('selected_graphic', self.set_animations)

        # setup layout
        self.layout.addWidget(self.animation_name_label,0,0)
        self.layout.addWidget(self.animation_name_field,0,1)
        self.layout.addWidget(self.animation_list_view,1,0)
        self.animation_buttons_layout.addWidget(self.add_animation_button)
        self.animation_buttons_layout.addWidget(self.remove_animation_button)
        self.layout.addLayout(self.animation_buttons_layout,1,1)
        self.layout.addWidget(self.graphic_viewer,0,2)

        self.group.setLayout(self.layout)

        # wire up gui event handlers
        self.add_animation_button.clicked.connect(self.add_animation)
        self.remove_animation_button.clicked.connect(self.remove_animation)
        self.animation_list_view.currentItemChanged.connect(self.select_animation)

    def image_click(self, event):
        click_pos = event.pos()
        self.dragging = True
        self.frame_rect.setX(click_pos.x())
        self.frame_rect.setY(click_pos.y())
        self.frame_rect.setWidth(0)
        self.frame_rect.setHeight(0)
        self.draw_rect(self.frame_rect)

    def image_release(self, event):
        release_pos = event.pos()
        self.frame_rect.setWidth(release_pos.x() - self.frame_rect.x())
        self.frame_rect.setHeight(release_pos.y() - self.frame_rect.y())
        self.draw_rect(self.frame_rect)

    def image_drag(self, event):
        drag_pos = event.pos()
        self.frame_rect.setWidth(drag_pos.x() - self.frame_rect.x())
        self.frame_rect.setHeight(drag_pos.y() - self.frame_rect.y())
        self.draw_rect(self.frame_rect)

    def draw_rect(self, rect):
        self.frame_painter.drawRect(rect)

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
        context_animations = self.context[entity]['components']['animation']
        context_animations.append(animation_component_wrapper)

    def remove_animation(self):
        entity = self.context['selected_entity']
        selected_index = self.animation_list_view.currentRow()
        selected_animation = self.animation_list_view.takeItem(selected_index)
        self.animation_list_view.takeItem(selected_index)

        # remove the animation from the application context
        inner_ani_component = selected_animation.component
        self.context[entity]['components']['animation'].remove(inner_ani_component)

    def select_animation(self):
        selected_animation = self.animation_list_view.currentItem()
        # this function gets called when an animation is removed,
        # so we need to make sure there is actually a selected item
        if selected_animation:
            file_name = selected_animation.component.component.graphic.component.file_name
            self.show_graphic(file_name)

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
        animations = self.context[entity]['components']['animation']
        animations = [x for x in animations if x.component.graphic.component == graphic.component]

        # do a soft clear of the animation list
        for i in range(self.animation_list_view.count()-1,-1,-1):
            self.animation_list_view.takeItem(i)

        for animation in animations:
            animation_wrapper = WidgetItemComponent(animation.text, animation)
            self.animation_list_view.addItem(animation_wrapper)
