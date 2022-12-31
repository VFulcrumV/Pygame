from random import randrange

import pygame as pg


class Map():
    def __init__(self):
        self.number_of_map = randrange(1, 5)
        self.height_map_img = pg.image.load(f'../images/maps/height_maps/maph_{self.number_of_map}.png')
        self.height_map = pg.surfarray.array3d(self.height_map_img)

        self.color_map_img = pg.image.load(f'../images/maps/color_maps/map_{self.number_of_map}.png')
        self.color_map = pg.surfarray.array3d(self.color_map_img)

        self.map_height = len(self.height_map[0])
        self.map_width = len(self.height_map)

    def change_map(self):
        self.height_map_img = pg.image.load(f'../images/maps/height_maps/maph_{self.number_of_map}.png')
        self.height_map = pg.surfarray.array3d(self.height_map_img)

        self.color_map_img = pg.image.load(f'../images/maps/color_maps/map_{self.number_of_map}.png')
        self.color_map = pg.surfarray.array3d(self.color_map_img)

        self.map_height = len(self.height_map[0])
        self.map_width = len(self.height_map)
