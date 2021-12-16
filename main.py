import pygame
from pygame import mouse, Vector2
from pygame import Color
# import chapaev_3d_graph as graph
from chapaev_3d_graph import Render, Button  # Object_3D
# import numpy as np
from enum import Enum
from config import *

# Checker = enum.Enum("Side", "black white")
# model = np.array([list(Checker)] * 8)


class HitHandler:
    """
    Handler for mouse game control;
    and the only gameplay option is to TURN a checker.
    """
    HitStage = Enum("HitStage", "NONE, HITTING")
    SCALE = 100

    def __init__(self):
        """Set self state to waiting for mouse input"""
        self.reset()

    def reset(self):
        self.state = self.HitStage.NONE
        self.boost = Vector2(0, 0)

    def mouse_handler(self, fps):
        """
        The mouse handler logic itself
        """
        if self.state == self.HitStage.HITTING:
            if mouse.get_pressed()[0]:
                self.add_boost(Vector2(mouse.get_rel()), fps)
            else:
                self.release()
                return True

        elif self.state == self.HitStage.NONE:
            if mouse.get_pressed()[0]:
                # if model collide checker
                self.state = self.HitStage.HITTING

    def add_boost(self, shift, fps):
        self.boost += shift * fps / self.SCALE

    def release(self):
        # TURN model checker with boost
        print(self.boost)
        self.reset()
        # return 0


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
        # FIX: model gen all, not render_manager
        renderer.generate_game_objects()
        # display.toggle_screen('game')
        print('init', restart_option)

    def common_process(self):
        display.render()

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


class DisplayManager:
    Screens = Enum("Screens", "MENU GAME")

    def __init__(self):
        self.show_screen = self.Screens.GAME
        self.fixed_view = True
        self.change_cam = renderer.change_cam

    def render(self):
        if self.show_screen == self.Screens.GAME:
            if self.fixed_view:
                renderer.draw_objects_2D()
            else:
                renderer.draw_objects_3D()
                renderer.camera.control()
            renderer.objects[1].rotate_local_y(0.2)
        else:
            renderer.draw_menu()

    def toggle_view(self):
        self.fixed_view ^= True

    def toggle_screen(self, screen_name):
        self.show_screen = self.Screens[screen_name.upper()]


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
    display = DisplayManager()
    game = GameDispatcher()
    mainloop()
    pygame.quit()
