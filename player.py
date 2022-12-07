import math
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

import pygame as pg
import numpy as np
from pyautogui import moveTo

import voxel_render as vr
import settings


class Player:
    def __init__(self):
        self.pos = np.array([50, 50], dtype=float)
        self.angle = math.pi / 4
        self.height = 270
        self.pitch = 200
        self.angle_velocity = 0.1
        self.velocity = 2
        self.sensetivity = 0.002

        self.main_space_flag = False
        self.jump_flag = 0
        self.jump_coords = iter(range(7, 0, -1))

    def update(self):
        self.keys_control()
        self.mouse_control()

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        x = self.pos[0]
        y = self.pos[1]

        pressed_key = pg.key.get_pressed()

        if pressed_key[pg.K_ESCAPE]:
            exit()

        if 0 < x and len(vr.height_map) > x and 0 < y and len(vr.height_map) > y:

            if pressed_key[pg.K_SPACE] or self.main_space_flag:
                if pressed_key[pg.K_LSHIFT]:
                    self.velocity = 0.5
                else:
                    self.velocity = 2
                self.space_control()
            elif pressed_key[pg.K_LSHIFT] and self.height == vr.height_map[int(x), int(y)][0] + 20:
                self.height = vr.height_map[int(x), int(y)][0] + 20
                self.height += 10
                self.velocity = 0.5
            elif pressed_key[pg.K_LSHIFT] and self.height != vr.height_map[int(x), int(y)][0] + 20:
                self.height = vr.height_map[int(x), int(y)][0] + 20
                self.height -= 10
                self.velocity = 0.5
            else:
                self.height = vr.height_map[int(x), int(y)][0] + 20
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
                    self.height += next(self.jump_coords)
                else:
                    self.height -= next(self.jump_coords)
        except StopIteration:
            if self.jump_flag == 0:
                difference_height = vr.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20 - self.height
                last_jump_minus = (-1 + math.sqrt(1 + 2 * (-difference_height)))
                self.jump_coords = iter(range(1, int(last_jump_minus)))
                self.jump_flag = 1
            else:
                self.jump_flag = 0
                self.jump_coords = iter(range(7, 0, -1))
                self.height = vr.height_map[int(self.pos[0]), int(self.pos[1])][0] + 20
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
