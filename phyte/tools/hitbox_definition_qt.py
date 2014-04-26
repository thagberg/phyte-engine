from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent
from engine.common import BoxComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER


class HitboxViewer(QtGui.QGraphicsView):
    def __init__(self, check_context):
        super(HitboxViewer, self).__init__()
        self.check_context = check_context
        self.setUpdatesEnabled(True)
        self.current_graphic = QtGui.QPixmap()
        self.box_rect = QtCore.QRect(0, 0, 0, 0)
        self.graphic_item = None
        self.file_name = ''

        # frame properties
        self.setScene(QtGui.QGraphicsScene())

    def drawForeground(self, painter, rect):
        super(HitboxViewer, self).drawForeground(painter, rect)
        painter.setPen(self.resolve_color())
        if self.graphic_item:
            if self.box_rect:
                painter.drawRect(self.box_rect)

    def resolve_color(self):
        '''
            Determine pen color based on the various hitbox states
        '''
        color = None
        if self.check_context['hitactive']:
            if self.check_context['hurtactive']:
                color = QtCore.Qt.magenta
            else:
                color = QtCore.Qt.red
        elif self.check_context['hurtactive']:
            color = QtCore.Qt.blue
        elif self.check_context['blockactive']:
            if self.check_context['solid']:
                color = QtCore.Qt.cyan
            else:
                color = QtCore.Qt.green
        elif self.check_context['solid']:
            color = QtCore.Qt.yellow
        else:
            color = QtCore.Qt.gray

        return color

    def mousePressEvent(self, event):
        click_pos = event.pos()
        # translate the click position into scene coordinates
        click_pos = self.mapToScene(click_pos)
        self.dragging = True
        self.box_rect.setX(click_pos.x())
        self.box_rect.setY(click_pos.y())
        self.box_rect.setWidth(0)
        self.box_rect.setHeight(0)
        self.awkward_update()

        # fire event for updating box 
        new_event = Event('updated_box',
                          box=self.box_rect)
        EVENT_MANAGER.fire_event(new_event)

    def mouseReleaseEvent(self, event):
        release_pos = event.pos()
        # translate the release position into scene coordinates
        release_pos = self.mapToScene(release_pos)
        self.dragging = False
        self.box_rect.setWidth(release_pos.x() - self.box_rect.x())
        self.box_rect.setHeight(release_pos.y() - self.box_rect.y())
        self.awkward_update()

        # fire event for updating box
        new_event = Event('updated_box',
                          box=self.box_rect)
        EVENT_MANAGER.fire_event(new_event)

    def mouseMoveEvent(self, event):
        drag_pos = event.pos()
        if self.dragging:
            # traslate the drag position into scene coordinates
            drag_pos = self.mapToScene(drag_pos)
            self.box_rect.setWidth(drag_pos.x() - self.box_rect.x())
            self.box_rect.setHeight(drag_pos.y() - self.box_rect.y())
            self.awkward_update()

            # fire event for updating frame box
            new_event = Event('updated_box',
                              box=self.box_rect)
            EVENT_MANAGER.fire_event(new_event)

    def show_graphic(self, file_name, crop):
        # first clear anything currently being rendered
        if self.graphic_item:
            self.scene().removeItem(self.graphic_item)

        # then create the new graphic from the given file name and render it
        self.current_graphic.load(file_name)
        # if a crop rectangle is provided, crop the image to that
        if crop:
            self.current_graphic = self.current_graphic.copy(crop)
        self.graphic_item = QtGui.QGraphicsPixmapItem(self.current_graphic)
        self.scene().addItem(self.graphic_item)

    def set_box(self, x, y, w, h):
        self.box_rect.setX(x)
        self.box_rect.setY(y)
        self.box_rect.setWidth(w)
        self.box_rect.setHeight(h)
        self.awkward_update()

    def awkward_update(self):
        '''
            Use this to force a repaint until it is determined how to
            get update() to cause a repaint
        '''
        self.scene().removeItem(self.graphic_item)
        self.scene().addItem(self.graphic_item)


class HitboxDefinitionEditor(Editor):
    def __init__(self, context):
        super(HitboxDefinitionEditor, self).__init__(context,
                                                     QtGui.QGroupBox('Hitbox'))
        self.selected_frame = None
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

        # used to encapsulate the state of checkboxes
        # this simplifies notifying the graphic_viewer of how to
        # color the hitbox
        self.check_context = {
            'hitactive': self.box_hitactive_check.checkState(),
            'hurtactive': self.box_hurtactive_check.checkState(),
            'blockactive': self.box_blockactive_check.checkState(),
            'solid': self.box_solid_check.checkState()
        }
        self.graphic_viewer = HitboxViewer(self.check_context)

        # internal events
        EVENT_MAPPING.register_handler('selected_frame', self.set_frame)
        EVENT_MAPPING.register_handler('updated_box', self.update_fields)

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
        self.box_hitactive_check.stateChanged.connect(self.set_hitactive)
        self.box_hurtactive_check.stateChanged.connect(self.set_hurtactive)
        self.box_blockactive_check.stateChanged.connect(self.set_blockactive)
        self.box_solid_check.stateChanged.connect(self.set_solid)

    def add_box(self):
        box_name = self.box_name_field.text()
        entity = self.context['selected_entity']
        frame = self.selected_frame.component
        rect = QtCore.QRect(int(self.box_x_field.text()),
                            int(self.box_y_field.text()),
                            int(self.box_width_field.text()),
                            int(self.box_height_field.text()))
        hitactive = self.check_context['hitactive'] > 0
        hurtactive = self.check_context['hurtactive'] > 0
        blockactive = self.check_context['blockactive'] > 0
        solid = self.check_context['solid'] > 0
        box_component = BoxComponent(entity_id=entity,
                                     rect=rect,
                                     hitactive=hitactive,
                                     hurtactive=hurtactive,
                                     blockactive=blockactive,
                                     solid=solid)
        box_component_wrapper = Component(box_component, box_name)
        widget_component = WidgetItemComponent(box_name,
                                               box_component_wrapper)
        self.box_list_view.addItem(widget_component)

        # add box to the selected frame's box list
        frame.hitboxes.append(box_component_wrapper)

        # fire event
        new_event = Event('added_component',
                          entity=entity,
                          component_type='hitbox',
                          component=box_component_wrapper)
        EVENT_MANAGER.fire_event(new_event)

    def remove_box(self):
        entity = self.context['selected_entity']
        selected_index = self.box_list_view.currentRow()
        selected_box = self.box_list_view.takeItem(selected_index)

        # remove the box from its parent frame
        self.selected_frame.component.hitboxes.remove(selected_box.component)

        # fire event
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='hitbox',
                          component=selected_box.component)
        EVENT_MANAGER.fire_event(new_event)

    def select_box(self):
        selected_item = self.box_list_view.currentItem()
        if selected_item:
            selected_component = selected_item.component
            box = selected_component.component

            # set field values
            hurtactive = 2 if box.hurtactive else 0
            hitactive = 2 if box.hitactive else 0
            blockactive = 2 if box.blockactive else 0
            solid = 2 if box.solid else 0
            self.box_x_field.setText(str(box.rect.x()))
            self.box_y_field.setText(str(box.rect.y()))
            self.box_width_field.setText(str(box.rect.width()))
            self.box_height_field.setText(str(box.rect.height()))
            self.box_hurtactive_check.setCheckState(hurtactive)
            self.box_hitactive_check.setCheckState(hitactive)
            self.box_blockactive_check.setCheckState(blockactive)
            self.box_solid_check.setCheckState(solid)

            # update drawn box in graphic viewer
            self.graphic_viewer.set_box(x=box.rect.x(),
                                        y=box.rect.y(),
                                        w=box.rect.width(),
                                        h=box.rect.height())

            # fire event for selecting a box
            new_event = Event('selected_box',
                              box_component=selected_component,
                              entity=selected_component.component.entity_id)
            EVENT_MANAGER.fire_event(new_event)

    def set_frame(self, event):
        entity = event.entity
        frame = event.frame_component
        file_name = event.graphic_file_name
        self.selected_frame = frame
        boxes = frame.component.hitboxes
        crop = frame.component.crop

        self.show_graphic(file_name, crop)

        # do a soft clear of the box list
        for i in range(self.box_list_view.count()-1,-1,-1):
            self.box_list_view.takeItem(i)

        # repopulate box list
        for box in boxes:
            box_wrapper = WidgetItemComponent(box.text, box)
            self.box_list_view.addItem(box)

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

    def show_graphic(self, file_name, crop):
        self.graphic_viewer.show_graphic(file_name, crop)

    def update_fields(self, event):
        box = event.box
        self.box_x_field.setText(str(box.x()))
        self.box_y_field.setText(str(box.y()))
        self.box_width_field.setText(str(box.width()))
        self.box_height_field.setText(str(box.height()))

    def set_hitactive(self, state):
        self.check_context['hitactive'] = state
        self.graphic_viewer.awkward_update()

    def set_hurtactive(self, state):
        self.check_context['hurtactive'] = state
        self.graphic_viewer.awkward_update()

    def set_blockactive(self,state):
        self.check_context['blockactive'] = state
        self.graphic_viewer.awkward_update()

    def set_solid(self, state):
        self.check_context['solid'] = state
        self.graphic_viewer.awkward_update()
