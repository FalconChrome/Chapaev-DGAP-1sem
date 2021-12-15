import pygame
from pygame import mouse, Vector2
# import chapaev_3d_graph as graph
from chapaev_3d_graph import Render, Object_3D
import enum
import numpy as np
from config import *

# Checker = enum.Enum("Side", "black white")
# model = np.array([list(Checker)] * 8)


class HitHandler:
    """
    Handler for mouse game control;
    and the only gameplay option is to Turn a checker.
    """
    HitStage = enum.Enum("HitStage", "none, hitting")
    SCALE = 100

    def __init__(self):
        """Set self state to waiting for mouse input"""
        self.reset()

    def reset(self):
        self.state = self.HitStage.none
        self.boost = Vector2(0, 0)

    def mouse_handler(self, fps):
        """
        The mouse handler logic itself
        """
        if self.state == self.HitStage.hitting:
            if mouse.get_pressed()[0]:
                self.add_boost(Vector2(mouse.get_rel()), fps)
            else:
                self.release()
                return True

        elif self.state == self.HitStage.none:
            if mouse.get_pressed()[0]:
                # if model collide checker
                self.state = self.HitStage.hitting

    def add_boost(self, shift, fps):
        self.boost += shift * fps / self.SCALE

    def release(self):
        # Turn model checker with boost
        print(self.boost)
        self.reset()
        # return 0


class GameController:
    """
    The controller of game play and event
    """
    GameStage = enum.Enum("GameStage", "View Turn Motion Restart")
    size = 800, 600

    def __init__(self):
        """
        Intinialize with screen and flags
        """
        self.screen = pygame.display.set_mode(self.size)
        self.state = self.GameStage.View
        self.hit_control = HitHandler()

        self.render = Render(self.screen)
        #temporary, just while testing
        self.render.create_object(Object_3D.board[0], Object_3D.board[1], WHITE)
        for i in range(2):
            for j in range(8):
                pos = (i*7*TILE + TILE // 2, 0, j*TILE + TILE // 2)
                if i % 2 == 0:
                    self.render.create_object(Object_3D.cube[0], Object_3D.cube[1], GREEN) #куб (пока что)
                else:
                    self.render.create_object(Object_3D.cube[0], Object_3D.cube[1], RED) #куб (пока что)
                self.render.objects[-1].translate(pos) #Change
    
    def init(self, restart_option):
        # model init
        print('init', restart_option)

    def gameloop(self):
        self.FPS = 30
        self.clock = pygame.time.Clock()
        while self.state != self.GameStage.Restart:
            if self.state == self.GameStage.View:
                self.viewloop()
            elif self.state == self.GameStage.Turn:
                self.hitloop()
            elif self.state == self.GameStage.Motion:
                self.flyloop()
        return 0

    def common_process(self):
        self.render.objects[1].rotate_local_y(0.2)

        # self.render.draw_menu()
        pygame.display.set_caption(self.state.name)
        pygame.display.update()
        self.clock.tick(self.FPS)

    def hitloop(self):
        while self.state == self.GameStage.Turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.GameStage.Restart
                    return None
            hitted = self.hit_control.mouse_handler(self.FPS)
            if hitted:
                self.state = self.GameStage.Motion
                # model start motion

            self.render.draw_objects_2D()
            self.common_process()

    def flyloop(self):
        while self.state == self.GameStage.Motion:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.GameStage.Restart
                    return Nones
            # when model stop flying
            self.state = self.GameStage.View

            self.render.draw_objects_2D()
            self.common_process()

    def viewloop(self):
        fixed_view = True
        while self.state == self.GameStage.View:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.GameStage.Restart
                    return None
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_v):
                    fixed_view = not fixed_view
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event)
                else:
                    self.render.camera.control()
            if fixed_view:
                self.render.draw_objects_2D()
            else:
                self.render.draw_objects_3D()
            self.common_process()

    def click(self, event):
        if self.state == self.GameStage.View:
            self.state = self.GameStage.Turn
        # print(event.pos)


def mainloop(game):
    """
    Control loop of the games
    """
    restart_option = 1
    while restart_option != 0:
        game.init(restart_option)
        restart_option = game.gameloop()


if __name__ == "__main__":
    pygame.init()
    game = GameController()
    mainloop(game)
    pygame.quit()
