import pygame
from pygame import mouse, Vector2
from enum import Enum
from config import *
from checkers import Checker


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

class CheckerManager:
    def gen_players(self, tile, radius):
        player = []
        for i, color in enumerate(PLAYERCOLORS):
            for j in range(8):
                pos = (i * 7 * tile + tile // 2, 0, j * tile + tile // 2)
                self.create_objects3D("chees", color)
                self.objects[-1].translate(pos)3
