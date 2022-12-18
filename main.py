import math

import pygame as pg

from player import Player
from voxel_render import VoxelRender
import settings
from field import Map


class App:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.size = self.width, self.height = (settings.WIDTH, settings.HEIGHT)
        self.screen = pg.display.set_mode(self.size, pg.SCALED)
        self.clock = pg.time.Clock()
        self.map = Map()
        self.player = Player(self.map)
        self.voxel_render = VoxelRender(self, self.map)
        self.font = pg.font.SysFont('Arial', 15, bold=True)

    def update(self):
        self.player.update()
        self.voxel_render.update()

    def draw(self):
        self.voxel_render.draw()
        self.fps(self.clock)
        self.config()
        self.mini_map()
        pg.display.flip()

    def mini_map(self):
        mini_map = self.map.color_map_img
        scale_player_pos = (self.player.pos[0] // 10, self.player.pos[1] // 10)
        scale_map = pg.transform.scale(mini_map, (
            mini_map.get_width() // 10,
            mini_map.get_height() // 10))

        player_mini = self.player.mini_map_ind
        player_scale = pg.transform.scale(player_mini,
                                          (player_mini.get_width() // 80,
                                           player_mini.get_height() // 80))
        player_scale = pg.transform.rotate(player_scale, 90 + (-180 * (self.player.angle) / math.pi))

        scale_map.blit(player_scale,
                       (scale_player_pos[0] - player_scale.get_width() * 0.5,
                        scale_player_pos[1] - player_scale.get_width() * 0.5))
        self.screen.blit(scale_map, (0, settings.HEIGHT - scale_map.get_height()))


    def config(self):
        config = pg.image.load('images//config.png')
        config.set_colorkey((255, 255, 255))
        scale = pg.transform.rotate(config, 180)
        scale = pg.transform.scale(scale, (
            config.get_width() // 100,
            config.get_height() // 100
        ))
        scale_rect = scale.get_rect(center=(settings.WIDTH // 2 - scale.get_width() // 2,
                                            settings.HEIGHT // 2 - scale.get_height() // 2))
        self.screen.blit(scale, (scale_rect[0], scale_rect[1]))

    def act_pressed_keys(self, key):
        if 'key' in f'{key}':
            k = int(f'{key}'.split('key')[1].split(',')[0].split(' ')[1])
            if len(str(k)) <= 3:
                k = chr(k)
            if k in ['1', '2', '3', '4'] and int(k) != self.map.number_of_map:
                self.map.number_of_map = int(k)
                self.map.change_map()
            if pg.key.get_pressed()[pg.K_r]:
                app = App()
                app.run()


    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render_fps = self.font.render(display_fps, True, 'green')
        pos = int(self.player.pos[0]), int(self.player.pos[1])
        render_height = self.font.render(str(f'{self.player.height} {pos}'), True, 'blue')
        self.screen.blit(render_fps, (10, 5))
        self.screen.blit(render_height, (10, 20))

    def run(self):
        while True:
            [self.act_pressed_keys(event) for event in pg.event.get()]
            if pg.key.get_pressed()[pg.K_SPACE] and self.player.main_space_flag:
                self.player.main_space_flag = True

            self.update()
            self.draw()

            [self.act_pressed_keys(event) for event in pg.event.get()]
            if pg.key.get_pressed()[pg.K_SPACE] and not self.player.main_space_flag:
                self.player.main_space_flag = True

            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
