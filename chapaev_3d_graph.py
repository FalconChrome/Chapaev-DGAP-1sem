# Graphics for Chapaev 3D with poligons
''' Camera control: wasd, to change angle use LEFT,RIGHT.
    UP and DOWN didn't work well

    !!!ATTENTION!!! левосторонняя система координат xyz - y = 0 - плоскость событий
    '''
import pygame as pg
import numpy as np



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
    ''' button with color (tuple 3 int), text (str), text_size - int, pos - center (tuple 2 int),
        width (int) and height (int)'''
    def __init__(self, color, text, text_size, pos, width, height):
        self.color = color
        self.x, self.y = pos
        self.pos = (self.x - width / 2, self.y - height / 2)
        self.x, self.y = self.pos
        self.width = width
        self.height = height
        self.font = pg.font.SysFont('Comic Sans MS', text_size)
        self.text = self.font.render(text, True, [0, 0, 0])
        self.text_width, self.text_height = self.font.size(text)
        self.textpos = (self.x + (self.width - self.text_width) / 2 , self.y + (self.height - self.text_height) / 2)
    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.pos, (self.width, self.height)))#FIXIT нужен текст, + ещё кнопки
        screen.blit(self.text, self.textpos)

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
    def __init__(self, position):
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

    def control(self):   #Part of dispetcherisation
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

def calculate_board():
    A = np.empty(shape=(81,4), dtype = int)
    for i in range(9):
        for j in range(9):
            A[i*9+j] = (i*TILE, 0, j*TILE, 1)
    B = np.empty(shape = (64, 4), dtype = int)
    for i in range(8):
        for j in range(8):
            B[i*8 + j] = (i*9+j, i*9 + j + 1, i*9 + j + 10, i*9 + j + 9)
    return A, B

class Object_3D:
    ''' render - Render obgect
        points - numpy array of points
        faces - numpy array of numbers of points, that together make faces
        color - tuple of 3 integer (0 - 255)
        visibility - if True, then visibу, else - invisible
        pos = tuple 3 int
    '''
    cube = (np.array([(-RADIUS/2, 0, -RADIUS/2, 1), (-RADIUS/2, RADIUS, -RADIUS/2, 1),
                    (RADIUS/2, RADIUS, -RADIUS/2, 1),(RADIUS/2, 0, -RADIUS/2, 1),
                      (-RADIUS/2, 0, RADIUS/2, 1), (-RADIUS/2, RADIUS, RADIUS/2, 1),
                      (RADIUS/2, RADIUS, RADIUS/2, 1), (RADIUS/2, 0, RADIUS/2, 1)]),
                    np.array([(0, 1, 2, 3), (0, 4, 7, 3), (0, 4, 5, 1),
                              (1, 2, 6, 5), (2, 3, 7, 6), (4, 5, 6, 7)]))
    board = calculate_board()
    def __init__(self, render, points, faces, color, pos):
        self.screen = render.screen
        self.camera = render.camera
        self.projection = render.projection
        self.H_WIDTH = render.H_WIDTH
        self.H_HEIGHT = render.H_HEIGHT
        self.points = points
        self.color = color
        self.faces = faces
        self.visibility = True
        self.pos = pos

    def draw(self):
        if self.visibility:
            self.screen_projection()

    def draw_2D(self):
        if self.visibility:
            points_screen = self.points[:, ::2]
            for face in self.faces:
                polygon = points_screen[face]
                pg.draw.polygon(self.screen, self.color, polygon, 3)


    def screen_projection(self):
        points = self.points @ self.camera.camera_matrix()
        points = points @ self.projection.projection_matrix
        points /= points[:, -1].reshape(-1, 1)
        points[(points > 2) | (points < -2)] = 0
        points = points @ self.projection.to_screen_matrix
        points_screen = points[:, :2]

        for face in self.faces:
            polygon = points_screen[face]
            if not np.any((polygon == self.H_WIDTH)|(polygon == self.H_HEIGHT)):  #check out of drawing range
                pg.draw.polygon(self.screen, self.color, polygon, 3)


    def set_coords(self, pos):
        self.points = self.points @ translate(pos)        # Вращение и перемещение в глобальной системе координат

    def translate(self, pos):
        self.points = self.points @ translate(pos)

    def scale(self, sc):
        self.points = self.points @ scale(sc)

    def rotate_x(self, angle):
        self.points = self.points @ rotate_x(angle)

    def rotate_y(self, angle):
        self.points = self.points @ rotate_y(angle)

    def rotate_z(self, angle):
        self.points = self.points @ rotate_z(angle)

    def rotate_local_y(self, angle):
        t1, t2, t3 = self.pos
        anti_pos = -t1, -t2, -t3
        self.set_coords(anti_pos)
        self.rotate_y(angle)
        self.set_coords(self.pos)

    
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
    ''' The big main class, that draw everything
        __init__ - take screen - pygame screen
        methods:
        1) create_object(self, poitns, faces, color)
           creates object with position, that depends on the object definition
           easily can be changed to any coords, by using Object_3D method set_coords
        2) draw_objects_3D - drawing obgects in 3D
        3) draw_menu - drawing main screen
    '''



    def __init__(self, screen):
        self.objects = []  # First will be board, then cheese
        self.screen = screen
        self.RES = self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.H_WIDTH, self.H_HEIGHT = WIDTH // 2, HEIGHT // 2
        self.camera = Camera([0.5*TILE, TILE,-4*TILE])
        self.projection = Projection(self)

    def create_object(self, points, faces, color, pos):
        ''' Создание объекта для отрисовки'''
        object1 = Object_3D(self, points, faces, color, pos)
        self.objects.append(object1)

    def draw_objects_3D(self):
        ''' Метод для отрисовки объектов в 3D (пока на чёрном фоне)
            отрисовка зависит от положения объектов и от положения камеры
        '''
        self.screen.fill(BLACK)
        for object1 in self.objects:
            object1.draw()

    def draw_menu(self):  #FIXIT
        ''' The first screen, greeting, settings, game mode'''
        self.screen.fill(BLACK)
        BUT_START.draw(self.screen)
        BUT_NAME.draw(self.screen)
        BUT_SETTINGS.draw(self.screen)
    def draw_objects_2D(self):
        self.screen.fill(BLACK)
        for object1 in self.objects:
            object1.draw_2D()


def rescale():
    '''This function will scale coords, if we need'''
    pass

'''if __name__ == "__main__":
    print('THIS MODULE NOT FOR DIRECT CALL') '''

'''   TUTORIAL
    draw1 = Render(screen) - example of initialization class Render
    draw1.create_object(Object_3D.board[0], Object_3D.board[1], WHITE, (0, 0, 0)) - 
        Object_3D.board[0] - numpy array of points
        Object_3D.board[1] - numpy array of faces
        WHITE - color
        (0, 0, 0) - position of local sistem coords.
        Object_3D.cube - same with board - tuple of 2 numpy arrays
    draw1.objects[-1].set_coords(pos) - in future - set new coords in global sistem
        [-1] - last object in array
    draw1.draw_menu() - draw menu. Nothing else.
    draw1.objects[1].rotate_local_y(0.2) - rotate object around it's local oy (vertical)
        0.2 - angle 
    draw1.draw_objects_2D() - draw objects in 3D
    draw1.draw_objects_3D() - draw objects in 2D
    draw1.camera.control() - motion camera (MAYBE PUT IT IN MAIN)
'''


if __name__ == "__main__": # This module will be not callable, this is temporary, just while testing
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.font.init()
    clock = pg.time.Clock()
    draw1 = Render(screen) # экземпляр класса отрисовки
    draw1.create_object(Object_3D.board[0], Object_3D.board[1], WHITE, (0, 0, 0))

    BUT_START = Button(RED, 'START', 20, (HALF_WIDTH, HALF_HEIGHT), 125, 50)
    BUT_NAME = Button(RED, 'WRITE YOUR NAME', 10, (HALF_WIDTH, HALF_HEIGHT -100), 125, 50)
    BUT_SETTINGS = Button(RED, 'SETTINGS', 20, (HALF_WIDTH, HALF_HEIGHT +100), 125, 50)

    
    for i in range(2):
        for j in range(8):
            pos = (i*7*TILE + TILE // 2, 0, j*TILE + TILE // 2)
            if i % 2 == 0:
                draw1.create_object(Object_3D.cube[0], Object_3D.cube[1], GREEN, pos) #куб (пока что)
            else:
                draw1.create_object(Object_3D.cube[0], Object_3D.cube[1], RED, pos) #куб (пока что)
            draw1.objects[-1].translate(pos) #Changed
    
    finished = False
    great_finish = False
    FLAG = True
    while not great_finish:

        while not finished and not great_finish:
            draw1.draw_menu()                             #ТИПА МЕНЮ (FIXIT)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    great_finish = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        finished = True
            pg.display.set_caption(str(clock.get_fps()))
            pg.display.update()
            clock.tick(FPS)

        finished = False
        while not finished and not great_finish:
            draw1.objects[1].rotate_local_y(0.2) #поворот объекта 1 на 0.2 радиана каждый кадр
            if FLAG == True:
                draw1.draw_objects_2D()              #отрисовка объектов
            else:
                draw1.draw_objects_3D()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        FLAG = not FLAG
                draw1.camera.control()
            pg.display.set_caption(str(clock.get_fps()))
            pg.display.update()
            clock.tick(FPS)
        finished = False

    pg.quit()
