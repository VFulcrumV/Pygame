import math
from collections import deque

import pygame as pg
import numpy as np
import pavouk_ecs.setup

import ecs.ecs_components as c


pavouk_ecs.setup.MAX_ENTITIES = 1000000


###
### ENTITYS
###


class PlayerEntity:
    def __init__(self, manager):
        self.manager = manager
        self.player = self.manager.create_entity()
        pos = self.manager.assign(c.PositionComponent, self.player)
        pos.position = (15, 15)
        pos.position_x, pos.position_y = pos.position[0], pos.position[1]

        pit = self.manager.assign(c.PitchComponent, self.player)
        pit.pitch = 200

        ang = self.manager.assign(c.AngleComponent, self.player)
        ang.angle = math.pi / 4

        hei = self.manager.assign(c.HeightComponent, self.player)
        hei.height = 200

        anv = self.manager.assign(c.AngleVelocityComponent, self.player)
        anv.angle_velocity = 0.1

        vel = self.manager.assign(c.VelocityComponent, self.player)
        vel.velocity = 2

        sen = self.manager.assign(c.SensitivityComponent, self.player)
        sen.sensitivity = 0.002

        mi = self.manager.assign(c.MinimapIndicatorComponent, self.player)
        mi.minimap_indicator = pg.image.load(f'../images/player_minimap_indicator/player_1.png')

        jf = self.manager.assign(c.JumpFlagComponent, self.player)
        jf.jump_flag = False

        gr = self.manager.assign(c.GravitationForceComponent, self.player)
        gr.gravitation = 0.7

        jv = self.manager.assign(c.JumpVelocity, self.player)
        jv.jump_velocity = 7

        ws = self.manager.assign(c.WeaponSpriteComponent, self.player)
        ws.weapon_sprite = pg.image.load(f'../images/sprites/ak_47/animation/0.png')
        ws.weapon_sprite_base = pg.image.load(f'../images/sprites/ak_47/base/0.png')
        ws.weapon_animation = deque(
            [pg.image.load(f'../images/sprites/ak_47/animation/{i}.png').convert_alpha() for i in range(24, -1, -2)]
        )

        ff = self.manager.assign(c.FireFlagComponent, self.player)

        m = self.manager.assign(c.MapComponent, self.player)
        m.map = MapEntity(manager).map


class MapEntity:
    def __init__(self, manager):
        self.manager = manager
        self.map = self.manager.create_entity()

        mn = self.manager.assign(c.MapNumberComponent, self.map)
        mn.map_number = 1

        hmi = self.manager.assign(c.HeightMapImageComponent, self.map)
        hmi.height_map_image = pg.image.load(f'../images/maps/height_maps/maph_{mn.map_number}.png')

        hma = self.manager.assign(c.HeightMapArray3DComponent, self.map)
        hma.height_map_array_3d = pg.surfarray.array3d(hmi.height_map_image)

        cmi = self.manager.assign(c.ColorMapImageComponent, self.map)
        cmi.color_map_image = pg.image.load(f'../images/maps/color_maps/map_{mn.map_number}.png')

        cma = self.manager.assign(c.ColorMapArray3DComponent, self.map)
        cma.color_map_array_3d = pg.surfarray.array3d(cmi.color_map_image)

        mh = self.manager.assign(c.MapHeightComponent, self.map)
        mh.map_height = len(hma.height_map_array_3d[0])

        mw = self.manager.assign(c.MapWidthComponent, self.map)
        mw.map_width = len(hma.height_map_array_3d)
