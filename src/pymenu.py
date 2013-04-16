import pygame
import math

class Menu:
    """Menu class returns an interactive text-based menu 
        drawn on a dynamic surface"""

    def __init__(self, image_name, style, items=None, header=None, selected=0):
        self.image_name     = image_name
        self.items          = items if not items == None else list()
        self.header         = header
        self.selected       = selected
        self.style          = style
        self.image          = None
        self.surface        = None
        self.rendered_items = list()

        self.image = pygame.image.load(self.image_name)


    def render_menu(self):
        width  = 0
        height = 0
        self.rendered_items = list() # clear rendered items

        # render the items and store them
        # start with the header
        if self.header is not None:
            divider = '' + ('-' * len(self.header))
            rendered_header = self.style.h_font.render(
                self.header, True, self.style.h_color)
            rendered_divider = self.style.h_font.render(
                divider, True, self.style.h_color)
            width = rendered_header.get_width()
            height += rendered_header.get_height() + rendered_divider.get_height()
            self.rendered_items.append(rendered_header)
            self.rendered_items.append(rendered_divider)
        for index in range(len(self.items)):
            if index == self.selected:
                rendered_item = self.style.s_font.render(
                    self.items[index], True, self.style.s_color)
            else:
                rendered_item = self.style.n_font.render(
                    self.items[index], True, self.style.n_color)
            self.rendered_items.append(rendered_item)
            this_width = rendered_item.get_width()
            width = this_width if this_width > width else width
            height += rendered_item.get_height()

        # calculate dimensions for rendered surface
        i = int(math.ceil(height / self.style.c_rect.height))
        j = int(math.ceil(width / self.style.c_rect.width))
        surface_width = j * self.style.c_rect.width + self.style.l_rect.width + self.style.r_rect.width
        surface_height = i * self.style.c_rect.height + self.style.t_rect.height + self.style.b_rect.height

        # create and render the surface
        self.surface = pygame.Surface((surface_width, surface_height))
        self.surface.blit(self.image, (0,0), self.style.tl_rect) 
        for x in range(0, j):
            self.surface.blit(self.image, (x * self.style.c_rect.width + self.style.tl_rect.width, 0), self.style.t_rect)
        self.surface.blit(self.image, (j * self.style.c_rect.width + self.style.tl_rect.width, 0), self.style.tr_rect)
        for y in range(0, i):
            self.surface.blit(self.image, (0, y * self.style.c_rect.height + self.style.t_rect.height), self.style.l_rect)
            for x in range(0, j):
                self.surface.blit(self.image, 
                    (x * self.style.c_rect.width + self.style.l_rect.width, 
                    y * self.style.c_rect.height + self.style.t_rect.height), self.style.c_rect)
            self.surface.blit(self.image, 
                (j * self.style.c_rect.width + self.style.l_rect.width, 
                y * self.style.c_rect.height + self.style.t_rect.height), self.style.r_rect)
        self.surface.blit(self.image, (0, i * self.style.c_rect.height + self.style.t_rect.height), self.style.bl_rect)
        for x in range(0, j):
            self.surface.blit(self.image, 
                (x * self.style.b_rect.width + self.style.l_rect.width, 
                i * self.style.c_rect.height + self.style.t_rect.height), self.style.b_rect)
        self.surface.blit(self.image, 
            (j * self.style.c_rect.width + self.style.bl_rect.width, 
            i * self.style.c_rect.height + self.style.t_rect.height), self.style.br_rect)

        # draw the items on the surface
        y_offset = self.style.t_rect.height
        for item in self.rendered_items:
            x_offset = (self.surface.get_width() - item.get_width()) / 2
            self.surface.blit(item, (x_offset, y_offset))
            y_offset += item.get_height()

        return self.surface

    def move_selected(self, up=False):
        if up:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.items) - 1
        else:
            self.selected += 1
            if self.selected == len(self.items):
                self.selected = 0


class Item:
    """Item represents one menu item.  An Item's handler property 
        is a callback function which is called when the Item is selected"""

    def __init__(self, text, handler):
        self.text       = text
        self.handler    = handler


class Style:
    """Style defines the fonts and colors used for normal and highlighted 
        menu items"""

    def __init__(self, n_font, n_color, s_font, s_color,
                 tl_rect, tr_rect, bl_rect, br_rect,
                 t_rect, b_rect, l_rect, r_rect, c_rect, h_font=None, h_color=None):

        self.n_font     = n_font
        self.n_color    = n_color
        self.s_font     = s_font
        self.s_color    = s_color
        self.h_font     = h_font
        self.h_color    = h_color
        self.tl_rect    = tl_rect
        self.tr_rect    = tr_rect
        self.bl_rect    = bl_rect
        self.br_rect    = br_rect
        self.t_rect     = t_rect 
        self.b_rect     = b_rect
        self.l_rect     = l_rect
        self.r_rect     = r_rect
        self.c_rect     = c_rect