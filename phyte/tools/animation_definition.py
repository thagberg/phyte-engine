import pygame
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from frame import EditorFrame
from common import *
from engine import animation, graphics2d


class Animation(TextListItem):
    def __init__(self, image_file, frames=None):
        super(Animation, self).__init__()
        self.image_file = image_file
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
        self.anis = self.context['animations'][self.context['chosen_entity']]
        self.graphics = self.context['graphics']
        self.image = None

        # define widgets
        self.graphic_list = ScrolledList(240, 300, self.graphics)
        self.add_button = Button('Add Graphic')
        self.update_button = Button('Update Graphic')
        self.remove_button = Button('Remove Graphic')
        self.file_button = Button('Browse')
        self.file_entry = Entry()
        self.ani_list = ScrolledList(200, 200, self.anis)
        self.add_ani_button = Button('Add Animation')
        self.remove_ani_button = Button('Remove Animation')

        # build widget list
        append = self.widgets.append
        append(self.graphic_list)
        append(self.add_button)
        append(self.update_button)
        append(self.remove_button)
        append(self.file_button)
        append(self.file_entry)
        append(self.ani_list)
        append(self.add_ani_button)
        append(self.remove_ani_button)

        # set widget properties
        self.set_pos(self.file_button, (10,0))
        self.set_pos(self.file_entry, (80, 0))
        self.set_pos(self.graphic_list, (10, 30))
        self.set_pos(self.add_button, (255, 30))
        self.set_pos(self.update_button, (255, 60))
        self.set_pos(self.remove_button, (255, 90))
        self.set_pos(self.ani_list, (10, 360))
        self.set_pos(self.add_ani_button, (215, 360))
        self.set_pos(self.remove_ani_button, (215, 390))

        # miscelaneous
        self.add_button.sensitive = False
        self.update_button.sensitive = False
        self.remove_button.sensitive = False
        self.file_entry.minsize = (250, self.file_entry.minsize[1])
        self.add_ani_button.sensitive = False
        self.remove_ani_button.sensitive = False

        # wire up GUI
        self.file_button.connect_signal(SIG_CLICKED, 
                                        self._open_file_dialog,
                                        self.file_entry)
        self.graphic_list.connect_signal(SIG_SELECTCHANGED, 
                                         self._activate_controls)
        self.graphic_list.connect_signal(SIG_SELECTCHANGED,
                                         self._set_current_graphic)
        self.add_button.connect_signal(SIG_CLICKED, self._add_graphic)
        self.remove_button.connect_signal(SIG_CLICKED, self._remove_graphic)
        self.add_ani_button.connect_signal(SIG_CLICKED, 
                                           self._add_animation)
        self.remove_ani_button.connect_signal(SIG_CLICKED, 
                                              self._remove_animation)
        self.ani_list.connect_signal(SIG_SELECTCHANGED, 
                                     self._activate_controls)

    def _add_animation(self):
        selection = self.graphic_list.get_selected()[0]
        graphic = selection.component
        ani = animation.AnimationComponent(entity_id=self.context['chosen_entity'],
                                           graphic=graphic)
        get_text = lambda: 'Animation: {file}'.format(file=graphic.file_name)
        ani_wrapper = Component(ani, get_text)
        self.ani_list.items.append(ani_wrapper)
        self.ani_list.child.update_items()
        self.anis.append(ani)

    def _remove_animation(self):
        selection = self.ani_list.get_selected()[0]
        self.ani_list.items.remove(selection)
        self.ani_list.child.update_items()
        self.anis.remove(selection.component)

    def _set_current_graphic(self):
        selection = self.graphic_list.get_selected()[0]
        self._load_image(selection.component.file_name)

    def _add_graphic(self):
        image_file = self.file_entry.text
        image = self._load_image(image_file)
        new_graphic = graphics2d.GraphicsComponent(self.context['chosen_entity'].name,
                                                   image, image_file)
        get_text = lambda: '{file}'.format(file=new_graphic.file_name)
        graphic_wrapper = Component(new_graphic, get_text)
        self.graphic_list.items.append(graphic_wrapper)
        self.graphics.append(new_graphic)
        self.context['components'].append(new_graphic)

    def _remove_graphic(self):
        selection = self.graphic_list.get_selected()[0]
        self.graphic_list.items.remove(selection)
        self.graphics.remove(selection.component)

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
        return self.image

    def _activate_controls(self):
        selection = self.graphic_list.get_selected()
        ani_selection = self.ani_list.get_selected()
        if self.image is not None:
            self.add_button.sensitive = True
        else:
            self.add_button.sensitive = False

        if len(selection) > 0:
            self.update_button.sensitive = True
            self.remove_button.sensitive = True
            self.add_ani_button.sensitive = True
        else:
            self.update_button.sensitive = False
            self.remove_button.sensitive = False
            self.add_ani_button.sensitive = False

        if len(ani_selection) > 0:
            self.remove_ani_button.sensitive = True
        else:
            self.remove_ani_button.sensitive = False
            

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

