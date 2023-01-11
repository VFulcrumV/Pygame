import sys
from threading import Thread

import pygame as pg

from client_server import client, server
import game_directory.game as game
import game_directory.voxel_render as voxel_render
from lobby.main_lobby import MainLobby


class App:
    def __init__(self):
        self.passed_buttons = pg.key

        self.switch = 'lobby'
        self.client_answer = False
        self.server_answer = False

        self.server = None
        self.client = None

        self.users = []

        self.game = None
        self.lobby = None

    def in_lobby(self):
        self.lobby = MainLobby(self.client, self.server)
        if self.server is not None:
            self.server.server_answer = False
        self.switch = self.lobby.run()
        self.lobby = None

    def create_client(self):
        try:
            self.switch = 'game_directory'
            self.client = client.Client('26.35.223.104', 7000)
            self.client.connect()
        except Exception:
            self.switch = 'lobby'

    def run_server(self):
        try:
            self.switch = 'client'
            self.server = server.Server('26.35.223.104', 7000)
            Thread(target=self.server.start_server).start()
            self.server_answer = True
        except Exception as e:
            print(e)
            self.switch = 'lobby'

    def start_game(self):
        self.game = game.Game(self.client)
        self.switch = self.game.run()
        self.game = None

    def exit(self):
        if self.server is not None:
            self.server = None
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    app = App()
    while True:
        if app.switch == 'lobby':
            app.in_lobby()
        elif app.switch == 'client':
            app.create_client()
        elif app.switch == 'server' and not app.server_answer:
            app.run_server()
        elif app.switch == 'game_directory':
            app.start_game()
        elif app.switch == 'exit':
            app.exit()
            sys.exit()
