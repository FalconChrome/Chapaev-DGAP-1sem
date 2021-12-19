import pygame
from pygame import mouse, Vector2
from enum import Enum
# from config import *
from checkers import Checker


class HitHandler:
    """
    Handler for mouse game control;
    and the only gameplay option is to TURN a checker.
    """
    HitStage = Enum("HitStage", "NONE, HITTING")
    SCALE = 60

    def __init__(self):
        """Set self state to waiting for mouse input"""
        self.reset()

    def reset(self):
        self.state = self.HitStage.NONE
        self.checker = None

    def mouse_handler(self, checkers, fps):
        """
        The mouse handler logic itself
        """
        if self.state == self.HitStage.HITTING:
            checker = checkers.collide(mouse.get_pos())
            if checker is not None and self.checker is None:
                self.checker = checker
            self.time += 1 / fps
            if not mouse.get_pressed()[0]:
                self.release()
                return True

        elif self.state == self.HitStage.NONE:
            if mouse.get_pressed()[0]:
                self.start_hit(Vector2(mouse.get_pos()))

    def start_hit(self, pos):
        self.state = self.HitStage.HITTING
        self.startpos = pos
        self.time = 0.01

    def release(self):
        if self.checker is not None:
            shift = Vector2(mouse.get_pos()) - self.startpos
            # print(self.checker.get_pos(), "release")
            self.checker.kick(shift / self.time / self.SCALE)
        self.reset()
        # return 0


class DisplayManager:
    Screens = Enum("Screens", "MENU GAME")

    def __init__(self, renderer):
        self.show_screen = self.Screens.GAME
        self.fixed_view = True
        self.change_cam = renderer.change_cam

    def render(self, renderer):
        if self.show_screen == self.Screens.GAME:
            if self.fixed_view:
                renderer.draw_objects_2D()
            else:
                renderer.draw_objects_3D()
                renderer.camera.control()
        else:
            renderer.draw_menu()

    def toggle_view(self):
        self.fixed_view ^= True

    def toggle_screen(self, screen_name):
        self.show_screen = self.Screens[screen_name.upper()]

class CheckerManager:
    def gen_players(self, tile=75, radius=37.5):
        positions = [[(i * 7 * tile + tile // 2,
                       j * tile + tile // 2)
                      for j in range(8)]
                     for i in range(2)]
        self.players = [[Checker(*pos, 0, 0, radius)
                         for pos in player_pos]
                        for player_pos in positions]
        self.all = [*self.players[0], *self.players[1]]
        # self.all[0].Vy += 5

    def get_positions(self):
        return [checker.get_pos() for checker in self.all]

    def update(self):
        # print(self.all[0].distance2(self.all[1]))
        for checker in self.all:
            checker.update(self.all)

    def collide(self, pos):
        i = 0
        for checker in self.all:
            dist2 = checker.distance2_to_pos(mouse.get_pos())
            if dist2 <= checker.radius ** 2:
                print("found", i)
                return checker
            i+=1

    def resting(self):
        return all(map(Checker.resting, self.all))
