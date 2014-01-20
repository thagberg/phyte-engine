import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from common import *

class HitBox(TextListItem):
    def __init__(self, rect, hitactive=False, hurtactive=False,
                 blockactive=False, solid=False):
        super(HitBox, self).__init__()
        self.rect = rect
        self.hitactive = hitactive
        self.hurtactive = hurtactive
        self.blockactive = blockactive
        self.solid = solid
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        self.text = '%s:%s:%s:%s / (%d,%d) - (%d, %d)' % (self.hitactive,
                                                          self.hurtactive,
                                                          self.blockactive,
                                                          self.solid,
                                                          self.rect.x,
                                                          self.rect.y,
                                                          self.rect.width,
                                                          self.rect.height)

class HitBoxDefineFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, image, curr_frame, 
                 offset=(0,0), widgets=None):
        super(HitBoxDefineFrame, self).__init__(renderer, draw_to, context, 
                                                offset, widgets)
        self.text = 'Hit Box Definition'
        self.image = image
        self.curr_frame = curr_frame
        self.canvas = pygame.Surface((800, 800))
        self.canvas_rect = pygame.get_rect()
        self.boxes = self.context['boxes']
        self.click_down = False
        self.current_box = None
        self.current_frame = None

        # define widgets
        self.hitactive_check = CheckButton("Hit Active")
        self.hurtactive_check = CheckButton("Hurt Active")
        self.blockactive_check = CheckButton("Block Active")
        self.solid_check = CheckButton("Solid")
        self.box_x_label = Label('Box X')
        self.box_x = Entry()
        self.box_y_label = Label('Box Y')
        self.box_y = Entry()
        self.box_width_label = Label('Box Width')
        self.box_width = Entry()
        self.box_height_label = Label('Box Height')
        self.box_height = Entry()
        self.add_button = Button('Add Box')
        self.box_list = ScrolledList(300, 300, self.boxes)
        self.update_button = Button('Update Box')
        self.remove_button = Button('Remove Box')

        # set widget properties
        # alignments
        self.box_x_label.align = ALIGN_LEFT
        self.box_y_label.align = ALIGN_LEFT
        self.box_width_label.align = ALIGN_LEFT
        self.box_height_label.align = ALIGN_LEFT
        # positions
        self.set_pos(self.hitactive_check.topleft, (10, 25))
        self.set_pos(self.hurtactive_check.topleft, (10, 50))
        self.set_pos(self.blockactive_check.topleft, (10, 75))
        self.set_pos(self.solid_check.topleft, (10, 100))
        self.set_pos(self.box_x_label.topleft, (150, 25))
        self.set_pos(self.box_x.topleft, (225, 25))
        self.set_pos(self.box_y_label.topleft, (150, 50))
        self.set_pos(self.box_y.topleft, (225, 50))
        self.set_pos(self.box_width_label.topleft, (150, 75))
        self.set_pos(self.box_width.topleft, (225, 75))
        self.set_pos(self.box_height_label.topleft, (150, 100))
        self.set_pos(self.box_height.topleft, (225, 100))
        self.set_pos(self.add_button.topleft, (320, 145))
        self.set_pos(self.box_list.topleft, (10, 140))
        self.set_pos(self.update_button.topleft, (320, 175))
        self.set_pos(self.remove_button.topleft, (320, 205))
        # miscelaneous 
        self.box_list.selectionmode = SELECTION_SINGLE
        self.update_button.sensitive = False
        self.remove_button.sensitive = False

        # wire up GUI events
        self.add_button.connect_signal(SIG_CLICKED, self.add_box)
        self.box_list.connect_signal(SIG_SELECTCHANGED, 
                                     self.set_current_box, 
                                     self.box_list.get_selected())
        self.box_list.connect_signal(SIG_SELECTCHANGED, self.activate_controls)
        self.update_button.connect_signal(SIG_CLICKED, self.update_box)
        self.remove_button.connect_signal(SIG_CLICKED, self.remove_box)

        # add widgets to widgets list
        append = self.widgets.append
        append(self.hitactive_check)
        append(self.hurtactive_check)
        append(self.blockactive_check)
        append(self.solid_check)
        append(self.box_x_label)
        append(self.box_y_label)
        append(self.box_x)
        append(self.box_y)
        append(self.box_width_label)
        append(self.box_width)
        append(self.box_height_label)
        append(self.box_height)
        append(self.add_button)
        append(self.box_list)
        append(self.update_button)
        append(self.remove_button)

    def update(self, events):
        # clear the canvas
        self.canvas.fill(WHITE)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_RIGHT:
                    if self.canvas_rect.collidepoint(event.pos):
                        current_box = self.current_box
                        self.click_down = True
                        translated_pos = (event.pos[0] - frame_pos[0],
                                          event.pos[1] - frame_pos[1])
                        current_box = pygame.Rect(translated_pos, (0,0))
                        self.box_x.text = str(current_box.x)
                        self.box_y.text = str(current_box.y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_RIGHT:
                    if self.canvas_rect.collidepoint(event.pos):
                        current_box = self.current_box
                        self.click_down = False
                        end_pos = event.pos
                        translated_pos = (event.pos[0] - frame_pos[0],
                                          event.pos[1] - frame_pos[1])
                        current_box.width = translated_pos[0] - current_box.x
                        current_box.height = translated_pos[1] - current_box.y
                        self.cleanup_box(current_box)

        # draw the animation frame
        self.draw_frame(self.canvas, self.image, self.curr_frame)

        # draw temporary click-and-drag box
        if self.click_down:
            current_pos = pygame.mouse.get_pos()
            current_box = self.current_box
            translated_pos = (current_pos[0] - frame_pos[0],
                              current_pos[1] - frame_pos[1])
            temp_box = pygame.Rect(current_box.x,
                                   current_box.y,
                                   translated_pos[0] - current_box.x, 
                                   translated_pos[1] - current_box.y) 
            hb = HitBox(temp_box, 
                        hitactive=self.hitactive_check.active,
                        hurtactive=self.hurtactive_check.active,
                        blockactive=self.blockactive_check.active,
                        solid=self.solid_check.active)
            self.draw_box(self.canvas, hb)

        # draw the current box
        if current_box:
            hb = HitBox(current_box, 
                        hitactive=self.hitactive_check.active,
                        hurtactive=self.hurtactive_check.active,
                        blockactive=self.blockactive_check.active,
                        solid=self.solid_check.active)
            self.draw_box(self.canvas, hb)

        # draw canvas to editor pane
        pass

    def draw_frame(self, canvas, image, crop):
        dest_x = canvas.get_width()/2 - crop[2]/2
        dest_y = canvas.get_height()/2 - crop[3]/2
        canvas.blit(image, (dest_x, dest_y), crop)

    def draw_box(canvas, box, offset=(0,0)):
        rect = box.rect.copy()
        rect[0] = rect[0] + offset[0]
        rect[1] = rect[1] + offset[1]
        color = BLACK
        if box.hitactive:
            if box.hurtactive:
                color = PURPLE
            else:
                color = BLUE
        elif box.hurtactive:
            color = RED
        elif box.blockactive:
            color = GREEN
        pygame.draw.rect(canvas, color, rect, 1)

    def add_box():
        rect = pygame.Rect(int(box_x.text),
                           int(box_y.text),
                           int(box_width.text),
                           int(box_height.text))
        hitactive = self.hitactive_check.active
        hurtactive = self.hurtactive_check.active
        blockactive = self.blockactive_check.active
        solid = self.solid_check.active
        hitbox = HitBox(rect, hitactive, hurtactive, blockactive, solid)
        self.box_list.items.append(hitbox)

    def update_box():
        selected = box_list.get_selected()[0]
        rect = selected.rect
        rect.x = int(box_x.text)
        rect.y = int(box_y.text)
        rect.width = int(box_width.text)
        rect.height = int(box_height.text)
        selected.hitactive = hitactive_check.active
        selected.hurtactive = hurtactive_check.active
        selected.blockactive = blockactive_check.active
        selected.solid = solid_check.active
        selected.refresh_text()

    def remove_box():
        selected = self.box_list.get_selected()[0]
        self.box_list.items.remove(selected)
        self.activate_controls()

    def cleanup_box(rect):
        # flip the origin corner to the top left if necessary
        if rect.width < 0:
            rect.x = rect.x + rect.width
            rect.width = 0 - rect.width
        if rect.height < 0:
            rect.y = rect.y + rect.height
            rect.height = 0 - rect.height
        self.box_x.text = str(rect.x)
        self.box_y.text = str(rect.y)
        self.box_width.text = str(rect.width)
        self.box_height.text = str(rect.height)

    def set_current_box(selection):
        selection = self.box_list.get_selected()[0]
        self.current_box.x = selection.rect.x
        self.current_box.y = selection.rect.y
        self.current_box.width = selection.rect.width
        self.current_box.height = selection.rect.height
        self.box_x.text = str(selection.rect.x)
        self.box_y.text = str(selection.rect.y)
        self.box_width.text = str(selection.rect.width)
        self.box_height.text = str(selection.rect.height)
        self.hitactive_check.active = selection.hitactive
        self.hurtactive_check.active = selection.hurtactive
        self.blockactive_check.active = selection.blockactive
        self.solid_check.active = selection.solid

    def activate_controls():
        selection = self.box_list.get_selected()
        if len(selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False
