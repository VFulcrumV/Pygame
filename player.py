import math
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

import pygame as pg
import numpy as np
from pyautogui import moveTo

import settings


class Player:
    def __init__(self, map):
        self.pos = np.array([5, 5], dtype=float)
        self.angle = math.pi / 4
        self.height = 270
        self.pitch = 200
        self.angle_velocity = 0.1
        self.velocity = 2
        self.sensetivity = 0.002

        self.mini_map_ind = pg.image.load(f'images/player_1.png')
        self.map = map
        self.map_located = [0, 0]

        self.main_space_flag = False
        self.jump_flag = 0
        self.jump_coords = iter(range(12, 0, -1))

    def update(self):
        if (int(self.pos[0]) <= 4 or int(self.pos[0]) >= 1020) or (int(self.pos[1]) <= 4 or int(self.pos[1]) >= 1020):
            self.located()
        self.keys_control()
        self.mouse_control()

    def located(self):
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
            exit()

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
                if self.jump_flag == 0:
                    self.height += int(next(self.jump_coords) * 0.5)
                else:
                    self.height -= int(next(self.jump_coords) * 1.5)
        except StopIteration:
            if self.jump_flag == 0:
                difference_height = self.map.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20 - self.height
                try:
                    jump_down = int((-1 + math.sqrt(1 + 2 * (-difference_height))))
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        self.jump_coords = list(range(1, jump_down))
                    else:
                        self.jump_coords = list(range(1, jump_down)) + [2, 2, 1]
                    self.jump_coords = iter(self.jump_coords)
                    self.jump_flag = 1
                except ValueError:
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        pass
                    else:
                        self.height = self.map.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20
                finally:
                    pass

            else:
                self.jump_flag = 0
                self.jump_coords = iter(range(12, 0, -1))
                self.height = self.map.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20
                self.main_space_flag = False
        finally:
            pass

    def mouse_control(self):
        if pg.mouse.get_focused() :
            difference_x = pg.mouse.get_pos()[0] - settings.HALF_WIDTH
            difference_y = pg.mouse.get_pos()[1] - settings.HALF_HEIGHT
            pg.mouse.set_pos((settings.HALF_WIDTH, settings.HALF_HEIGHT))
            self.angle += difference_x * self.sensetivity
            if self.pitch >= -530:
                self.pitch -= difference_y
            elif difference_y <= 0:
                self.pitch -= difference_y
        else:
            window_x, window_y = self.get_window_coords()
            try:
                moveTo(window_x + settings.HALF_WIDTH + pg.SCALED, window_y + settings.HALF_HEIGHT + pg.SCALED // 2)
            except Exception:
                pass
            finally:
                pass

    def get_window_coords(self):
        hwnd = pg.display.get_wm_info()['window']
        prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
        paramflags = (1, 'hwnd'), (2, 'lprect')

        GetWindowRect = prototype(('GetWindowRect', windll.user32), paramflags)

        rect = GetWindowRect(hwnd)
        return rect.top, rect.left
