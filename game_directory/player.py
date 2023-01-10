import math

import pygame as pg
import numpy as np

import settings.settings as settings


class Player:
    def __init__(self, map):
        self.x, self.y = self.pos = np.array([5, 5], dtype=float)
        self.angle = math.pi / 4
        self.height = 0
        self.pitch = 200
        self.angle_velocity = 0.1
        self.velocity = 2
        self.sensitivity = 0.002

        self.mini_map_ind = pg.image.load(f'../images/player_minimap_indicator/player.png')
        self.map = map
        self.map_located = np.array([0, 0], dtype=int)

        self.main_space_flag = False
        self.jump_flag = False
        self.jump_cords = iter(range(15, 0, -1))

    def update(self):
        self.located()
        self.keys_control()
        self.mouse_control()

    def located(self):
        if (int(self.pos[0]) <= 4 or int(self.pos[0]) >= 1020) or (int(self.pos[1]) <= 4 or int(self.pos[1]) >= 1020):
            if int(self.pos[1]) >= 1020:
                self.map_located[1] = (self.map_located[1] + 1) % 2
                self.pos[1] = 5
            elif int(self.pos[1]) <= 4:
                self.map_located[1] = (self.map_located[1] + 1) % 2
                self.pos[1] = 1019
            elif int(self.pos[0]) >= 1020:
                self.map_located[0] = (self.map_located[0] + 1) % 2
                self.pos[0] = 5
            elif int(self.pos[0]) <= 4:
                self.map_located[0] = (self.map_located[0] + 1) % 2
                self.pos[0] = 1019
            self.go_to_another_map()

    def go_to_another_map(self):
        if self.map_located == [0, 0]:
            self.map.number_of_map = 1
            self.map.change_map()
        elif self.map_located == [0, 1]:
            self.map.number_of_map = 2
            self.map.change_map()
        elif self.map_located == [1, 1]:
            self.map.number_of_map = 3
            self.map.change_map()
        elif self.map_located == [1, 0]:
            self.map.number_of_map = 4
            self.map.change_map()

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        x = self.pos[0]
        y = self.pos[1]

        pressed_key = pg.key.get_pressed()

        if pressed_key[pg.K_ESCAPE]:
            pass

        if pressed_key[pg.K_SPACE] or self.main_space_flag:
            if pressed_key[pg.K_LSHIFT]:
                self.velocity = 0.5
            else:
                self.velocity = 2
            self.space_control()
        elif pressed_key[pg.K_LSHIFT] and self.height == self.map.height_map[int(x), int(y)][0] + 20:
            self.height = self.map.height_map[int(x), int(y)][0] + 20
            self.height += 10
            self.velocity = 0.5
        elif pressed_key[pg.K_LSHIFT] and self.height != self.map.height_map[int(x), int(y)][0] + 20:
            self.height = self.map.height_map[int(x), int(y)][0] + 10
            self.velocity = 0.5
        else:
            self.height = self.map.height_map[int(x), int(y)][0] + 20
            self.velocity = 2

        if pressed_key[pg.K_w]:
            self.pos[0] += self.velocity * cos_a
            self.pos[1] += self.velocity * sin_a
        if pressed_key[pg.K_s]:
            self.pos[0] -= self.velocity * cos_a
            self.pos[1] -= self.velocity * sin_a
        if pressed_key[pg.K_a]:
            self.pos[0] += self.velocity * sin_a
            self.pos[1] -= self.velocity * cos_a
        if pressed_key[pg.K_d]:
            self.pos[0] -= self.velocity * sin_a
            self.pos[1] += self.velocity * cos_a


    def space_control(self):
        try:
            if self.main_space_flag:
                if not self.jump_flag:
                    self.height += int(next(self.jump_cords) * 0.5)
                else:
                    self.height -= int(next(self.jump_cords) * 1.5)
        except StopIteration:
            if not self.jump_flag:
                difference_height = self.map.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20 - self.height
                try:
                    jump_down = int((-1 + math.sqrt(1 + 2 * (-difference_height))))
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        self.jump_cords = list(range(1, jump_down))
                    else:
                        self.jump_cords = list(range(1, jump_down)) + [2, 2, 1]
                    self.jump_cords = iter(self.jump_cords)
                    self.jump_flag = True
                except ValueError:
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        pass
                    else:
                        self.height = self.map.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20
                finally:
                    pass

            else:
                self.jump_flag = False
                self.jump_cords = iter(range(15, 0, -1))
                self.height = self.map.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20
                self.main_space_flag = False

    def mouse_control(self):
        difference_x = pg.mouse.get_pos()[0] - settings.HALF_WIDTH
        difference_y = pg.mouse.get_pos()[1] - settings.HALF_HEIGHT
        self.angle += difference_x * self.sensitivity
        if self.pitch >= -530:
            self.pitch -= difference_y
        elif difference_y <= 0:
            self.pitch -= difference_y
print()