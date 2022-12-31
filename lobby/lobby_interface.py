from random import randrange

import pygame as pg

import settings.settings as settings


class Button:
    def __init__(self, screen, text=str(), colors=tuple(), size=(0.2, 0.2), position=(1, 1)):

        self.screen = screen
        self.text = text
        self.colors = colors
        self.size = size
        self.position = position

        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_click = pg.mouse.get_pressed()

        self.button_font = pg.font.SysFont('Arial', 30, bold=True)
        self.button = self.button_font.render(self.text, 1, pg.Color(self.colors[0]))
        self.button_rect = pg.Rect(0, 0, settings.LOBBY_WIDTH * self.size[0], settings.LOBBY_HEIGHT * self.size[1])
        self.button_rect.center = settings.WIDTH * self.position[0], settings.HEIGHT * self.position[1]

    def draw(self):
        self.mouse_pos = pg.mouse.get_pos()
        if self.button_rect.collidepoint(self.mouse_pos):
            color = self.colors[1]
        else:
            color = self.colors[0]

        pg.draw.rect(self.screen, color, self.button_rect, border_radius=10, width=2)
        self.button = self.button_font.render(self.text, 1, pg.Color(color))
        self.screen.blit(self.button, (self.button_rect.centerx - self.button.get_width() * 0.5,
                                       self.button_rect.centery - self.button.get_height() * 0.5))
        return self.mouse_pos, self.mouse_click

    def tap(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_click = pg.mouse.get_pressed()
        if self.button_rect.collidepoint(self.mouse_pos):
            if self.mouse_click[0]:
                return True
        return False


class Label:
    def __init__(self, screen, text=str(), color=tuple(), size=int(), position=(1, 1)):

        self.label_font = pg.font.SysFont('Arial', size, bold=True)

        self.screen = screen
        self.text = text
        if color[0] == 'random':
            self.color = ('random', (None))
        else:
            self.color = color
        self.size = size
        self.position = position
        self.label_rect = pg.Rect(0, 0, 1, 1)
        self.label_rect.center = settings.WIDTH * self.position[0], settings.HEIGHT * self.position[1]

    def draw(self):
        if self.color[0] != 'random':
            color = self.color
        else:
            color = (randrange(200), randrange(200), randrange(200))
        self.label = self.label_font.render(self.text, 1, color)
        self.screen.blit(self.label, (self.label_rect.centerx - self.label.get_width() * 0.5,
                                      self.label_rect.centery - self.label.get_height() * 0.5))


class Background:
    def __init__(self,screen, filename):
        self.x = 0
        self.screen = screen
        self.menu_background = pg.image.load(filename).convert()

    def draw(self):
        self.screen.blit(self.menu_background, (0, 0), (self.x % settings.WIDTH, settings.HEIGHT,
                                                        settings.LOBBY_WIDTH, settings.LOBBY_HEIGHT))
        self.x += 1
