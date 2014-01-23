import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from animation_definition import Animation
from common import *


class Frame(TextListItem):
    def __init__(self, crop, repeat=0, hitboxes=None):
        super(Frame, self).__init__()
        self.crop = crop
        self.repeat = repeat
        self.hitboxes = list() if hitboxes is None else hitboxes
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '({crop.x},{crop.y},{crop.width},{crop.height}) - {repeat}'
        self.text = t.format(crop=self.crop, repeat=self.repeat)
        

class FrameDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(FrameDefinitionFrame, self).__init__(renderer, draw_to, 
                                                   context, offset, widgets)
        self.text = 'Frame Definition'
        self.canvas = pygame.Surface((800, 800))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_offset = (250, 0)
        self.canvas_rect.x += self.canvas_offset[0]
        self.canvas_rect.y += self.canvas_offset[1]
        #self.frames = self.context['frames']
        self.frames = ListItemCollection()
        self.anis = self.context['animations']
        self.current_frame = None
        self.current_box = None
        self.click_down = False
        self.image = None

        # define widgets
        self.frame_list = ScrolledList(170, 250, self.frames)
        self.frame_x_label = Label('Frame X')
        self.frame_x = Entry()
        self.frame_y_label = Label('Frame Y')
        self.frame_y = Entry()
        self.frame_width_label = Label('Frame Width')
        self.frame_width = Entry()
        self.frame_height_label = Label('Frame Height')
        self.frame_height = Entry()
        self.repeat_label = Label('Repeat')
        self.repeat = Entry()
        self.add_button = Button('Add Frame')
        self.update_button = Button('Update Frame')
        self.remove_button = Button('Remove')
        self.ani_list = ScrolledList(200, 150, self.anis)
        self.ani_label = Label('Choose Animation')

        # build widget list
        append = self.widgets.append
        append(self.frame_list)
        append(self.frame_x_label)
        append(self.frame_x)
        append(self.frame_y_label)
        append(self.frame_y)
        append(self.frame_width_label)
        append(self.frame_width)
        append(self.frame_height_label)
        append(self.frame_height)
        append(self.repeat_label)
        append(self.repeat)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)
        append(self.ani_list)
        append(self.ani_label)

        # widget properties
        self.frame_x_label.align = ALIGN_LEFT
        self.frame_y_label.align = ALIGN_LEFT
        self.frame_width_label.align = ALIGN_LEFT
        self.frame_height_label.align = ALIGN_LEFT
        self.ani_label.align = ALIGN_NONE

        # positions
        self.set_pos(self.frame_x_label, (10, 200))
        self.set_pos(self.frame_x, (85, 200))
        self.set_pos(self.frame_y_label, (10, 225))
        self.set_pos(self.frame_y, (85, 225))
        self.set_pos(self.frame_width_label, (10, 250))
        self.set_pos(self.frame_width, (85, 250))
        self.set_pos(self.frame_height_label, (10, 275))
        self.set_pos(self.frame_height, (85, 275))
        self.set_pos(self.repeat_label, (10, 300))
        self.set_pos(self.repeat, (85, 300))
        self.set_pos(self.add_button, (10, 340))
        self.set_pos(self.update_button, (85, 340))
        self.set_pos(self.remove_button, (10, 370))
        self.set_pos(self.frame_list, (10, 400))
        self.set_pos(self.ani_label, (10, 0))
        self.set_pos(self.ani_list, (10, 25))

        # miscelaneous
        self.frame_list.selectionmode = SELECTION_SINGLE
        self.update_button.sensitive = False
        self.remove_button.sensitive = False

        # wire up GUI events
        self.add_button.connect_signal(SIG_CLICKED, self.add_frame)
        self.frame_list.connect_signal(SIG_SELECTCHANGED, self.set_current_frame)
        self.frame_list.connect_signal(SIG_SELECTCHANGED, self.activate_controls)
        self.update_button.connect_signal(SIG_CLICKED, self.update_frame)
        self.remove_button.connect_signal(SIG_CLICKED, self.remove_frame)
        self.ani_list.connect_signal(SIG_SELECTCHANGED, self._select_animation)

    def add_frame(self):
        crop = pygame.Rect(int(self.frame_x.text), 
                           int(self.frame_y.text),
                           int(self.frame_width.text),
                           int(self.frame_height.text))
        repeat = int(self.repeat.text)
        new_frame = Frame(crop, repeat)
        self.frame_list.items.append(new_frame)
        #self.context['frames'].append(new_frame)
        self.context['chosen_animation'].frames.append(new_frame)

    def set_current_frame(self):
        selection = self.frame_list.get_selected()[0]
        if self.current_box is None:
            self.current_box = pygame.Rect(0,0,0,0)
        self.current_box.x = selection.crop.x
        self.current_box.y = selection.crop.y
        self.current_box.width = selection.crop.width
        self.current_box.height = selection.crop.height
        self.frame_x.text = str(selection.crop.x)
        self.frame_y.text = str(selection.crop.y)
        self.frame_width.text = str(selection.crop.width)
        self.frame_height.text = str(selection.crop.height)
        self.repeat.text = str(selection.repeat)
        self.context['chosen_frame'] = selection

    def _select_animation(self):
        ani_selection = self.ani_list.get_selected()[0]
        if ani_selection is not None:
            self.image = self._load_image(ani_selection.image_file)
            self.context['chosen_animation'] = ani_selection
            self.frames = ListItemCollection(ani_selection.frames)
            self.frame_list.items = self.frames
            self.frame_list.child.update_items()

    def activate_controls(self):
        selection = self.frame_list.get_selected()
        if len(selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False

    def _load_image(self, filename):
        return pygame.image.load(filename)

    def update_frame(self):
        selected = self.frame_list.get_selected()[0]
        selected.crop.x = int(self.frame_x.text)
        selected.crop.y = int(self.frame_y.text)
        selected.crop.width = int(self.frame_width.text)
        selected.crop.height = int(self.frame_height.text)
        selected.repeat = int(self.repeat.text)
        selected.refresh_text()

    def remove_frame(self):
        selected = self.frame_list.get_selected()[0]
        self.frame_list.items.remove(selected)
        self.context['chosen_animation'].frames.remove(selected)
        self.activate_controls()

    def cleanup_box(self):
        rect = self.current_box
        # flip the origin corner to the top left if necessary
        if rect.width < 0:
            rect.x = rect.x + rect.width
            rect.width = 0 - rect.width
        if rect.height < 0:
            rect.y = rect.y + rect.height
            rect.height = 0 - rect.height
        self.frame_x.text = str(rect.x)
        self.frame_y.text = str(rect.y)
        self.frame_width.text = str(rect.width)
        self.frame_height.text = str(rect.height)

    def update(self, events):
        self.canvas.fill(WHITE)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_RIGHT:
                    if self.canvas_rect.collidepoint(event.pos):
                        self.click_down = True
                        offset_x = self.offset[0] + self.canvas_offset[0]
                        offset_y = self.offset[1] + self.canvas_offset[1]
                        translated_pos = (event.pos[0] - offset_x,
                                          event.pos[1] - offset_y)
                        current_box = pygame.Rect(translated_pos, (0,0))
                        self.frame_x.text = str(current_box.x)
                        self.frame_y.text = str(current_box.y)
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
                            self.cleanup_box()

        # draw image
        if self.image is not None:
            draw_image(self.canvas, self.image)
        
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
                draw_box(self.canvas, temp_box)

        # draw the current box
        if self.current_box:
            draw_box(self.canvas, self.current_box)

        # draw to the parent surface
        self.draw_to.blit(self.canvas, self.canvas_offset)

    def activate(self):
        super(FrameDefinitionFrame, self).activate()
        items = ListItemCollection()
        # can't directly copy items over from one ScrolledLIst's
        # ListItemCollection to another, because of some hacky stuff
        # in the ocempgui library.  Can't properly mark each item as
        # dirty, so when the new ScrolledList's ListPortView tries to
        # update itself, it tries to redraw the ListItem's image, which
        # hasn't been defined for that ListPortView yet
        # Creating copies of each Frame is not the cleanest solution,
        # but it works
        for item in self.context['animations']:
            copy_ani = Animation(item.image_file)
            items.append(copy_ani)
        self.ani_list.items = items
        self.ani_list.child.update_items()

def draw_image(canvas, image):
    canvas.blit(image, (0,0))


def draw_box(canvas, box):
    color = RED
    pygame.draw.rect(canvas, color, box, 1)
    
