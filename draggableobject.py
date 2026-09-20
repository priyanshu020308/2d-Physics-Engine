import pygame as py
from physicsobject import PhysicsObject


class DraggableObject(PhysicsObject):

    def handle_drag(self, screen, clock):
        pressed = py.mouse.get_pressed()[0] # constantly check if the mouse button is pressed or not

        mouse_x, mouse_y = py.mouse.get_pos()

        # add a hitbox around the physics object, to do this, check if the mouse is on the circle or not
        if mouse_x > self.x - self.radius and mouse_x < self.x + self.radius and mouse_y > self.y - self.radius and mouse_y < self.y + self.radius and pressed: # start drag
            while pressed:
                py.event.pump() # lets pygame refresh the mouse state
                pressed = py.mouse.get_pressed()[0] # re-check the button so the loop can end
                final_x, final_y = py.mouse.get_pos()

                screen.fill((0, 0, 0))#keep on refilling the screen and drawing the circle
                py.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
                py.draw.line(screen, (225, 225, 225), (self.x, self.y), (final_x, final_y), 1)
                py.display.flip()

                clock.tick(120) # keeps the time spent dragging out of delta_time. Basically pauses the ball temporarily.

            dx, dy = final_x - self.x, final_y - self.y # moved inside the if, so it runs once per release
            if dx != 0 or dy != 0:
                if (self.y == self.floor and dy < 0) or (self.y == self.ceiling and dy > 0):
                    dy = 0
                if (self.x == self.right_wall and dx < 0) or (self.x == self.left_wall and dx > 0):
                    dx = 0
                self.vel_y = -dy*10
                self.vel_x = -dx*10