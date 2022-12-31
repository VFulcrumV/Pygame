import math

import pygame as pg

import settings.settings as settings


class GameInterface:
    def __init__(self, map, player, screen):
        self.map = map
        self.player = player
        self.screen = screen
        self.answer = None

    def draw_mini_map(self):
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

    def draw_config(self):
        config = pg.image.load('../images/config/config.png')
        config.set_colorkey((255, 255, 255))
        scale = pg.transform.rotate(config, 180)
        scale = pg.transform.scale(scale, (
            config.get_width() // 100,
            config.get_height() // 100
        ))
        scale_rect = scale.get_rect(center=(settings.WIDTH // 2 - scale.get_width() // 2,
                                            settings.HEIGHT // 2 - scale.get_height() // 2))
        self.screen.blit(scale, (scale_rect[0], scale_rect[1]))

    def draw_fps(self, clock):
        fps_font = pg.font.SysFont('Arial', 15, bold=True)
        display_fps = str(int(clock.get_fps()))
        render_fps = fps_font.render(display_fps, True, 'green')
        pos = int(self.player.pos[0]), int(self.player.pos[1])
        render_height = fps_font.render(str(f'{self.player.height} {pos}'), True, 'blue')
        self.screen.blit(render_fps, (10, 5))
        self.screen.blit(render_height, (10, 20))

    def response_pressed_keys(self, event):
        if 'key' in f'{event}':
            k = int(f'{event}'.split('key')[1].split(',')[0].split(' ')[1])
            if len(str(k)) <= 3:
                if chr(k) in ['1', '2', '3', '4'] and int(chr(k)) != self.map.number_of_map:
                    self.map.number_of_map = int(chr(k))
                    self.map.change_map()
                if k == pg.K_ESCAPE:
                    self.answer = 'lobby'
        return self.answer

    def update_mouse(self):
        if pg.mouse.get_focused():
            pg.mouse.set_pos((settings.HALF_WIDTH, settings.HALF_HEIGHT))