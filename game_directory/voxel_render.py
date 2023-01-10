import math

from numba import njit
import numpy as np

from ecs.ecs_components import *


class VoxelRender:
    def __init__(self, game, manager):
        self.app = game
        self.player = game.player
        self.map = game.map
        self.manager = manager
        self.fov = math.pi / 3
        self.height_fov = self.fov / 2
        self.num_rays = game.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 1500
        self.scale_height = 500
        self.screen_array = np.full((game.width, game.height, 3), (0, 0, 0))

    def update(self):
        pos = self.manager.get(PositionComponent, self.player)
        ang = self.manager.get(AngleComponent, self.player)
        hei = self.manager.get(HeightComponent, self.player)
        pit = self.manager.get(PitchComponent, self.player)
        m = self.manager.get(MapComponent, self.player).map

        map_height = self.manager.get(MapHeightComponent, m).map_height
        map_width  = self.manager.get(MapWidthComponent, m).map_width
        height_map = self.manager.get(HeightMapArray3DComponent, m).height_map_array_3d
        color_map = self.manager.get(ColorMapArray3DComponent, m).color_map_array_3d

        self.screen_array = ray_casting(self.screen_array, pos.position_x, pos.position_y, ang.angle,
                                        hei.height, pit.pitch, self.app.width,
                                        self.app.height, self.delta_angle, self.ray_distance,
                                        self.height_fov, self.scale_height,
                                        (map_height, map_width, height_map,
                                         color_map))

    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0, 0))


@njit(fastmath=True)
def ray_casting(screen_array, player_pos_x, player_pos_y, player_angle, player_height, player_pitch, screen_width,
                screen_height, delta_angle, ray_distance, height_fov, scale_height, map):

    screen_array[:] = np.array([0, 0, 0])
    height_buffer = np.full(screen_width, screen_height)

    ray_angle = player_angle - height_fov
    for num_ray in range(screen_width):
        first_contact = False
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_pos_x + depth * cos_a)
            if 0 < x < map[1]:
                y = int(player_pos_y + depth * sin_a)
                if 0 < y < map[0]:

                    #remove fish eye and get height on screen
                    depth *= math.cos(player_angle - ray_angle)
                    height_on_screen = int((player_height - map[2][x, y][0] + 5) / depth * scale_height + player_pitch)

                    #remove unnecessary drawing
                    if not first_contact:
                        height_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True

                    #remove mirror bag
                    if height_on_screen < 0:
                         height_on_screen = 0

                    #draw vert line
                    if height_on_screen < height_buffer[num_ray]:
                        for screen_y in range(height_on_screen, height_buffer[num_ray]):
                            screen_array[num_ray, screen_y] = map[3][x, y]
                        height_buffer[num_ray] = height_on_screen

        ray_angle += delta_angle

    return screen_array
