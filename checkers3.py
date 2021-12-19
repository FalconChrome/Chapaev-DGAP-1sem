import pygame
import math

class Checker:
    def __init__(self, x,y,Vx,Vy,radius=37.5):
        self.x  =  x
        self.y  =  y
        self.Vx  =  Vx
        self.Vy  =  Vy
        self.radius = radius

    def distance2(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def distance2_to_pos(self, pos):
        return (self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2

    def move(self,):
        # if self.Vy != 0.0:
        #     print(self.x, self.Vx, self.y)
        self.x+=self.Vx    #Перемещение
        self.y+=self.Vy
        self.Vx-=self.Vx*0.04 # вязкое трение
        self.Vy-=self.Vy*0.04
        if 0 < self.Vx ** 2 < 0.01:
            self.Vx = 0
        if 0 < self.Vy ** 2 < 0.01:
            self.Vy = 0

    def update(self, others):
        self.move()
        for other in others:
            # if self.distance2(other) not in (0.0, 551250.0):
            #     print(self.distance2(other))
            if 0 < self.distance2(other) <= (self.radius + other.radius) ** 2:
                self.hit(other)

    def hit(self,other):
        print("hit checker")
        self.x+=-self.Vx
        self.y+=-self.Vy
        gamma=math.atan2(other.y-self.y,other.x-self.x)
        betta=math.atan2(self.Vy,self.Vx)
        alfa=abs(gamma-betta)
        V0=(self.Vx**2+self.Vy**2)**0.5
        V=V0*math.sin(alfa)
        V1=V0*math.cos(alfa)
        other.Vx=V1*math.cos(gamma)
        other.Vy=V1*math.sin(gamma)
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

    def kick(self, boost):
        self.Vx += boost[0]
        self.Vy += boost[1]

    def get_pos(self):
        return self.x, 0, self.y

    def resting(self):
        return self.Vx == 0 and self.Vy == 0
