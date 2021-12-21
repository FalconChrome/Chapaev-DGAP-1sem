# Graphics for Chapaev 3D with poligons and 2D as projection on a ground surface
'''
    Camera control: wasd, to change angle use LEFT,RIGHT,UP,DOWN.
    ATTENTION this function is just for testing, because of many bugs
'''

import pygame as pg
import numpy as np

# COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BACKGROUND_BLUE = (224, 255, 255)
BOARD_YELLOW = (250, 208, 174)
BOARD_BLACK = (81, 22, 4)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEXT_COLOR = (100, 200, 100)

TABLE_COLOR = LIGHT_BLUE
PLAYERCOLORS = (GREEN, RED)
BOARD_COLORS = (BOARD_YELLOW, BOARD_BLACK)

# pygame settings
WIDTH = 600
HEIGHT = 600
FPS = 30
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# Game settings
TILE = min(WIDTH, HEIGHT) // 8 #Length of one tile in chessboard
RADIUS = TILE // 4             #Radius of the "шашка"

CH_H = RADIUS                  #HEIGHT of "шашка"


class Button():
    '''
    mini class Button, to easily create then
    button with color (tuple 3 int), text (str), text_size - int, pos - center (tuple 2 int),
    width (int) and height (int)
    '''
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
        pg.draw.rect(screen, self.color, (self.pos, (self.width, self.height)))
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
        self.ox = np.array([-1, 0, 0, 1])     #axes
        self.oy = np.array([0, 1, 0, 1])
        self.oz = np.array([0, 0, 1, 1])
        self.h_fov = np.pi / 3
        self.v_fov = self.h_fov * (HEIGHT / WIDTH)
        self.near_plane = 0.2
        self.far_plane = 1000
        self.moving_speed = 0.02*TILE #Скорость камеры
        self.rot_speed = 0.2          #changing angle speed

    def control(self):   #Part of dispetcherisation (IT IS JUST FOR TESTING)
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.pos -= self.ox * self.moving_speed
        if key[pg.K_d]:
            self.pos += self.ox * self.moving_speed
        if key[pg.K_s]:
            if self.pos[1] > 2*TILE:
                self.pos -= self.oy * self.moving_speed
        if key[pg.K_w]:
            self.pos += self.oy * self.moving_speed
        if key[pg.K_q]:
            self.pos -= self.oz * self.moving_speed
        if key[pg.K_e]:
            if self.pos[1] > 2*TILE:
                self.pos += self.oz * self.moving_speed
        if key[pg.K_LEFT]:
            self.camera_rot_y(self.rot_speed)
        if key[pg.K_RIGHT]:
            self.camera_rot_y(-self.rot_speed)
        #if key[pg.K_UP]:
        #    self.camera_rot_x(-self.rot_speed)
        #if key[pg.K_DOWN]:
        #   self.camera_rot_x(self.rot_speed)


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

    def camera_rot_z(self, angle):
        rotate = rotate_z(angle)
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
    A = np.empty(shape = (82, 4), dtype = float)
    for i in range(9):
        for j in range(9):
            A[i*9 + j] = (i*TILE, 0, j*TILE, 1)
    A[81] = (0, 0, 0, 1)
    B = np.empty(shape = (64, 4), dtype = int)
    for i in range(8):
        for j in range(8):
            B[i*8 + j] = (i*9 + j, i*9 + j + 1, i*9 + j + 10, i*9 + j + 9)
    return A, B

def calculate_chees(N):
    H = CH_H
    A = np.empty(shape = (2*N + 1, 4), dtype = float)
    B = np.empty(shape = (N, 4), dtype = int)
    for i in range(N):
        x = RADIUS * np.cos(2*np.pi * i / N)
        z = RADIUS * np.sin(2*np.pi * i / N)
        A[i] = (x, 0, z, 1)
    for i in range(N , 2*N):
        x = RADIUS * np.cos(2*np.pi * (i-N) / N)
        z = RADIUS * np.sin(2*np.pi * (i-N) / N)
        A[i] = (x, H, z, 1)
    A[2*N] = (0, 0, 0, 1)
    for i in range(N):
        B[i] = (i, (i+1) % N, N + (i+1) % N, N+i)
    return A, B

class Object_3D:
    '''
    render - Render object
    points - numpy array of points, last point - center of local sistem
    faces - numpy array of numbers of points, that together make faces
    color - tuple of 3 integer (0 - 255)
    visibility - if True, then visibу, else - invisible
    pos = tuple 4 float (last in points)
    '''
    cube = (np.array([(-RADIUS/2, 0, -RADIUS/2, 1), (-RADIUS/2, RADIUS, -RADIUS/2, 1),
                    (RADIUS/2, RADIUS, -RADIUS/2, 1),(RADIUS/2, 0, -RADIUS/2, 1),
                      (-RADIUS/2, 0, RADIUS/2, 1), (-RADIUS/2, RADIUS, RADIUS/2, 1),
                      (RADIUS/2, RADIUS, RADIUS/2, 1), (RADIUS/2, 0, RADIUS/2, 1), (0, 0, 0, 1)]),
                    np.array([(0, 1, 2, 3), (0, 4, 7, 3), (0, 4, 5, 1),
                              (1, 2, 6, 5), (2, 3, 7, 6), (4, 5, 6, 7)]))
    board = calculate_board()
    chees = calculate_chees(16) #20 - Ideal, 50 - max, over 200 - lagging

    table = (np.array([(-4*TILE, 0, -4*TILE, 1), (-4*TILE, 4*TILE, -4*TILE, 1),
                    (4*TILE, 4*TILE, -4*TILE, 1),(4*TILE, 0, -4*TILE, 1),
                      (-4*TILE, 0, 4*TILE, 1), (-4*TILE, 4*TILE, 4*TILE, 1),
                      (4*TILE, 4*TILE, 4*TILE, 1), (4*TILE, 0, 4*TILE, 1), (0, 0, 0, 1)]),
                    np.array([(0, 1, 2, 3), (0, 4, 7, 3), (0, 4, 5, 1),
                              (1, 2, 6, 5), (2, 3, 7, 6), (4, 5, 6, 7)]))#USELESS


    def __init__(self, render, points, faces, color, type):
        self.screen = render.screen
        self.camera = render.camera
        self.projection = render.projection
        self.H_WIDTH = render.H_WIDTH
        self.H_HEIGHT = render.H_HEIGHT
        self.points = points
        self.color = color
        self.faces = faces
        self.visibility = True
        self.pos = points[-1]
        self.type = type

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
        points[(points > 4) | (points < -4)] = 0
        points = points @ self.projection.to_screen_matrix
        points_screen = points[:, :2]
        for face in self.faces:
            polygon = points_screen[face]
            if not np.any((polygon == self.H_WIDTH)|(polygon == self.H_HEIGHT)):#checking out of drawing range
                color = self.color
                LINE_WIDTH = 3
                if self.type == "board":
                    color = BOARD_COLORS[max(face) % 2]
                    LINE_WIDTH = 0
                pg.draw.polygon(self.screen, color, polygon, LINE_WIDTH)

    def change_pos(self):
        ''' change pos to actual pos'''
        self.pos = self.points[-1]

    def set_coords(self, pos):
        ''' set coords pos in global sistem '''
        t1, t2, t3, t4 = self.points[-1]
        anti_pos_0 = (-t1, -t2, -t3)
        self.points = self.points @ translate(anti_pos_0)
        self.points = self.points @ translate(pos)
        self.change_pos()

    def translate(self, pos):
        self.points = self.points @ translate(pos)
        self.change_pos()

    def scale(self, sc):
        self.points = self.points @ scale(sc)

    def rotate_x(self, angle):
        self.points = self.points @ rotate_x(angle)

    def rotate_y(self, angle):
        self.points = self.points @ rotate_y(angle)

    def rotate_z(self, angle):
        self.points = self.points @ rotate_z(angle)

    def rotate_local_y(self, angle):
        t1, t2, t3, t4 = self.pos
        pos = t1, t2, t3
        anti_pos = -t1, -t2, -t3
        self.set_coords(anti_pos)
        self.rotate_y(angle)
        self.set_coords(pos)

    def change_cam(self, camera):
        ''' function change camera '''
        self.camera = camera

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

def calculate_cam(pos, angle_x, angle_y, angle_z):
    CAM = Camera([0, 0, 0])
    CAM.camera_rot_y(angle_y)
    CAM.camera_rot_x(angle_x)
    CAM.camera_rot_z(angle_z)
    CAM.pos = [*pos, 1.0]
    return CAM

class Render():
    '''
    The big main class, that draw everything
    __init__ - take screen - pygame screen
    methods:
    1) create_object(self, poitns, faces, color)
    creates object with position, that depends on the object definition
    easily can be changed to any coords, by using Object_3D method set_coords
    2) draw_objects_3D - drawing obgects in 3D
    3) draw_menu - drawing main screen
    '''
    '''!!! Render cams, you can change them, to observe the field
    Also you can move them, but dispetcherisation not from
    main module is bad, so, I think it is not necessary to
    have ability to move camera during the game
    '''
    CAMS = [calculate_cam([14*TILE, 3*TILE, 4*TILE+0.01], 0, -np.pi / 2, np.pi / 8),
            calculate_cam([-6*TILE, 3*TILE, 4*TILE+0.01], 0, np.pi / 2, -np.pi / 8)]

    def __init__(self):
        self.objects = []  # First will be board, then cheese
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.RES = self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.H_WIDTH, self.H_HEIGHT = WIDTH // 2, HEIGHT // 2
        self.cam_number = 0
        self.camera = Render.CAMS[self.cam_number]
        self.projection = Projection(self)
        self.menu_background = pg.image.load('chapaev.jpg')
        self.menu_background_rect = self.menu_background.get_rect(bottomright=(WIDTH, HEIGHT))
        self.game_background = pg.image.load('chessboard_texture.png')
        self.game_background = pg.transform.scale(self.game_background,(WIDTH, HEIGHT))
        self.game_background_rect = self.game_background.get_rect(bottomright=(WIDTH, HEIGHT))
    
    def distance(self, a):
        ''' a, b -tuples of 4 float '''
        a1, a2, a3, a4 = a.pos
        b1, b2, b3, b4 = self.camera.pos
        return int(np.sqrt(((a1 - b1) ** 2) + ((a2 - b2) ** 2) + ((a3 - b3) ** 2)))

    def create_object(self, points, faces, color, type):
        ''' Создание объекта для отрисовки '''
        object1 = Object_3D(self, points, faces, color, type)
        self.objects.append(object1)

    def draw_objects_3D(self):
        '''
        Метод для отрисовки объектов в 3D (пока на чёрном фоне)
        отрисовка зависит от положения объектов и от положения камеры
        '''
        self.screen.fill(BACKGROUND_BLUE)
        self.objects[0].draw()

        obj = list(self.objects)
        del obj[0]
        obj.sort(key=self.distance, reverse = True)
        for object1 in obj:
            object1.draw()


    def draw_menu(self):
        ''' The first screen, greeting, settings, game mode'''
        self.screen.fill(BLACK)
        self.screen.blit(self.menu_background, self.menu_background_rect) #Отрисовка Чапаева
        BUT_START.draw(self.screen)
    
    def draw_text(self, name):
        color = BLACK
        self.screen.fill(color)
        font = pg.font.SysFont('Comic Sans MS', 30)
        text = font.render(name, True, TEXT_COLOR)
        text_width, text_height = font.size(name)
        textpos = ((WIDTH - text_width) / 2, (HEIGHT - text_height) / 2)
        pg.draw.rect(self.screen, color, ((0, 0), (WIDTH, HEIGHT)))
        self.screen.blit(text, textpos)
    
    def move_chees(self, pos):
        ''' pos - array of tuples (float, float, float)'''
        for i in range(1, len(self.objects)):
            if self.objects[i].type == "chees":
                self.objects[i].set_coords(pos[i-1])

    def draw_objects_2D(self):
        ''' This method draw 2D projection of objects (on a surface y = 0) '''
        self.screen.fill(BLACK)
        self.screen.blit(self.game_background, self.game_background_rect)
        for object1 in self.objects:
            object1.draw_2D()

    def change_cam(self):
        ''' this method change cams one by one in Render.CAMS '''
        self.cam_number = (self.cam_number + 1) % len(Render.CAMS)
        self.camera = Render.CAMS[self.cam_number]
        for obj in self.objects:
            obj.change_cam(self.camera)

    def create_objects3D(self, type, color):
        ''' wrapper for creating 3D objects '''
        if type == "chees":
            object = Object_3D.chees
        elif type == "board":
            object = Object_3D.board
        elif type == "cube":
            object = Object_3D.cube
        self.create_object(object[0], object[1], color, type)

    def generate_game_objects(self, positions):
        ''' This method generate 16 chess and a board'''
        self.create_objects3D("board", WHITE)
        for i, color in enumerate(PLAYERCOLORS):
            for j in range(8):
                self.create_objects3D("chees", color)
        self.move_chees(positions)

    def end_render(self):
        pg.quit()

def rescale():
    '''This function will scale coords, if we need'''
    pass

if __name__ == "__main__":
    print('THIS MODULE NOT FOR DIRECT CALL')
    


'''
    TUTORIAL
    draw1 = Render() - example of initialization class Render
    draw1.create_object(Object_3D.board[0], Object_3D.board[1], WHITE, "chees") -
        Object_3D.board[0] - numpy array of points
        Object_3D.board[1] - numpy array of faces
        WHITE - color
        "chees" - type
        Object_3D.cube - same with board - tuple of 2 numpy arrays
    draw1.objects[-1].set_coords(pos) - in future - set new coords in global sistem
        [-1] - last object in array
    draw1.draw_menu() - draw menu. Nothing else.
    draw1.objects[1].rotate_local_y(0.2) - rotate object around it's local oy (vertical)
        0.2 - angle
    generate_game_objects() - create game objects
    draw1.move_chees(POS) - moving all chess on their bos
    draw1.draw_objects_2D() - draw objects in 3D
    draw1.draw_objects_3D() - draw objects in 2D
    draw1.change_cam() - change camera
    draw1.camera.control() - motion camera
    draw1.draw_menu() - draw menu

'''
