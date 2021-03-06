import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from frame_definition import Frame
from animation_definition import Animation
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

class HitBoxDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, image, offset=(0,0), 
                 widgets=None):
        super(HitBoxDefinitionFrame, self).__init__(renderer, draw_to, context, 
                                                    offset, widgets)
        self.text = 'Hit Box Definition'
        self.image = image
        self.canvas = pygame.Surface((600, 600))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_offset = (380,0)
        self.canvas_rect.x += self.canvas_offset[0] + self.offset[0]
        self.canvas_rect.y += self.canvas_offset[1] + self.offset[1]
        #self.boxes = self.context['boxes']
        #self.frames = self.context['frames']
        self.boxes = ListItemCollection()
        self.frames = ListItemCollection()
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
        self.box_list = ScrolledList(240, 300, self.boxes)
        self.update_button = Button('Update Box')
        self.remove_button = Button('Remove Box')
        self.frame_list = ScrolledList(175, 100, self.frames)
        self.frame_label = Label('Choose Frame')

        # build widget list
        append = self.widgets.append
        append(self.hitactive_check)
        append(self.hurtactive_check)
        append(self.blockactive_check)
        append(self.solid_check)
        append(self.box_x_label)
        append(self.box_x)
        append(self.box_y_label)
        append(self.box_y)
        append(self.box_width_label)
        append(self.box_width)
        append(self.box_height_label)
        append(self.box_height)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)
        append(self.box_list)
        append(self.frame_list)
        append(self.frame_label)

        # set widget properties
        # alignments
        self.box_x_label.align = ALIGN_LEFT
        self.box_y_label.align = ALIGN_LEFT
        self.box_width_label.align = ALIGN_LEFT
        self.box_height_label.align = ALIGN_LEFT
        self.frame_label.align = ALIGN_NONE
        # positions
        self.set_pos(self.frame_label, (10, 0))
        self.set_pos(self.frame_list, (10, 20))
        self.set_pos(self.hitactive_check, (10, 200))
        self.set_pos(self.hurtactive_check, (10, 225))
        self.set_pos(self.blockactive_check, (10, 250))
        self.set_pos(self.solid_check, (10, 275))
        self.set_pos(self.box_x_label, (150, 200))
        self.set_pos(self.box_x, (225, 200))
        self.set_pos(self.box_y_label, (150, 225))
        self.set_pos(self.box_y, (225, 225))
        self.set_pos(self.box_width_label, (150, 250))
        self.set_pos(self.box_width, (225, 250))
        self.set_pos(self.box_height_label, (150, 275))
        self.set_pos(self.box_height, (225, 275))
        self.set_pos(self.add_button, (250, 310))
        self.set_pos(self.box_list, (10, 310))
        self.set_pos(self.update_button, (250, 340))
        self.set_pos(self.remove_button, (250, 370))
        # miscelaneous 
        self.box_list.selectionmode = SELECTION_SINGLE
        self.add_button.sensitive = False
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
        self.frame_list.connect_signal(SIG_SELECTCHANGED, self._select_frame)

    def _select_frame(self):
        frame_selection = self.frame_list.get_selected()[0]
        if frame_selection is not None:
            selected_ani = self.context['chosen_animation']
            self.image = pygame.image.load(selected_ani.image_file)
            self.boxes = ListItemCollection(frame_selection.hitboxes)
            self.box_list.items = self.boxes
            self.box_list.child.update_items()
            self.activate_controls()

    def update(self, events):
        # clear the canvas
        self.canvas.fill(WHITE)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_RIGHT:
                    if self.canvas_rect.collidepoint(event.pos):
                        current_box = self.current_box
                        self.click_down = True
                        offset_x = self.offset[0] + self.canvas_offset[0]
                        offset_y = self.offset[1] + self.canvas_offset[1]
                        translated_pos = (event.pos[0] - offset_x,
                                          event.pos[1] - offset_y)
                        current_box = pygame.Rect(translated_pos, (0,0))
                        self.box_x.text = str(current_box.x)
                        self.box_y.text = str(current_box.y)
                        self.current_box = current_box
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_RIGHT:
                    if self.canvas_rect.collidepoint(event.pos):
                        current_box = self.current_box
                        self.click_down = False
                        if current_box is not None:
                            end_pos = event.pos
                            offset_x = self.offset[0] + self.canvas_offset[0]
                            offset_y = self.offset[1] + self.canvas_offset[1]
                            translated_pos = (event.pos[0] - offset_x,
                                              event.pos[1] - offset_y)
                            current_box.width = translated_pos[0] - current_box.x
                            current_box.height = translated_pos[1] - current_box.y
                            self.cleanup_box(current_box)

        # draw the animation frame
        if self.current_frame is not None:
            self.draw_frame(self.canvas, self.image, self.current_frame.crop)

        # draw temporary click-and-drag box
        if self.click_down:
            current_pos = pygame.mouse.get_pos()
            current_box = self.current_box
            offset_x = self.offset[0] + self.canvas_offset[0]
            offset_y = self.offset[1] + self.canvas_offset[1]
            translated_pos = (current_pos[0] - offset_x,
                              current_pos[1] - offset_y)
            if current_box is not None:
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
        if self.current_box:
            hb = HitBox(self.current_box, 
                        hitactive=self.hitactive_check.active,
                        hurtactive=self.hurtactive_check.active,
                        blockactive=self.blockactive_check.active,
                        solid=self.solid_check.active)
            self.draw_box(self.canvas, hb)

        # draw canvas to editor pane
        self.draw_to.blit(self.canvas, self.canvas_offset)

    def draw_frame(self, canvas, image, crop):
        dest_x = canvas.get_width()/2 - crop[2]/2
        dest_y = canvas.get_height()/2 - crop[3]/2
        canvas.blit(image, (dest_x, dest_y), crop)

    def draw_box(self, canvas, box, offset=(0,0)):
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

    def add_box(self):
        rect = pygame.Rect(int(self.box_x.text),
                           int(self.box_y.text),
                           int(self.box_width.text),
                           int(self.box_height.text))
        hitactive = self.hitactive_check.active
        hurtactive = self.hurtactive_check.active
        blockactive = self.blockactive_check.active
        solid = self.solid_check.active
        hitbox = HitBox(rect, hitactive, hurtactive, blockactive, solid)
        self.box_list.items.append(hitbox)
        #self.context['boxes'].append(hitbox)
        self.context['chosen_frame'].hitboxes.append(hitbox)
        self.context['components'].append(hitbox)

    def update_box(self):
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

    def remove_box(self):
        selected = self.box_list.get_selected()[0]
        self.box_list.items.remove(selected)
        self.context['chosen_frame'].hitboxes.remove(selected)
        self.context['components'].remove(selected)
        self.activate_controls()

    def cleanup_box(self, rect):
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

    def set_current_box(self, selection):
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
        self.box_list.child.update_items()

    def activate_controls(self):
        frame_selection = self.frame_list.get_selected()[0]
        selection = self.box_list.get_selected()
        # first process frame selection stuff
        if frame_selection is not None:
            self.current_frame = frame_selection
            self.context['chosen_frame'] = frame_selection
        # then process box control stuff
        if self.current_frame is None:
            self.add_button.sensitive = False
        else:
            self.add_button.sensitive = True
        if len(selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False

    def activate(self):
        super(HitBoxDefinitionFrame, self).activate()
        items = ListItemCollection()
        # can't directly copy items over from one ScrolledLIst's
        # ListItemCollection to another, because of some hacky stuff
        # in the ocempgui library.  Can't properly mark each item as
        # dirty, so when the new ScrolledList's ListPortView tries to
        # update itself, it tries to redraw the ListItem's image, which
        # hasn't been defined for that ListPortView yet
        # Creating copies of each Frame is not the cleanest solution,
        # but it works
        ani = self.context['chosen_animation']
        if isinstance(ani, Animation):
            for item in ani.frames:
                copy_frame = Frame(item.crop,
                                   item.repeat,
                                   item.hitboxes)
                items.append(copy_frame)
            self.frame_list.items = items
            self.frame_list.child.update_items()

    def deactivate(self):
        frame_selection = self.frame_list.get_selected()
        if len(frame_selection) > 0:
            frame_selection = frame_selection[0]
            frame_selection.hitboxes = list()
            for box in self.boxes:
                frame_selection.hitboxes.append(box) 
        super(HitBoxDefinitionFrame, self).deactivate()

