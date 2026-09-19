#This is a 2d physics engine built in python, using the PyGame module and math module.
#The physics objects used will be basic shapes, such as rectangles, circles, triangles, etc.

import pygame as py
import math as m
import random as r
#initialise pygame
py.init()
lst = [] # to check if the mouse press works, we will append the balls coordinates and whenever I press the mouse button, and print it in the  end.
#update: mouse click works, and position check works, will remove it shortly
width = 1500
height = 1000

#initialise screen
screen = py.display.set_mode((width, height))
py.display.set_caption("2d Physics Engine")

clock = py.time.Clock() #initialise clock


# initialise physics vars
g = 980 # initialise gravity
restitution = 0.9 # 1 = perfectly elastic, 0 = no bounce at all
rest_threshold = 15 # below this speed on impact, the ball is considered at rest
friction = 0.01

#initialise circle vars
radius = 50
floor = height - radius
ceiling = 0 + radius

left_wall = 0 + radius
right_wall = width - radius
a, b = 400, ceiling # initial positions
x, y = a, b # will be used to control the objects movement and position
vel_y = 0.0 # y velocity of the object
vel_x = 0.0 # x velocity of the object

#set boundaries
mouse_x, mouse_y = 0, 0
pressed = False
running = True # initialise loop
final_x, final_y = 0, 0

dx, dy = 0, 0 # store change in mouse position while dragging 
while running:

    delta_time = clock.tick(120) / 1000.0

    #get all the events, such as key press, quit, etc.
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    pressed = py.mouse.get_pressed()[0] # constantly check if the mouse button is pressed or not

    mouse_x, mouse_y = py.mouse.get_pos()

    # add a hitbox around the physics object, to do this, check if the mouse is on the circle or not
    if mouse_x > x - radius and mouse_x < x + radius and mouse_y > y - radius and mouse_y < y + radius and pressed: # start drag
        while pressed:
            py.event.pump() # lets pygame refresh the mouse state
            pressed = py.mouse.get_pressed()[0] # re-check the button so the loop can end
            final_x, final_y = py.mouse.get_pos()
            clock.tick(120) # keeps the time spent dragging out of delta_time. Basically pauses the ball temporarily.

        dx, dy = final_x - x, final_y - y # moved inside the if, so it runs once per release
        if dx != 0 or dy != 0:
            if (y == floor and dy < 0) or (y == ceiling and dy > 0):
                dy = 0
            if (x == right_wall and dx < 0) or (x == left_wall and dx > 0):
                dx = 0
            vel_y = -dy*10 
            vel_x = -dx*10

    #adding horizontal movement
    if vel_x != 0 and y == floor or y == ceiling:
        vel_x -= vel_x*friction
    x += vel_x * delta_time

    vel_x 
    #adding gravity
    vel_y += g * delta_time # constantly pull object towards the floor
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
    #wall collision and rebound
    if x >= right_wall or x <= left_wall:
        if x >= right_wall:
            x = right_wall # snap back so the object never goes beyond the right wall
        elif x <= left_wall:
            x = left_wall # snap back so the object never goes beyond the left wall
        vel_x = -vel_x * restitution # reverse direction and lose some energy

        if abs(vel_x) < rest_threshold: # stop tiny endless micro-bounces
            vel_x = 0.0
    screen.fill((0, 0, 0))

    #using pygame.draw to draw a physics shape (a rigid body)
    py.draw.circle(screen, (255, 255, 255), (int(x), int(y)), radius)

    py.display.flip()

py.quit()
print("Quit")
