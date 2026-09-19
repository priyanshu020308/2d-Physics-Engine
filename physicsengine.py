#This is a 2d physics engine built in python, using the PyGame module and math module.
#The physics objects used will be basic shapes, such as rectangles, circles, triangles, etc.

import pygame as py
import math as m
import random as r
#initialise pygame
py.init()

width = 800
height = 600

#initialise screen
screen = py.display.set_mode((width, height))
py.display.set_caption("2d Physics Engine")

clock = py.time.Clock() #initialise clock


# initialise physics vars
g = 980 # initialise gravity
restitution = 1.5 # 1 = perfectly elastic, 0 = no bounce at all
rest_threshold = 15 # below this speed on impact, the ball is considered at rest

#initialise circle vars
radius = 50
floor = height - radius
ceiling = 0 + radius

a, b = 400, ceiling # initial positions
x, y = a, b # will be used to control the objects movement and position
vel_y = 0.0 # y velocity of the object
vel_x = 0.0 # x velocity of the object

#set boundaries


running = True # initialise loop
while running:

    delta_time = clock.tick(120) / 1000.0

    #get all the events, such as key press, quit, etc.
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    #adding gravity
    vel_y += g * delta_time
    y += vel_y * delta_time

    #floor collision and rebound
    if y >= floor or y <= ceiling:
        if y >= floor:
            y = floor # snap back so the object never sinks below the floor
        elif y <= ceiling:
            y = ceiling # snap back so the object never goes above the ceiling
        vel_y = -vel_y * restitution # reverse direction and lose some energy

        if abs(vel_y) < rest_threshold: # stop tiny endless micro-bounces
            vel_y = 0.0

    screen.fill((0, 0, 0))

    #using pygame.draw to draw a physics shape (a rigid body)
    py.draw.circle(screen, (255, 255, 255), (int(x), int(y)), radius)

    py.display.flip()

py.quit()
print("Quit")