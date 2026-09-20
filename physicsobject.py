#This object class allows us to seperate the objects between objects that can be launched and the objects that are affected by physics but cant be directly launched.
import pygame as py
from settings import *

class PhysicsObject():

    def __init__(self):
        #initialise object shape
        self.radius = 50
        self.floor = height - self.radius
        self.ceiling = 0 + self.radius

        self.left_wall = 0 + self.radius
        self.right_wall = width - self.radius
        self.x, self.y = width/2, self.ceiling # will be used to control the objects movement and position
        self.vel_y = 0.0 # y velocity of the object
        self.vel_x = 0.0 # x velocity of the object

    def update(self, delta_time):
        #adding gravity
        self.vel_y += g * delta_time # constantly pull object towards the floor
        self.y += self.vel_y * delta_time

        #floor collision and rebound
        if self.y >= self.floor or self.y <= self.ceiling:
            if self.y >= self.floor:
                self.y = self.floor # snap back so the object never sinks below the floor
            elif self.y <= self.ceiling:
                self.y = self.ceiling # snap back so the object never goes above the ceiling
            self.vel_y = -self.vel_y * restitution # reverse direction and lose some energy

            if abs(self.vel_y) < rest_threshold: # stop tiny endless micro-bounces
                self.vel_y = 0.0
        #wall collision and rebound
        if self.x >= self.right_wall or self.x <= self.left_wall:
            if self.x >= self.right_wall:
                self.x = self.right_wall # snap back so the object never goes beyond the right wall
            elif self.x <= self.left_wall:
                self.x = self.left_wall # snap back so the object never goes beyond the left wall
            self.vel_x = -self.vel_x * restitution # reverse direction and lose some energy

            if abs(self.vel_x) < rest_threshold: # stop tiny endless micro-bounces
                self.vel_x = 0.0
        #addding horizontal movement and friction
        if self.vel_x != 0 and (self.y == self.floor or self.y == self.ceiling):
            self.vel_x -= self.vel_x*friction
        self.x += self.vel_x * delta_time
            
    def draw(self, screen):
        py.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)