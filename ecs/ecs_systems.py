import math

from pavouk_ecs.system import System

import settings.settings as set
from ecs.ecs_components import *


class MouseControlSystem(System):
    def on_update(self, surface, deltatime, events):
        difference_x = pg.mouse.get_pos()[0] - set.HALF_WIDTH
        difference_y = pg.mouse.get_pos()[1] - set.HALF_HEIGHT

        for entity in self.manager.query([AngleComponent,
                                          SensitivityComponent,
                                          PitchComponent]):

            ang = self.manager.get(AngleComponent, entity)
            sen = self.manager.get(SensitivityComponent, entity)
            pit = self.manager.get(PitchComponent, entity)

            ang.angle += difference_x * sen.sensitivity

            if pit.pitch >= -530:
                pit.pitch -= difference_y
            elif difference_y <= 0:
                pit.pitch -= difference_y

            print(ang.angle, math.pi / 4)


class GravitationSystem(System):
    def on_update(self, surface, deltatime, events):
        pressed_key = pg.key.get_pressed()

        for entity in self.manager.query([PositionComponent,
                                          GravitationForceComponent,
                                          HeightComponent,
                                          JumpVelocity,
                                          MapComponent,
                                          JumpFlagComponent]):

            pos = self.manager.get(PositionComponent, entity)
            gr = self.manager.get(GravitationForceComponent, entity).gravitation
            hei = self.manager.get(HeightComponent, entity)
            jv = self.manager.get(JumpVelocity, entity)
            m = self.manager.get(MapComponent, entity).map
            height_map_array_3d = self.manager.get(HeightMapArray3DComponent, m).height_map_array_3d
            jf = self.manager.get(JumpFlagComponent, entity)
            vel = self.manager.get(VelocityComponent, entity)

            if pressed_key[pg.K_SPACE]:
                jf.jump_flag = True

            if jf.jump_flag:
                hei.height = hei.height + jv.jump_velocity
                jv.jump_velocity -= gr
            elif pressed_key[pg.K_LSHIFT]:
                if hei.height > height_map_array_3d[int(pos.position_x), int(pos.position_y)][0] + 10:
                    hei.height -= 2
                else:
                    hei.height = height_map_array_3d[int(pos.position_x), int(pos.position_y)][0] + 10
                vel.velocity = 0.5
            elif hei.height < height_map_array_3d[int(pos.position_x), int(pos.position_y)][0] + 20:
                hei.height += 2
            else:
                hei.height = height_map_array_3d[int(pos.position_x), int(pos.position_y)][0] + 20
                vel.velocity = 2

            if hei.height <= height_map_array_3d[int(pos.position_x), int(pos.position_y)][0] + 20:
                jv.jump_velocity = 7
                jf.jump_flag = False


class KeysControlSystem(System):
    def on_update(self, surface, deltatime, events):
        pressed_key = pg.key.get_pressed()

        for entity in self.manager.query([PositionComponent,
                                          VelocityComponent,
                                          AngleComponent,]):

            pos = self.manager.get(PositionComponent, entity)
            vel = self.manager.get(VelocityComponent, entity)
            ang = self.manager.get(AngleComponent, entity)

            sin_a = math.sin(ang.angle)
            cos_a = math.cos(ang.angle)

            if pressed_key[pg.K_ESCAPE]:
                pass

            if pressed_key[pg.K_w]:
                pos.position_x += vel.velocity * cos_a
                pos.position_y += vel.velocity * sin_a
            if pressed_key[pg.K_s]:
                pos.position_x -= vel.velocity * cos_a
                pos.position_y -= vel.velocity * sin_a
            if pressed_key[pg.K_a]:
                pos.position_x += vel.velocity * sin_a
                pos.position_y -= vel.velocity * cos_a
            if pressed_key[pg.K_d]:
                pos.position_x -= vel.velocity * sin_a
                pos.position_y += vel.velocity * cos_a


class LocatedSystem(System):
    def on_update(self, surface, deltatime, events):
        for entity in self.manager.query([PositionComponent,
                                          MapComponent]):
            pos = self.manager.get(PositionComponent, entity)
            x = pos.position_x
            y = pos.position_y
            m = self.manager.get(MapComponent, entity).map
            mn = self.manager.get(MapNumberComponent, m)

            if int(x) <= 4 or int(x) >= 1020:
                if mn.map_number == 1:
                    mn.map_number = 2
                elif mn.map_number == 2:
                    mn.map_number = 1
                elif mn.map_number == 3:
                    mn.map_number = 4
                elif mn.map_number == 4:
                    mn.map_number = 3
                if int(x) <= 4:
                    pos.position_x = 1019
                else:
                    pos.position_x = 5

            if int(y) <= 4 or int(y) >= 1020:
                if mn.map_number == 1:
                    mn.map_number = 4
                elif mn.map_number == 2:
                    mn.map_number = 3
                elif mn.map_number == 3:
                    mn.map_number = 2
                elif mn.map_number == 4:
                    mn.map_number = 1
                if int(y) <= 4:
                    pos.position_y = 1019
                else:
                    pos.position_y = 5

            if (int(y) <= 4 or int(y) >= 1020) or (int(x) <= 4 or int(x) >= 1020):

                hmi = self.manager.get(HeightMapImageComponent, m)
                hmi.height_map_image = pg.image.load(f'../images/maps/height_maps/maph_{mn.map_number}.png')

                hma = self.manager.get(HeightMapArray3DComponent, m)
                hma.height_map_array_3d = pg.surfarray.array3d(hmi.height_map_image)

                cmi = self.manager.get(ColorMapImageComponent, m)
                cmi.color_map_image = pg.image.load(f'../images/maps/color_maps/map_{mn.map_number}.png')

                cma = self.manager.get(ColorMapArray3DComponent, m)
                cma.color_map_array_3d = pg.surfarray.array3d(cmi.color_map_image)


class FirstPersonWeaponSystem(System):
    def on_update(self, surface, deltatime, events):
        for entity in self.manager.query([WeaponSpriteComponent,
                                          FireFlagComponent]):

            ws = self.manager.get(WeaponSpriteComponent, entity)
            ff = self.manager.get(FireFlagComponent, entity)

            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        ff.fire_flag = True
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        ff.fire_flag = False


            if ff.fire_flag or ws.animation_counter != 0:
                ws.weapon_sprite = ws.weapon_animation[0]
                ws.weapon_animation.rotate()
                ws.animation_counter += 1
            if ws.animation_counter == 13:
                ws.animation_counter = 0

            surface.blit(ws.weapon_sprite, (200, 200))


class EnemySpriteSystem(System):
    def on_update(self, surface, deltatime, events):
        player_pos = None
        player_ang = None

        for entity in self.manager.query([PositionComponent,
                                          PlayerFlagComponent,
                                          AngleComponent]):
            player_pos = self.manager.get(PositionComponent, entity).position
            player_ang = self.manager.get(AngleComponent, entity).angle

        for entity in self.manager.query([PositionComponent,
                                          AngleComponent,
                                          EntitySpriteComponent,
                                          HeightComponent,
                                          AngleComponent,
                                          SpriteScaleComponent,
                                          SpriteShiftComponent]):

            sprite_pos = self.manager.get(PositionComponent, entity).position
            entity_scale = self.manager.get(SpriteScaleComponent, entity).sprite_scale
            sprite_shift = self.manager.get(SpriteShiftComponent, entity).sprite_shift
            entity_sprite = self.manager.get(EntitySpriteComponent, entity).entity_sprite

            dx, dy = sprite_pos[0] - player_pos[0], sprite_pos[1] - player_pos[1]
            distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

            theta = math.atan2(dy, dx)
            gamma = theta - player_ang

            if dx > 0 and 180 <= math.degrees(player_ang) <= 360 or dx < 0 and dy < 0:
                gamma += set.DOUBLE_PI

            delta_rays = int(gamma / set.DELTA_ANGLE)
            current_ray = set.CENTRAL_RAY + delta_rays

            distance_to_sprite *= math.cos(set.HALF_FOV - current_ray * set.DELTA_ANGLE)

            fake_ray = current_ray + set.FAKE_RAYS

            if 0 <= fake_ray <= set.WIDTH - 1 + 2 * set.FAKE_RAYS:
                proj_height = min(int(set.PR_CF / distance_to_sprite * entity_scale), 2 * set.HEIGHT)
                half_proj_height = proj_height // 2
                shift = half_proj_height * sprite_shift

                #НЕЗАБЫТЬ НЕ СТАТИЧНЫЕ СПРАЙТЫ

                sprite_pos = (current_ray, set.HALF_HEIGHT)

                surface.blit(entity_sprite, sprite_pos)


