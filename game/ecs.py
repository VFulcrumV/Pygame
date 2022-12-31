import pygame
import sys

from dataclasses import dataclass
from pavouk_ecs import Manager
from pavouk_ecs.system import System

RESOLUTION = (800, 450)
BACKGROUND_COLOR = (10, 10, 10)


###
### COMPONENTS
###


@dataclass
class Area:
    w: int = 0
    h: int = 0


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0


@dataclass
class Transform:
    x: int = 0
    y: int = 0


@dataclass
class Velocity:
    x: float = 0.0
    y: float = 0.0


###
### SYSTEMS
###


class RenderSystem(System):
    def on_update(self, surface, deltatime):
        for e in self.manager.query([Transform, Area, Color]):
            t = self.manager.get(Transform, e)
            a = self.manager.get(Area, e)
            c = self.manager.get(Color, e)

            r = pygame.Rect(t.x, t.y, a.w, a.h)
            pygame.draw.rect(surface, (c.r, c.g, c.b), r)


class BouncingSystem(System):
    def on_update(self, surface, deltatime):
        for e in self.manager.query([Transform, Area, Velocity]):
            t = self.manager.get(Transform, e)
            a = self.manager.get(Area, e)
            v = self.manager.get(Velocity, e)

            if t.x <= 0 and v.x < 0 or t.x + a.w >= RESOLUTION[0]:
                v.x = -v.x
            if t.y <= 0 and v.y < 0 or t.y + a.h >= RESOLUTION[1]:
                v.y = -v.y

            t.x += v.x
            t.y += v.y
