import game_directory.voxel_render as voxel_render
import settings.settings as settings
import game_directory.game_interface as game_interface

from ecs.ecs_entitys import *
from ecs.ecs_systems import *
from ecs.ecs_components import *
from pavouk_ecs import Manager

class Game:
    def __init__(self, client=None):
        pg.init()
        pg.mouse.set_visible(False)
        self.size = self.width, self.height = (settings.WIDTH, settings.HEIGHT)
        self.screen = pg.display.set_mode(self.size, pg.SCALED)

        self.manager = Manager()

        self.player = PlayerEntity(self.manager).player
        self.map = self.manager.get(MapComponent, self.player).map

        self.manager.add_system(MouseControlSystem)
        self.manager.add_system(LocatedSystem)
        self.manager.add_system(KeysControlSystem)
        self.manager.add_system(GravitationSystem)
        self.manager.add_system(FirstPersonWeaponSystem)

        self.game_interface = game_interface.GameInterface(self.map, self.player, self.screen, self.manager)

        self.voxel_render = voxel_render.VoxelRender(self, self.manager)

        self.clock = pg.time.Clock()

        self.answer = ''
        self.game_run = True

        self.client = client

        self.client_return = None

    def update(self):
        events = pg.event.get()
        for _ in events:
            self.response_pressed_keys()
        self.manager.update_systems(self.screen, 0, events)
        self.voxel_render.update()
        self.game_interface.update_mouse()

    def draw(self):
        self.voxel_render.draw()
        self.game_interface.draw_fps(self.clock)
        self.game_interface.draw_config()
        self.game_interface.draw_mini_map()
        self.game_interface.draw_weapon()
        pg.display.flip()

    def response_pressed_keys(self):
        self.player_data = []
        self.answer = self.game_interface.response_pressed_keys()
        if self.answer == 'lobby':
            self.game_run = False

    def run(self):
        while self.game_run:
            self.update()
            self.draw()

            self.client_return = []
            self.player_data = []

            self.clock.tick(60)
        return self.answer


if __name__ == '__main__':
    app = Game()
    app.run()
