import pygame
from pygame import sprite
import math

class Checker(sprite.Sprite):

    def __init__(self, x,y,Vx,Vy,checkergroup,*groups,radius=37.5):
        super().__init__(checkergroup,*groups)
        self.x  =  x
        self.y  =  y
        self.Vx  =  Vx
        self.Vy  =  Vy
        self.radius = radius
        self.image = pygame.Surface()
        self.rect = pygame.Rect(x-self.radius,y-self.radius,
                                2*self.radius,2*self.radius)
    def move(self,):
        self.x+=self.Vx    #Перемещение
        self.y+=self.Vy
        self.Vx-=self.Vx*0.01 # вязкое трение
        self.Vy-=self.Vy*0.01
    def update(self,):
        self.move()
        for checker in sprite.spritecollide(self,self.groups()[0],False,
                                            sprite.collide_circle):
            self.hit(checker) #проверка на столкновение
    def hit(self,other):
        self.x+=-2*self.Vx
        self.y+=-2*self.Vy
        gamma=math.atan2(other.y-self.y,other.x-self.x)
        betta=math.atan2(self.Vy,self.Vx)
        alfa=abs(gamma-betta)
        V0=(self.Vx**2+self.Vy**2)**0.5
        V=V0*math.sin(alfa)
        V1=V0*math.cos(alfa)
        other.Vx=V1*math.cos(gamma)
        other.Vy=V1*math.sin(gamma)
        print(gamma)
        print(alfa)
        print(betta)
        if self.Vy<0:
            if abs(gamma)<abs(betta):
                self.Vx=V*math.cos(-3.14159/2+gamma)#FIX
                self.Vy=V*math.sin(-3.14159/2+gamma)
            else:
                self.Vx=V*math.cos(3.14159/2+gamma)#FIX
                self.Vy=V*math.sin(3.14159/2+gamma)
        else:
            if abs(gamma)>abs(betta):
                self.Vx=V*math.cos(-3.14159/2+gamma)#FIX
                self.Vy=V*math.sin(-3.14159/2+gamma)
            else:
                self.Vx=V*math.cos(3.14159/2+gamma)#FIX
                self.Vy=V*math.sin(3.14159/2+gamma)
        self.y+=self.Vy
        self.x+=self.Vx
        other.y+=other.Vy
        other.x+=other.Vx

    def get_pos(self):
        return self.x, 0, self.y
        

        
        
    



