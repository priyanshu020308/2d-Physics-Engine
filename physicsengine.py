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

#initialise circle vars
a, b = 400, 0 # initial positions
radius = 50
x, y = a, b # will be used to control the objects movement and position
vel_y = 0.0 # y velocity of the object
vel_x = 0.0 # x velocity of the object

#set boundaries
floor = height - radius
ceiling = 0 + radius

running = True # initialise loop
while running:

    delta_time = clock.tick(60) / 1000.0

    #get all the events, such as key press, quit, etc.
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.fill((0, 0, 0))

    #using pygame.draw to draw a physics shape (a rigid body) at random positions
    py.draw.circle(screen, (255, 255, 255), (x, y), radius)

    #adding gravity
    if y <= floor:
        vel_y += g*delta_time
        y += vel_y*delta_time
    else:
        y = floor # to make sure that if the object goes below the floor,it gets snapped back to the floor 
        vel_y = 0 # since the object is snapped back to floor, y = 550 now, but vel_y != 0, so in the next loop, the if statement runs again. To ensure that the ball doesnt glitch out, we set vel_y = 0

    py.display.flip()

py.quit()
print("Quit")