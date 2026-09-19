#This is a 2d physics engine built in python, using the PyGame module and math module.
#The physics objects used will be basic shapes, such as rectangles, circles, triangles, etc.

import pygame as py
import math as m
import random as r

#initialise pygame
py.init()

screen = py.display.set_mode((800, 600))

py.display.set_caption("2d Physics Engine")

running = True
a, b = r.randint(0, 800), r.randint(0, 600)
while running:

    #get all the events, such as key press, quit, etc.
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.fill((0, 0, 0))

    #using pygame to draw a shape at random positions
    py.draw.rect(screen, (255, 255, 255), (a, b, 100, 100))

    py.display.flip()

py.quit()
print("Quit")
input("Press enter to exit...")