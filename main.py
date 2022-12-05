import pygame as pg

from player import Player
from voxel_render import VoxelRender
import settings


class App:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.size = self.width, self.height = (settings.WIDTH, settings.HEIGHT)
        self.screen = pg.display.set_mode(self.size, pg.SCALED)
        self.clock = pg.time.Clock()
        self.player = Player()
        self.voxel_render = VoxelRender(self)
        self.font = pg.font.SysFont('Arial', 15, bold=True)

    def update(self):
        self.player.update()
        self.voxel_render.update()

    def draw(self):
        self.voxel_render.draw()
        self.fps(self.clock)
        self.config()
        pg.display.flip()

    def config(self):
        config = pg.image.load('images//config.png')
        config.set_colorkey((255, 255, 255))
        scale = pg.transform.rotate(config, 180)
        scale = pg.transform.scale(scale, (
            config.get_width() // 100,
            config.get_height() // 100
        ))
        scale_rect = scale.get_rect(center=(settings.WIDTH // 2 - scale.get_width() // 2,
                                            settings.HEIGHT // 2 - scale.get_height() // 2))
        self.screen.blit(scale, (scale_rect[0], scale_rect[1]))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render_fps = self.font.render(display_fps, True, 'green')
        render_height = self.font.render(str(self.player.height), True, 'blue')
        self.screen.blit(render_fps, (10, 5))
        self.screen.blit(render_height, (10, 20))

    def run(self):
        while True:
            self.update()
            self.draw()

            [exit() for event in pg.event.get() if event.type == pg.QUIT]

            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
