import pygame
from pygame import mouse, Vector2, mixer
from pygame import Color
from chapaev_3d_graph import Render, Button, RADIUS, TILE  # Object_3D
from enum import Enum
# from config import *
from checkers import Checker
from managers import HitHandler, DisplayManager, CheckerManager

# from transitions import Machine

# Checker = enum.Enum("Side", "black white")
# model = np.array([list(Checker)] * 8)


class GameDispatcher:
    """
    The controller of game play and event
    """
    MUSIC = "петр-чаиковскии-вальс-цветов-щелкунчик.mp3"
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
        mixer.music.load(self.MUSIC)
        self.state = self.GameStage.VIEW
        self.hit_control = HitHandler()
        self.FPS = 30
        self.clock = pygame.time.Clock()
        # self.players = {"color": ("green", "red")}
        # self.player_colors = tuple(map(Color, self.players["color"]))

    def restart(self, restart_option):
        # model init
        # FIX: model gen all, not renderer_manager
        mixer.music.play(loops=-1)
        checkers.gen_players(TILE, RADIUS)
        renderer.generate_game_objects(checkers.get_positions())
        # display.toggle_screen('game')

    def common_process(self):
        display.render(renderer)

        # renderer.draw_menu()
        checkers.update()
        renderer.move_chees(checkers.get_positions())
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
            hitted = self.hit_control.mouse_handler(checkers, self.FPS)
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        display.toggle_view()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    display.toggle_view()
            if checkers.resting():
                self.state = self.GameStage.VIEW
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
                    self.state = self.GameStage.TURN
                    display.fixed_view = True
            self.common_process()


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
    mixer.init()
    renderer = Render()
    display = DisplayManager(renderer)
    game = GameDispatcher()
    checkers = CheckerManager()
    mainloop()
    pygame.quit()
