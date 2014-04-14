from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.animation import AnimationComponent, FrameComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class FrameDefinitionEditor(Editor):
    def __init__(self, context):
        super(FrameDefinitionEditor, self).__init__(context,
                                                        QtGui.QGroupBox('Animation'))
        self.outer_layout = QtGui.QHBoxLayout()
        self.layout = QtGui.QGridLayout()
        self.frame_name_field = QtGui.QLineEdit()
        self.frame_name_label = QtGui.QLabel('Frame Name')
        self.frame_list_view = QtGui.QListWidget()
        self.add_frame_button = QtGui.QPushButton('Add Frame')
        self.remove_frame_button = QtGui.QPushButton('Remove Frame')
        self.frame_buttons_layout = QtGui.QVBoxLayout()
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
        EVENT_MAPPING.register_handler('selected_animation', self.set_animation)

        # setup layout
        self.outer_layout.addLayout(self.layout)
        self.outer_layout.addWidget(self.graphic_viewer)
        self.layout.addWidget(self.frame_name_label,0,0)
        self.layout.addWidget(self.frame_name_field,0,1)
        self.layout.addWidget(self.frame_list_view,1,0)
        self.frame_buttons_layout.addWidget(self.add_frame_button)
        self.frame_buttons_layout.addWidget(self.remove_frame_button)
        self.layout.addLayout(self.frame_buttons_layout,1,1)

        self.group.setLayout(self.outer_layout)

        # wire up gui event handlers
        self.add_frame_button.clicked.connect(self.add_frame)
        self.remove_frame_button.clicked.connect(self.remove_frame)
        self.frame_list_view.currentItemChanged.connect(self.select_frame)

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

    def add_frame(self):
        frame_name = self.frame_name_field.text()
        entity = self.context['selected_entity']
        ani = self.selected_animation
        frame_name = '{ani_name} - {index}'.format(ani_name=ani.text,
                                                   index=len(ani.component.frames))
        frame_component = FrameComponent(entity_id=entity)
        frame_component_wrapper = Component(frame_component, frame_name)
        widget_component = WidgetItemComponent(frame_name, 
                                               frame_component_wrapper)
        self.frame_list_view.addItem(widget_component)

        # add new frame component to the selected animation's frame list
        ani.component.frames.append(frame_component_wrapper)

    def remove_frame(self):
        entity = self.context['selected_entity']
        selected_index = self.frame_list_view.currentRow()
        selected_frame = self.frame_list_view.takeItem(selected_index)
        self.frame_list_view.takeItem(selected_index)

        # remove the animation from its parent animation
        frame_component = selected_frame.component
        self.selected_animation.component.remove(frame_component)

    def select_frame(self):
        selected_item = self.frame_list_view.currentItem()
        if selected_item:
            selected_component = selected_item.component
            graphic = self.selected_animation.component.graphic.component
            file_name = graphic.file_name
            self.show_graphic(file_name)

            # fire event for selecting a graphic
            new_event = Event('selected_frame',
                              frame_component=selected_component,
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

    def set_animation(self, event):
        entity = event.entity
        ani = event.animation_component
        self.selected_animation = ani
        frames = ani.component.frames

        # do a soft clear of the animation list
        for i in range(self.frame_list_view.count()-1,-1,-1):
            self.frame_list_view.takeItem(i)

        for frame in frames:
            frame_wrapper = WidgetItemComponent(frame.text, frame)
            self.frame_list_view.addItem(frame_wrapper)
