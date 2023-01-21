import math

import pygame as pg

import settings.settings as settings
from ecs.ecs_components import *


class GameInterface:
    def __init__(self, map, player, screen, manager):
        self.map = map
        self.player = player
        self.screen = screen
        self.manager = manager
        self.answer = None

        self.image_of_config = self.load_config()

        self.font = pg.font.SysFont('Arial', 15, bold=True)

    def draw_mini_map(self):
        pos = self.manager.get(PositionComponent, self.player)
        ind = self.manager.get(MinimapIndicatorComponent, self.player)
        ang = self.manager.get(AngleComponent, self.player)

        mini_map = self.manager.get(ColorMapImageComponent, self.map).color_map_image
        scale_player_pos = (pos.position_x // 10, pos.position_y // 10)
        scale_map = pg.transform.scale(mini_map, (
            mini_map.get_width() // 10,
            mini_map.get_height() // 10))

        player_mini = ind.minimap_indicator
        player_scale = pg.transform.scale(player_mini,
                                          (player_mini.get_width() // 80,
                                           player_mini.get_height() // 80))
        player_scale = pg.transform.rotate(player_scale, 90 + (-180 * (ang.angle) / math.pi))

        scale_map.blit(player_scale,
                       (scale_player_pos[0] - player_scale.get_width() * 0.5,
                        scale_player_pos[1] - player_scale.get_width() * 0.5))
        self.screen.blit(scale_map, (0, settings.HEIGHT - scale_map.get_height()))

    def draw_config(self):
        self.screen.blit(self.image_of_config[0], (self.image_of_config[1][0], self.image_of_config[1][1]))

    @staticmethod
    def load_config():
        config = pg.image.load('images/config/config.png')
        config.set_colorkey((255, 255, 255))
        scale = pg.transform.rotate(config, 180)
        scale = pg.transform.scale(scale, (
            config.get_width() // 100,
            config.get_height() // 100
        ))
        scale_rect = scale.get_rect(center=(settings.WIDTH // 2,
                                            settings.HEIGHT // 2))

        return scale, scale_rect

    def draw_weapon(self):
        ws = self.manager.get(WeaponSpriteComponent, self.player)
        ws.weapon_sprite.set_colorkey((255, 255, 255))
        self.screen.blit(ws.weapon_sprite, (0, 0))

    def draw_fps(self, clock):
        pos = self.manager.get(PositionComponent, self.player)
        hei = self.manager.get(HeightComponent, self.player)
        pitch = self.manager.get(PitchComponent, self.player)

        display_fps = str(int(clock.get_fps()))
        render_fps = self.font.render(display_fps, True, 'green')
        render_height = self.font.render(str(f'{int(hei.height)} {int(pos.position_x), int(pos.position_y)}'), True, 'blue')
        render_pitch = self.font.render(str(f'{pitch.pitch}'), True, 'red')
        self.screen.blit(render_fps, (10, 5))
        self.screen.blit(render_height, (10, 20))
        self.screen.blit(render_pitch, (10, 35))

    def response_pressed_keys(self):
        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_ESCAPE]:
            self.answer = 'lobby'
        return self.answer
