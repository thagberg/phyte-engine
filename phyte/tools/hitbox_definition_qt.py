from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.animation import AnimationComponent, FrameComponent
from engine.common import BoxComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class HitboxViewer(QtGui.QGraphicsView):
    def __init__(self):
        super(HitboxViewer, self).__init__()
        self.setUpdatesEnabled(True)
        self.current_graphic = QtGui.QPixmap()
        self.frame_rect = QtCore.QRect(0, 0, 0, 0)
        self.graphic_item = None
        self.file_name = ''

        # frame properties
        self.setScene(QtGui.QGraphicsScene())

    def drawForeground(self, painter, rect):
        super(HitboxViewer, self).drawForeground(painter, rect)
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

        # fire event for updating box 
        new_event = Event('updated_box',
                          box=self.frame_rect)
        EVENT_MANAGER.fire_event(new_event)

    def mouseReleaseEvent(self, event):
        release_pos = event.pos()
        # translate the release position into scene coordinates
        release_pos = self.mapToScene(release_pos)
        self.dragging = False
        self.frame_rect.setWidth(release_pos.x() - self.frame_rect.x())
        self.frame_rect.setHeight(release_pos.y() - self.frame_rect.y())
        self.update()
        self.repaint()

        # fire event for updating box
        new_event = Event('updated_box',
                          box=self.frame_rect)
        EVENT_MANAGER.fire_event(new_event)

    def mouseMoveEvent(self, event):
        drag_pos = event.pos()
        if self.dragging:
            # traslate the drag position into scene coordinates
            drag_pos = self.mapToScene(drag_pos)
            self.frame_rect.setWidth(drag_pos.x() - self.frame_rect.x())
            self.frame_rect.setHeight(drag_pos.y() - self.frame_rect.y())
            self.update()
            self.repaint()

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


class HitboxDefinitionEditor(Editor):
    def __init__(self, context):
        super(HitboxDefinitionEditor, self).__init__(context,
                                                     QtGui.QGroupBox('Hitbox'))
        self.outer_layout = QtGui.QHBoxLayout()
        self.layout = QtGui.QGridLayout()
        self.box_name_label = QtGui.QLabel('Hitbox Name')
        self.box_name_field = QtGui.QLineEdit()
        self.box_hitactive_label = QtGui.QLabel('Hit Active')
        self.box_hitactive_check = QtGui.QCheckBox()
        self.box_hurtactive_label = QtGui.QLabel('Hurt Active')
        self.box_hurtactive_check = QtGui.QCheckBox()
        self.box_blockactive_label = QtGui.QLabel('Block Active')
        self.box_blockactive_check = QtGui.QCheckBox()
        self.box_solid_label = QtGui.QLabel('Solid')
        self.box_solid_check = QtGui.QCheckBox()
        self.box_x_label = QtGui.QLabel('X')
        self.box_x_field = QtGui.QLineEdit()
        self.box_y_label = QtGui.QLabel('Y')
        self.box_y_field = QtGui.QLineEdit()
        self.box_width_label = QtGui.QLabel('Width')
        self.box_width_field = QtGui.QLineEdit()
        self.box_height_label = QtGui.QLabel('Height')
        self.box_height_field = QtGui.QLineEdit()
        self.box_layout = QtGui.QGridLayout()
        self.box_list_view = QtGui.QListWidget()
        self.add_box_button = QtGui.QPushButton('Add Hitbox')
        self.remove_box_button = QtGui.QPushButton('Remove Hitbox')
        self.box_buttons_layout = QtGui.QVBoxLayout()
        self.graphic_viewer = HitboxViewer()

        # internal events
        EVENT_MAPPING.register_handler('selected_frame', self.set_frame)

        #set up layout
        self.outer_layout.addLayout(self.layout)
        self.layout.addWidget(self.box_name_label,0,0)
        self.layout.addWidget(self.box_name_field,0,1)
        self.box_layout.addWidget(self.box_hitactive_label,0,0)
        self.box_layout.addWidget(self.box_hitactive_check,0,1)
        self.box_layout.addWidget(self.box_hurtactive_label,0,2)
        self.box_layout.addWidget(self.box_hurtactive_check,0,3)
        self.box_layout.addWidget(self.box_blockactive_label,1,0)
        self.box_layout.addWidget(self.box_blockactive_check,1,1)
        self.box_layout.addWidget(self.box_solid_label,1,2)
        self.box_layout.addWidget(self.box_solid_check,1,3)
        self.box_layout.addWidget(self.box_x_label,2,0)
        self.box_layout.addWidget(self.box_x_field,2,1)
        self.box_layout.addWidget(self.box_width_label,2,2)
        self.box_layout.addWidget(self.box_width_field,2,3)
        self.box_layout.addWidget(self.box_y_label,3,0)
        self.box_layout.addWidget(self.box_y_field,3,1)
        self.box_layout.addWidget(self.box_height_label,3,2)
        self.box_layout.addWidget(self.box_height_field,3,3)
        self.layout.addLayout(self.box_layout,1,0)
        self.layout.addWidget(self.box_list_view,2,0)
        self.box_buttons_layout.addWidget(self.add_box_button)
        self.box_buttons_layout.addWidget(self.remove_box_button)
        self.layout.addLayout(self.box_buttons_layout,2,1)
        self.outer_layout.addWidget(self.graphic_viewer)

        self.group.setLayout(self.outer_layout)

        # wire up gui event handlers
        self.add_box_button.clicked.connect(self.add_box)
        self.remove_box_button.clicked.connect(self.remove_box)
        self.box_list_view.currentItemChanged.connect(self.select_box)

    def add_box(self):
        box_name = self.box_name_field.text()
        entity = self.context['selected_entity']
        pass

    def remove_box(self):
        pass

    def select_box(self):
        pass

    def set_frame(self, event):
        entity = event.entity
        frame = event.frame_component
        file_name = event.graphic_file_name
        self.selected_frame = frame
        boxes = frame.component.hitboxes

        self.show_graphic(file_name)

        # do a soft clear of the box list
        for i in range(self.box_list_view.count()-1,-1,-1):
            self.box_list_view.takeItem(i)

        # repopulate box list
        for box in boxes:
            box_wrapper = WidgetItemComponent(box.text, box)
            self.box_list-view.addItem(box)

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

    def show_graphic(self, file_name):
        self.graphic_viewer.set_graphic_file(file_name)
