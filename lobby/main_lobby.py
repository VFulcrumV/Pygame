import sys

import pygame as pg

import settings.settings as settings
from lobby import lobby_interface


class MainLobby:
    def __init__(self, client, server):
        self.interface()

        self.client = client
        self.server = server

        self.lobby_run = True
        self.answer = ''

    def interface(self):
        pg.init()
        pg.mouse.set_visible(True)
        self.size = self.width, self.height = (settings.LOBBY_WIDTH, settings.LOBBY_HEIGHT)
        self.screen = pg.display.set_mode(self.size, pg.SCALED)
        self.clock = pg.time.Clock()

        self.start_button = lobby_interface.Button(self.screen, 'START',
                                                   ('lightgray', 'green'), (0.2, 0.15), (1, 0.85))
        self.settings_button = lobby_interface.Button(self.screen, 'SETTINGS',
                                                      ('lightgray', 'green'), (0.2, 0.15), (1, 1.16))
        self.statistic_button = lobby_interface.Button(self.screen, 'STATISTIC',
                                                       ('lightgray', 'green'), (0.2, 0.15), (1, 1.47))
        self.exit_button = lobby_interface.Button(self.screen, 'EXIT',
                                                  ('lightgray', 'red'), (0.2, 0.15), (1, 1.78))

        self.background = lobby_interface.Background(self.screen, 'images/background/menu.png')

        self.present_label = lobby_interface.Label(self.screen, 'HAHA GUN MAKES PEW-PEW!', ['random'], 100, (1, 0.3))

        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_click = pg.mouse.get_pressed()

    def draw(self):
        self.background.draw()

        self.start_button.draw()
        self.settings_button.draw()
        self.statistic_button.draw()
        self.exit_button.draw()

        self.present_label.draw()

        pg.display.flip()

    def response_pressed_keys(self, event):
        if self.start_button.tap():
            self.lobby_run = False
            self.answer = 'server'
        if self.settings_button.tap():
            self.lobby_run = False
            self.answer = 'client'
        if self.statistic_button.tap():
            pass
        if self.exit_button.tap():
            pg.quit()
            sys.exit()

    def run(self):
        while self.lobby_run:
            [self.response_pressed_keys(event) for event in pg.event.get()]

            self.draw()

            pg.display.flip()
            self.clock.tick(60)
        return self.answer
