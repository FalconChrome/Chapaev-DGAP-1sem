# Graphics for Chapaev 3D with poligons
''' Camera control: wasd, to change angle use LEFT,RIGHT.
    UP and DOWN didn't work well                         '''
import pygame as pg
import numpy as np
from config import *

class Projection:
    def __init__(self, render):
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        RIGHT = np.tan(render.camera.h_fov / 2)
        LEFT = -RIGHT
        TOP = np.tan(render.camera.v_fov / 2)
        BOTTOM = -TOP

        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)
        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]                ])
        HW, HH = render.H_WIDTH, render.H_HEIGHT
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]               ])
        
        

class Camera:
    def __init__(self, render, position):
        self.pos = np.array([*position, 1.0]) #coords of camera
        self.ox = np.array([1, 0, 0, 1]) #axes
        self.oy = np.array([0, 1, 0, 1])
        self.oz = np.array([0, 0, 1, 1])
        self.h_fov = np.pi / 3
        self.v_fov = self.h_fov * (HEIGHT / WIDTH)
        self.near_plane = 0.2
        self.far_plane = 1000
        self.moving_speed = 0.02*TILE #Скорость камеры
        self.rot_speed = 0.03 #changing angle speed
    
    def control(self, event):   #Part of dispetcherisation
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.pos -= self.ox * self.moving_speed
        if key[pg.K_d]:
            self.pos += self.ox * self.moving_speed
        if key[pg.K_s]:
            self.pos -= self.oy * self.moving_speed
        if key[pg.K_w]:
            self.pos += self.oy * self.moving_speed
        if key[pg.K_q]:
            self.pos -= self.oz * self.moving_speed
        if key[pg.K_e]:
            self.pos += self.oz * self.moving_speed
        if key[pg.K_LEFT]:
            self.camera_rot_y(-self.rot_speed)
        if key[pg.K_RIGHT]:
            self.camera_rot_y(self.rot_speed)
        if key[pg.K_UP]:
            self.camera_rot_x(-self.rot_speed)
        if key[pg.K_DOWN]:
            self.camera_rot_x(self.rot_speed)
            

    def camera_rot_y(self, angle):
        rotate = rotate_y(angle)
        self.ox = self.ox @ rotate
        self.oy = self.oy @ rotate
        self.oz = self.oz @ rotate

    def camera_rot_x(self, angle):
        rotate = rotate_x(angle)
        self.ox = self.ox @ rotate
        self.oy = self.oy @ rotate
        self.oz = self.oz @ rotate
        
        
    def translate_matrix(self):
        x, y, z, w = self.pos
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]])
    def rotate_matrix(self):
        oxx, oxy, oxz, w = self.ox
        oyx, oyy, oyz, w = self.oy
        ozx, ozy, ozz, w = self.oz
        return np.array([
            [oxx, oyx, ozx, 0],
            [oxy, oyy, ozy, 0],
            [oxz, oyz, ozz, 0],
            [0, 0, 0, 1]])
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
        

class Object_3D:
    def __init__(self, render, points, faces, color):
        self.render = render
        self.points = points
        self.color = color
        self.faces = faces

    def draw(self):
        self.screen_projection()
    
    def screen_projection(self):
        points = self.points @ self.render.camera.camera_matrix()
        points = points @ self.render.projection.projection_matrix
        points /= points[:, -1].reshape(-1, 1)
        points[(points > 2) | (points < -2)] = 0
        points = points @ self.render.projection.to_screen_matrix
        points_screen = points[:, :2]
        
        for face in self.faces:
            polygon = points_screen[face]
            if not np.any((polygon == self.render.H_WIDTH)|(polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, self.color, polygon, 3)
                    
                
    def set_coords(self, pos):
        self.points = self.points @ translate(pos)
    
    def translate(self, pos):
        self.points = self.points @ translate(pos)

    def scale(self, sc):
        self.points = self.points @ scale(pos)
        
    def rotate_x(self, angle):
        self.points = self.points @ rotate_x(angle)

    def rotate_y(self, angle):
        self.points = self.points @ rotate_y(angle)

    def rotate_z(self, angle):
        self.points = self.points @ rotate_z(angle)

def set_coord(pos):
    ''' pos - tuple of 3 float'''
    tx, ty, tz = pos
    return np.array([
        [tx, 0, 0, 0],
        [0, ty, 0, 0],
        [0, 0, tz, 0],
        [0, 0, 0, 1]])
    
def translate(pos):
    ''' pos - tuple of 3 float'''
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]])

def rotate_x(w):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(w), np.sin(w), 0],
        [0, -np.sin(w), np.cos(w), 0],
        [0, 0, 0, 1]])
def rotate_y(w):
    return np.array([
        [np.cos(w), 0, -np.sin(w), 0],
        [0, 1, 0, 0],
        [np.sin(w), 0, np.cos(w), 0],
        [0, 0, 0, 1]])
def rotate_z(w):
    return np.array([
        [np.cos(w), np.sin(w), 0, 0],
        [-np.sin(w), np.cos(w), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

def scale(a):
    return np.array([
        [a, 0, 0, 0],
        [0, a, 0, 0],
        [0, 0, a, 0],
        [0, 0, 0, 1]])

class Render():
    def __init__(self, screen):
        self.objects = []  # First will be board, then cheese
        self.screen = screen
        self.RES = self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.H_WIDTH, self.H_HEIGHT = WIDTH // 2, HEIGHT // 2
        self.camera = Camera(self, [0.5*TILE, TILE,-4*TILE])
        self.projection = Projection(self)
        
    def create_object(self, points, faces, color, ):
        object1 = Object_3D(self, points, faces, color)
        self.objects.append(object1)
        
    def draw(self):
        self.screen.fill(BLACK)
        for object1 in self.objects:
            object1.draw()
        
def rescale():
    '''This function will scale coords, if we need'''
    pass

'''if __name__ == "__main__":
    print('THIS MODULE NOT FOR DIRECT CALL') '''

if __name__ == "__main__": # This module will be not callable, just while testing
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    draw1 = Render(screen) # экземпляр класса отрисовки
    A = np.empty(shape=(81,4), dtype = int)
    for i in range(9):
        for j in range(9):
            A[i*9+j] = (i*TILE, 0, j*TILE, 1)
    B = np.empty(shape = (64, 4), dtype = int)
    for i in range(8):
        for j in range(8):
            B[i*8 + j] = (i*9+j, i*9 + j + 1, i*9 + j + 10, i*9 + j + 9)
    draw1.create_object(A, B, WHITE)
    
    for i in range(2):
        for j in range(8):
            if i % 2 == 0:
                draw1.create_object(np.array([(0, 0, 0, 1), (0, RADIUS, 0, 1), (RADIUS, RADIUS, 0, 1), (RADIUS, 0, 0, 1),(0, 0, RADIUS, 1), (0, RADIUS, RADIUS, 1), (RADIUS, RADIUS, RADIUS, 1), (RADIUS, 0, RADIUS, 1)]),
                                    np.array([(0, 1, 2, 3), (0, 4, 7, 3), (0, 4, 5, 1),(1, 2, 6, 5), (2, 3, 7, 6), (4, 5, 6, 7)]),
                                    GREEN) #куб (пока что)
            else:
                draw1.create_object(TILE*np.array([(0, 0, 0, 1), (0, RADIUS, 0, 1), (RADIUS, RADIUS, 0, 1), (RADIUS, 0, 0, 1),(0, 0, RADIUS, 1), (0, RADIUS, RADIUS, 1), (RADIUS, RADIUS, RADIUS, 1), (RADIUS, 0, RADIUS, 1)]),
                                    np.array([(0, 1, 2, 3), (0, 4, 7, 3), (0, 4, 5, 1),(1, 2, 6, 5), (2, 3, 7, 6), (4, 5, 6, 7)]),
                                    RED) #куб (пока что)
            draw1.objects[-1].set_coords((i*7*TILE + TILE // 2 - RADIUS // 2, 0, j*TILE + TILE // 2 - RADIUS // 2))
    finished = False
    while not finished:
        draw1.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            draw1.camera.control(event)
        pg.display.set_caption(str(clock.get_fps()))
        pg.display.update()
        clock.tick(FPS)

    pg.quit()
