import pygame
from pygame import mouse
import chapaev_3d_graph as graph
import enum


class HitController:
    HitStage = enum.Enum("HitStage", "none, touched")

    def __init__(self):
        self.state = self.HitStage.none

    def mouse_handler(self):
        if mouse.get_pressed()[0]:
            if self.state == self.HitStage.none:
                self.state = self.HitStage.touched


class MainController:
    GameStage = enum.Enum("GameStage", "move, fly")

    def __init__(self):
        self.size = 1600, 960
        self.screen = pygame.display.set_mode(self.size)
        self.state = self.GameStage.move
        self.hit_control = HitController()

    def mainloop(self):
        restart_option = 1
        while restart_option != 0:
            self.init(restart_option)
            restart_option = self.gameloop()

    def init(self, restart_option):
        # model init
        print(restart_option)

    def gameloop(self):
        FPS = 24
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.process_event(event)

            if self.state == self.GameStage.move:
                if self.hit_control.mouse_handler():
                    self.state = self.GameStage.fly
                    # model start motion
            # update(FPS)
            # render()
            clock.tick(FPS)
        return 0

    def click(self, event):
        print(event.pos)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click(event)


if __name__ == "__main__":
    pygame.init()
    MainController().mainloop()
    pygame.quit()
