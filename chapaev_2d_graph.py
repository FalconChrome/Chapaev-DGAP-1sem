# Graphics for Chapaev
import pygame
from config import *

class Draw():
    ''' This class displays information on the screen'''
    def __init__(self, screen):
        self.sc = screen

    def background(self, pos):
        x, y = pos
        for i in range(8):
            for j in range(8):
                cur_pos = (x + (i-4) * TILE, y + (j - 4) * TILE, TILE, TILE)
                color = RED if (i+j) % 2 == 0 else GREEN
                pygame.draw.rect(self.sc, color, cur_pos, 0)

    def chess(self):
        pass

if __name__ == "__main__":
    print('THIS MODULE NOT FOR DIRECT CALL')
                
