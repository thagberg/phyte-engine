import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from common import *


class Animation(TextListItem):
    def __init__(self, image_file, image, frames=None):
        super(Animation, self).__init__()
        self.image_file = image_file
        self.image = image
        self.frames = list() if frames is None else frames
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        t = '{image} - {length} frames'
        self.text = t.format(image=self.image_file, length=len(self.frames))


class AnimationDefinitionFrame(EditorFrame):
    def __init__(self, renderer, draw_to, context, offset=(0,0), widgets=None):
        super(AnimationDefinitionFrame, self).__init__(renderer, draw_to,
                                                       context, offset, widgets)
        self.text = 'Animation Definiton'
        self.canvas = pygame.Surface((600,600))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_offset = (380, 0)
        self.canvas_rect.x += self.canvas_offset[0] + self.offset[0]
        self.canvas_rect.y += self.canvas_offset[1] + self.offset[1]
        self.files = self.context['files']
        self.image = None

        # define widgets
        self.file_list = ScrolledList(240, 300, self.files)
        self.add_button = Button('Add Animation')
        self.update_button = Button('Update Animation')
        self.remove_button = Button('Remove Animation')
        self.file_button = Button('Browse')
        self.file_entry = Entry()

        # build widget list
        append = self.widgets.append
        append(self.file_list)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)
        append(self.file_button)
        append(self.file_entry)

        # set widget properties
        self.set_pos(self.file_button, (10,0))
        self.set_pos(self.file_entry, (80, 0))
        self.set_pos(self.file_list, (10, 30))
        self.set_pos(self.add_button, (255, 30))
        self.set_pos(self.update_button, (255, 60))
        self.set_pos(self.remove_button, (255, 90))

        # miscelaneous
        self.add_button.sensitive = False
        self.update_button.sensitive = False
        self.remove_button.sensitive = False
        self.file_entry.minsize = (250, self.file_entry.minsize[1])

        # wire up GUI
        self.file_button.connect_signal(SIG_CLICKED, 
                                        self._open_file_dialog,
                                        self.file_entry)
        self.file_list.connect_signal(SIG_SELECTCHANGED, 
                                      self._activate_controls)

    def _open_file_dialog(self, entry):
        file_dlg = FileDialog('Select Image File...',
                              [Button('OK'), Button('Cancel')],
                              [DLGRESULT_OK, DLGRESULT_CANCEL])
        file_dlg.filelist.selectionmode = SELECTION_SINGLE
        self.set_pos(file_dlg, (10, 0))
        file_dlg.connect_signal(SIG_DIALOGRESPONSE, 
                                self._set_file, 
                                file_dlg, 
                                entry)
        self.renderer.add_widget(file_dlg)

    def _set_file(self, result, dialog, entry):
        text = ''
        if result == DLGRESULT_OK:
            text = dialog.get_filenames()[0]
            self._load_image(text)
        else:
            text = 'No file selected'
        dialog.destroy()
        entry.text = text
        self._activate_controls()

    def _load_image(self, file_name):
        self.image = pygame.image.load(file_name)

    def _activate_controls(self):
        selection = self.file_list.get_selected()
        if self.image is not None:
            self.add_button.sensitive = True
        else:
            self.add_button.sensitive = False

        if len(selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False
            

    def update(self, events):
        self.canvas.fill(WHITE)
        for event in events:
            pass

        # draw loaded image
        if self.image is not None:
            self.canvas.blit(self.image, (0,0))

        self.draw_to.blit(self.canvas, self.canvas_offset)

    def draw_frame(self, canvas, image, crop):
        dest_x = canvas.get_width()/2 - crop[2]/2
        dest_y = canvas.get_height()/2 - crop[3]/2
        canvas.blit(image, (dest_x, dest_y), crop)
