import pygame
from pygame import mouse, Vector2
from pygame import Color
from chapaev_3d_graph import Render, Button  # Object_3D
from enum import Enum
from config import *
from checkers import Checker
from managers import HitHandler, DisplayManager, CheckerManager

from transitions import Machine

# Checker = enum.Enum("Side", "black white")
# model = np.array([list(Checker)] * 8)


class GameDispatcher:
    """
    The controller of game play and event
    """
    GameStage = Enum("GameStage", "VIEW TURN MOTION RESTART")

    def __init__(self):
        """
        Intinialize with screen and flags
        """
        # self.GameStage = Enum("GameStage", {
        #     'VIEW': self.viewloop,
        #     'TURN': self.hitloop,
        #     'MOTION': self.flyloop,
        #     'RESTART': self.restart
        # })

        self.state = self.GameStage.VIEW
        self.hit_control = HitHandler()
        # self.players = {"color": ("green", "red")}
        # self.player_colors = tuple(map(Color, self.players["color"]))

    def restart(self, restart_option):
        # model init
        # FIX: model gen all, not renderer_manager
        renderer.generate_game_objects()
        # display.toggle_screen('game')
        print('init', restart_option)

    def common_process(self):
        display.render(renderer)

        # renderer.draw_menu()
        pygame.display.set_caption(self.state.name)
        pygame.display.update()
        self.clock.tick(self.FPS)

    def menuloop(self):
        BUT_START = Button(RED, 'START', 20, (HALF_WIDTH, HALF_HEIGHT), 125, 50)
        BUT_NAME = Button(RED, 'WRITE YOUR NAME', 10, (HALF_WIDTH, HALF_HEIGHT -100), 125, 50)
        BUT_SETTINGS = Button(RED, 'SETTINGS', 20, (HALF_WIDTH, HALF_HEIGHT +100), 125, 50)
        self.FPS = 30
        self.clock = pygame.time.Clock()
        while (display.show_screen ==
               display.Screens['MENU']):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.GameStage.RESTART
                    return None
            self.common_process()
        else:
            return 0

    def gameloop(self):
        self.FPS = 30
        self.clock = pygame.time.Clock()
        while self.state != self.GameStage.RESTART:
            if self.state == self.GameStage.VIEW:
                self.viewloop()
            elif self.state == self.GameStage.TURN:
                self.hitloop()
            elif self.state == self.GameStage.MOTION:
                self.flyloop()
        return 0

    def hitloop(self):
        while self.state == self.GameStage.TURN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.GameStage.RESTART
                    return None
            hitted = self.hit_control.mouse_handler(self.FPS)
            if hitted:
                self.state = self.GameStage.MOTION
                # model start motion

            self.common_process()

    def flyloop(self):
        while self.state == self.GameStage.MOTION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.GameStage.RESTART
                    return None
                else:  # if event.type == pygame.KEYDOWN:
                    self.state = self.GameStage.VIEW
            # when model stop flying

            self.common_process()

    def viewloop(self):
        while self.state == self.GameStage.VIEW:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.GameStage.RESTART
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        display.toggle_view()
                    elif event.key == pygame.K_2:
                        display.change_cam()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event)
            self.common_process()

    def click(self, event):
        if self.state == self.GameStage.VIEW:
            self.state = self.GameStage.TURN
        # print(event.pos)

def mainloop():
    """
    Control loop of the games
    """
    restart_option = 1
    while restart_option != 0:
        game.restart(restart_option)
        restart_option = game.gameloop()


if __name__ == "__main__":
    pygame.init()
    renderer = Render()
    display = DisplayManager(renderer)
    game = GameDispatcher()
    mainloop()
    pygame.quit()
