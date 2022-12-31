import pygame as pg

import game.player as player
import game.voxel_render as voxel_render
import settings.settings as settings
import game.field as field
import game.game_interface as game_interface


class Game:
    def __init__(self, client):
        pg.init()
        pg.mouse.set_visible(False)
        self.size = self.width, self.height = (settings.WIDTH, settings.HEIGHT)

        self.map = field.Map()
        self.player = player.Player(self.map)
        self.screen = pg.display.set_mode(self.size, pg.SCALED)

        self.game_interface = game_interface.GameInterface(self.map, self.player, self.screen)

        self.voxel_render = voxel_render.VoxelRender(self, self.map)

        self.clock = pg.time.Clock()

        self.answer = ''
        self.game_run = True

        self.client = client

        self.player_data = []
        self.client_return = None

    def update(self):
        self.player.update()
        self.voxel_render.update()
        self.game_interface.update_mouse()

    def draw(self):
        self.voxel_render.draw()
        self.game_interface.draw_fps(self.clock)
        self.game_interface.draw_config()
        self.game_interface.draw_mini_map()
        pg.display.flip()

    def response_pressed_keys(self, event):
        self.answer = self.game_interface.response_pressed_keys(event)
        if self.answer == 'lobby':
            self.game_run = False

    def add_data_to_server(self):
        self.player_data.append((self.player.pos[0] // 10, self.player.pos[1] // 10))

    def run(self):
        while self.game_run:

            [self.response_pressed_keys(event) for event in pg.event.get()]
            if pg.key.get_pressed()[pg.K_SPACE] and self.player.main_space_flag:
                self.player.main_space_flag = True

            self.update()
            self.draw()
            self.add_data_to_server()

            if self.client is not None:
                if self.client.connected:
                    self.client.listen(self.player_data)
                else:
                    self.client.connect()

            if self.client.client_return is not None:
                print(self.client.client_return)

            [self.response_pressed_keys(event) for event in pg.event.get()]
            if pg.key.get_pressed()[pg.K_SPACE] and not self.player.main_space_flag:
                self.player.main_space_flag = True

            self.client_return = []
            self.player_data = []

            self.clock.tick(60)
        return self.answer