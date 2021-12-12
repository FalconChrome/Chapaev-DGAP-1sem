import pygame
import chapaev_3d_graph as graph
import enum


Stage = enum.Enum("Stage", "move, fly")

model = None


def init(option):
    # model init
    print(option)


def click(event):
    print(event.pos)


def process_event(event):
    if event.type == pygame.MOUSEBUTTONUP:
        click(event)


def mouse_hit(mouse):
    pass


def gameloop():
    FPS = 24
    clock = pygame.time.Clock()
    state = Stage.move
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                process_event(event)

        if state == Stage.move:
            mouse_hit(pygame.mouse)
        # update(FPS)
        # render()
        clock.tick(FPS)
    return False


def play(restart):
    init(restart)
    return gameloop()


if __name__ == "__main__":
    pygame.init()
    size = 1600, 960
    screen = pygame.display.set_mode(size)
    restart = 1
    while restart != 0:
        restart = play(restart)
    pygame.quit()
