#This is a 2d physics engine built in python, using the PyGame module and math module.
#The physics objects used will be basic shapes, such as rectangles, circles, triangles, etc.

import pygame as py
import math as m
from settings import width, height, fps
from draggableobject import DraggableObject
#initialise pygame
py.init()


#initialise screen
screen = py.display.set_mode((width, height))
py.display.set_caption("2d Physics Engine")

clock = py.time.Clock() #initialise clock

ball = DraggableObject() # the circle from before

running = True # initialise loop
while running:

    delta_time = clock.tick(fps) / 1000.0

    #get all the events, such as key press, quit, etc.
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    ball.handle_drag(screen, clock)
    ball.update(delta_time)

    screen.fill((0, 0, 0))
    ball.draw(screen)

    py.display.flip()

py.quit()
print("Quit")