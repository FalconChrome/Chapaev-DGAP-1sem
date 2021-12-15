'''This file using to to describe general data'''

# COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# pygame settings

WIDTH = 800
HEIGHT = 600
FPS = 30

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2


# Game settings

TILE = min(WIDTH, HEIGHT) // 8 #Length of one tile in chessboard
RADIUS = TILE // 2 #Radius of the "шашка"

# BUTTONs

class Button():
    ''' button with color (tuple 3 int), text (str), pos (tuple 2 int),
        width (int) and height (int)'''
    def __init__(self, color, text, pos, width, height):
        self.color = color
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text

BUT_1 = Button(RED, 'START', (HALF_WIDTH - 50, HALF_HEIGHT - 25), 100, 50)
