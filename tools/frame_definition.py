import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from common import *


class Frame(TextListItem):
    def __init__(self, crop, hitboxes=lambda:list(), repeat=0):
        super(Frame, self).__init__()
        self.crop = crop
        self.repeat = repeat
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '({crop.x},{crop.y},{crop.width},{crop.height}) - {repeat}'
        return t.format(crop=self.crop, repeat=self.repeat)
        

class FrameDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, image, offset=(0,0), widgets=None):
        super(FrameDefinitionFrame, self).__init__(renderer, draw_to, offset, widgets)
        self.text = 'Frame Definition'
        self.canvas = pygame.Surface((800, 800))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_offset = (350, 0)
        self.image = image
        self.frames = ListItemCollection()
        self.current_frame = None
        self.current_box = None
        self.click_down = False

        # define widgets
        self.frame_list = ScrolledList(300, 300, self.frames)
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

        # widget properties
        self.frame_x_label.align = ALIGN_LEFT
        self.frame_y_label.align = ALIGN_LEFT
        self.frame_width_label.align = ALIGN_LEFT
        self.frame_height_label.align = ALIGN_LEFT

        # positions
        self.set_pos(self.frame_x_label, (10, 25))
        self.set_pos(self.frame_x, (85, 25))
        self.set_pos(self.frame_y_label, (10, 50))
        self.set_pos(self.frame_y, (85, 50))
        self.set_pos(self.frame_width_label, (10, 75))
        self.set_pos(self.frame_width, (85, 75))
        self.set_pos(self.frame_height_label, (10, 100))
        self.set_pos(self.frame_height, (85, 100))
        self.set_pos(self.frame_list, (10, 125))

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

    def add_frame(self):
        crop = pygame.Rect(int(self.frame_x.text), 
                           int(self.frame_y.text),
                           int(self.frame_width.text),
                           int(self.frame_height.text))
        repeat = int(self.repeat.text)
        new_frame = Frame(crop, repeat)
        self.frame_list.items.append(new_frame)

    def set_current_frame(self):
        selection = self.frame_list.get_selected()[0]
        self.current_box.x = selection.crop.x
        self.current_box.y = selection.crop.y
        self.current_box.width = selection.crop.width
        self.current_box.height = selection.crop.height
        self.frame_x.text = str(selection.crop.x)
        self.frame_y.text = str(selection.crop.y)
        self.frame_width.text = str(selection.crop.width)
        self.frame_height.text = str(selection.crop.height)
        self.repeat.text = str(selection.repeat)

    def activate_controls(self):
        selection = self.frame_list.get_selected()
        if len(selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False

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
                        translated_pos = (event.pos[0] - self.offset[0],
                                          event.pos[1] - self.offset[1])
                        current_box = pygame.Rect(translated_pos, (0,0))
                        self.frame_x.text = str(current_box.x)
                        self.frame_y.text = str(current_box.y)
                        self.current_box = current_box
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_RIGHT:
                    if self.canvas_rect.collidepoint(event.pos):
                        current_box = self.current_box
                        self.click_down = False
                        end_pos = event.pos
                        translated_pos = (event.pos[0] - self.offset[0],
                                          event.pos[1] - self.offset[1])
                        current_box.width = translated_pos[0] - current_box.x
                        current_box.height = translated_pos[1] - current_box.y
                        self.cleanup_box()

        # draw image
        draw_image(self.canvas, self.image)
        
        # draw temporary click-and-drag box
        if self.click_down:
            current_pos = pygame.mouse.get_pos()
            current_box = self.current_box
            translated_pos = (current_pos[0] - self.offset[0],
                              current_pos[1] - self.offset[1])
            temp_box = pygame.Rect(current_box.x,
                                   current_box.y,
                                   translated_pos[0] - current_box.x, 
                                   translated_pos[1] - current_box.y) 
            draw_box(self.canvas, temp_box)

        # draw the current box
        if self.current_box:
            draw_box(self.canvas, self.current_box)

        # draw to the parent surface
        self.draw_to.blit(self.canvas, (
                          self.offset[0],
                          self.offset[1]))


def draw_image(canvas, image):
    canvas.blit(image, (0,0))


def draw_box(canvas, box):
    color = RED
    pygame.draw.rect(canvas, color, box, 1)
