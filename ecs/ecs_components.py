from dataclasses import dataclass
from collections import deque

import pygame as pg
import numpy as np

from ecs.ecs_entitys import MapEntity


###
### COMPONENTS
###

@dataclass
class PositionComponent:
    position: tuple = None
    position_x: float = None
    position_y: float = None


@dataclass
class PitchComponent:
    pitch: int = 0


@dataclass
class AngleComponent:
    angle: float = 0


@dataclass
class HeightComponent:
    height: int = 0


@dataclass
class JumpVelocity:
    Jump_velocity: int = 0


@dataclass
class AngleVelocityComponent:
    angle_velocity: float = 0


@dataclass
class VelocityComponent:
    velocity: int = 0


@dataclass
class GravitationForceComponent:
    gravitation: int = 0


@dataclass
class SensitivityComponent:
    sensitivity: float = 0


@dataclass
class MinimapIndicatorComponent:
    minimap_indicator: pg.image = None


@dataclass
class JumpFlagComponent:
    jump_flag: bool = False


@dataclass
class MapComponent:
    map_entity: MapEntity = None
    map: map = None


@dataclass
class MapNumberComponent:
    map_number: int = 1


@dataclass
class HeightMapImageComponent:
    height_map_image: pg.image = None


@dataclass
class HeightMapArray3DComponent:
    height_map_array_3d: pg.surfarray.array3d = None


@dataclass
class ColorMapImageComponent:
    color_map_image: pg.image = None


@dataclass
class ColorMapArray3DComponent:
    color_map_array3d: pg.surfarray.array3d = None


@dataclass
class MapHeightComponent:
    map_height: int = 0


@dataclass
class MapWidthComponent:
    map_width: int = 0


@dataclass
class WeaponSpriteComponent:
    weapon_sprite: pg.image = None
    weapon_sprite_base: pg.image = None
    weapon_animation: deque = None
    animation_counter: int = 0


@dataclass
class FireFlagComponent:
    fire_flag: bool = False