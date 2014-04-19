from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.animation import AnimationComponent, FrameComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class FrameViewer(QtGui.QGraphicsView):
    def __init__(self):
        super(FrameViewer, self).__init__()
        self.setUpdatesEnabled(True)
        self.current_graphic = QtGui.QPixmap()
        self.frame_rect = QtCore.QRect(0, 0, 0, 0)
        self.graphic_item = None
        self.file_name = ''

        # frame properties
        self.setScene(QtGui.QGraphicsScene())

    def drawForeground(self, painter, rect):
        super(FrameViewer, self).drawForeground(painter, rect)
        painter.setPen(QtCore.Qt.red)
        painter.drawRect(self.frame_rect)
        if self.graphic_item:
            if self.frame_rect:
                painter.drawRect(self.frame_rect)

    def mousePressEvent(self, event):
        click_pos = event.pos()
        # translate the click position into scene coordinates
        click_pos = self.mapToScene(click_pos)
        self.dragging = True
        self.frame_rect.setX(click_pos.x())
        self.frame_rect.setY(click_pos.y())
        self.frame_rect.setWidth(0)
        self.frame_rect.setHeight(0)
        self.update()
        self.repaint()

        # fire event for updating frame crop
        new_event = Event('updated_frame_crop',
                          crop=self.frame_rect)
        EVENT_MANAGER.fire_event(new_event)

    def mouseReleaseEvent(self, event):
        release_pos = event.pos()
        # translate the release position into scene coordinates
        release_pos = self.mapToScene(release_pos)
        self.dragging = False
        self.frame_rect.setWidth(release_pos.x() - self.frame_rect.x())
        self.frame_rect.setHeight(release_pos.y() - self.frame_rect.y())
        self.awkward_update()

        # fire event for updating frame crop
        new_event = Event('updated_frame_crop',
                          crop=self.frame_rect)
        EVENT_MANAGER.fire_event(new_event)

    def mouseMoveEvent(self, event):
        drag_pos = event.pos()
        if self.dragging:
            # traslate the drag position into scene coordinates
            drag_pos = self.mapToScene(drag_pos)
            self.frame_rect.setWidth(drag_pos.x() - self.frame_rect.x())
            self.frame_rect.setHeight(drag_pos.y() - self.frame_rect.y())
            self.awkward_update()

            # fire event for updating frame crop
            new_event = Event('updated_frame_crop',
                              crop=self.frame_rect)
            EVENT_MANAGER.fire_event(new_event)

    def show_graphic(self, file_name):
        # first clear anything currently being rendered
        if self.graphic_item:
            self.scene().removeItem(self.graphic_item)

        # then create the new graphic from the given file name and render it
        self.current_graphic.load(file_name)
        self.graphic_item = QtGui.QGraphicsPixmapItem(self.current_graphic)
        self.scene().addItem(self.graphic_item)

    def set_graphic_file(self, file_name):
        self.file_name = file_name
        self.show_graphic(self.file_name)

    def awkward_update(self):
        '''
            Use this to force a repaint until it is determined how to
            get update() to cause a repaint
        '''
        self.scene().removeItem(self.graphic_item)
        self.scene().addItem(self.graphic_item)


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
        self.graphic_viewer = FrameViewer()
        self.frame_form_layout = QtGui.QGridLayout()
        self.frame_x_label = QtGui.QLabel('X')
        self.frame_x_field = QtGui.QLineEdit()
        self.frame_y_label = QtGui.QLabel('Y')
        self.frame_y_field = QtGui.QLineEdit()
        self.frame_width_label = QtGui.QLabel('Width')
        self.frame_width_field = QtGui.QLineEdit()
        self.frame_height_label = QtGui.QLabel('Height')
        self.frame_height_field = QtGui.QLineEdit()
        self.frame_repeat_label = QtGui.QLabel('Repeat')
        self.frame_repeat_field = QtGui.QLineEdit()

        # events
        EVENT_MAPPING.register_handler('selected_animation', self.set_animation)
        EVENT_MAPPING.register_handler('updated_frame_crop', self.update_fields)

        # setup layout
        self.outer_layout.addLayout(self.layout)
        self.outer_layout.addWidget(self.graphic_viewer)
        self.frame_form_layout.addWidget(self.frame_name_label,0,0)
        self.frame_form_layout.addWidget(self.frame_name_field,0,1)
        self.frame_form_layout.addWidget(self.frame_x_label,1,0)
        self.frame_form_layout.addWidget(self.frame_x_field,1,1)
        self.frame_form_layout.addWidget(self.frame_y_label,2,0)
        self.frame_form_layout.addWidget(self.frame_y_field,2,1)
        self.frame_form_layout.addWidget(self.frame_width_label,1,2)
        self.frame_form_layout.addWidget(self.frame_width_field,1,3)
        self.frame_form_layout.addWidget(self.frame_height_label,2,2)
        self.frame_form_layout.addWidget(self.frame_height_field,2,3)
        self.frame_form_layout.addWidget(self.frame_repeat_label,3,0)
        self.frame_form_layout.addWidget(self.frame_repeat_field,3,1)
        self.layout.addLayout(self.frame_form_layout,0,0)
        self.layout.addWidget(self.frame_list_view,1,0)
        self.frame_buttons_layout.addWidget(self.add_frame_button)
        self.frame_buttons_layout.addWidget(self.remove_frame_button)
        self.layout.addLayout(self.frame_buttons_layout,1,1)

        self.group.setLayout(self.outer_layout)

        # wire up gui event handlers
        self.add_frame_button.clicked.connect(self.add_frame)
        self.remove_frame_button.clicked.connect(self.remove_frame)
        self.frame_list_view.currentItemChanged.connect(self.select_frame)

    def add_frame(self):
        frame_name = self.frame_name_field.text()
        entity = self.context['selected_entity']
        ani = self.selected_animation
        crop = QtCore.QRect(int(self.frame_x_field.text()),
                     int(self.frame_y_field.text()),
                     int(self.frame_width_field.text()),
                     int(self.frame_height_field.text()))
        repeat = int(self.frame_repeat_field.text())
        frame_component = FrameComponent(entity_id=entity,
                                         crop=crop,
                                         repeat=repeat)
        frame_component_wrapper = Component(frame_component, frame_name)
        widget_component = WidgetItemComponent(frame_name, 
                                               frame_component_wrapper)
        self.frame_list_view.addItem(widget_component)

        # add new frame component to the selected animation's frame list
        ani.component.frames.append(frame_component_wrapper)

    def update_fields(self, event):
        crop = event.crop
        self.frame_x_field.setText(str(crop.x()))
        self.frame_y_field.setText(str(crop.y()))
        self.frame_width_field.setText(str(crop.width()))
        self.frame_height_field.setText(str(crop.height()))

    def remove_frame(self):
        entity = self.context['selected_entity']
        selected_index = self.frame_list_view.currentRow()
        selected_frame = self.frame_list_view.takeItem(selected_index)

        # remove the frame from its parent animation
        frame_component = selected_frame.component
        self.selected_animation.component.frames.remove(frame_component)

    def select_frame(self):
        selected_item = self.frame_list_view.currentItem()
        if selected_item:
            selected_component = selected_item.component
            graphic = self.selected_animation.component.graphic.component
            file_name = graphic.file_name
            self.show_graphic(file_name)

            # set field values
            crop = selected_component.component.crop
            self.frame_x_field.setText(str(crop.x()))
            self.frame_y_field.setText(str(crop.y()))
            self.frame_width_field.setText(str(crop.width()))
            self.frame_height_field.setText(str(crop.height()))
            self.frame_repeat_field.setText(str(selected_component.component.repeat))

            # fire event for selecting a frame
            new_event = Event('selected_frame',
                              frame_component=selected_component,
                              entity=selected_component.component.entity_id,
                              graphic_file_name=file_name)
            EVENT_MANAGER.fire_event(new_event)

    def show_graphic(self, file_name):
        self.graphic_viewer.set_graphic_file(file_name)

    def set_animation(self, event):
        entity = event.entity
        ani = event.animation_component
        self.selected_animation = ani
        frames = ani.component.frames

        self.show_graphic(ani.component.graphic.component.file_name)

        # do a soft clear of the animation list
        for i in range(self.frame_list_view.count()-1,-1,-1):
            self.frame_list_view.takeItem(i)

        for frame in frames:
            frame_wrapper = WidgetItemComponent(frame.text, frame)
            self.frame_list_view.addItem(frame_wrapper)
