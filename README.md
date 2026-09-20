# 2D Physics Engine

A small 2D physics engine written from scratch in Python using **PyGame** and the built-in **math** module. It is a learning project: the goal is to understand how physics engines actually work under the hood by building one step by step, using the programming knowledge I already have instead of reaching for an existing physics library.

At the moment the engine simulates a single ball that you can grab, pull back, and throw around the window. It falls under gravity, bounces off the walls, floor and ceiling, loses energy on every bounce, and slows down from friction when it rolls along a surface.

## Features

- **Gravity:** a constant downward acceleration pulls the ball toward the floor.
- **Bouncing (restitution):** the ball reverses direction when it hits a boundary and keeps only part of its speed, controlled by a single `restitution` value.
- **Resting threshold:** when a bounce becomes very small, the ball is set to rest so it does not jitter forever.
- **Friction:** horizontal speed gradually drops while the ball is in contact with the floor or ceiling.
- **Drag-and-throw:** click and hold on the ball, drag the mouse, and release to launch it. The ball flies in the opposite direction of your drag, like a slingshot, and a longer drag means a faster throw.
- **Frame-rate independent movement:** motion is scaled by `delta_time`, so the simulation speed does not depend on how fast the computer runs.
- **Object-oriented structure:** physics lives in a `PhysicsObject` class, and mouse dragging is added by a `DraggableObject` subclass, so new kinds of objects can be built on the same base.

## Getting Started

### Requirements

- Python 3 (developed on Python 3.14)
- PyGame (developed with `pygame-ce`)

### Install and run

```bash
pip install pygame-ce
python physicsengine.py
```

The original `pygame` package also works on Python versions it supports (`pip install pygame`). Keep all the `.py` files in the same folder and run only `physicsengine.py`. Close the window to quit.

### Controls

| Action | Result |
| --- | --- |
| Click and hold on the ball | Start dragging; a line shows the pull |
| Move the mouse while holding | Aim and set the strength of the throw |
| Release the mouse button | Launch the ball opposite to the drag direction |

## How It Works

This section explains the ideas behind the code, since understanding them is the point of the project.

### The game loop

Everything runs inside one `while` loop in `physicsengine.py`. Each pass of the loop is one frame: read input, update the physics, then draw the result. The loop is capped at 120 frames per second with `clock.tick(fps)`.

### Delta time

`clock.tick()` returns how many milliseconds passed since the last frame. Dividing by 1000 gives `delta_time` in seconds. Every change in position or velocity is multiplied by `delta_time`, so the ball moves the same distance per real second no matter what the frame rate is.

### Integrating motion

Each frame follows the same two steps inside `PhysicsObject.update`:

```python
self.vel_y += g * delta_time    # acceleration changes velocity
self.y += self.vel_y * delta_time    # velocity changes position
```

Velocity is updated first and the new velocity is then used to move the object. This approach is known as semi-implicit (or symplectic) Euler integration. It is simple and stays stable for this kind of simulation.

### Collisions and restitution

When the ball reaches a boundary, its position is snapped back inside the window so it never sinks through the floor or walls. Then its velocity on that axis is flipped and multiplied by `restitution`:

```python
self.vel_y = -self.vel_y * restitution
```

A restitution of `1` is a perfectly elastic bounce and `0` means no bounce at all. This project uses `0.7`, so the ball keeps 70% of its speed after each impact.

### Friction

While the ball touches the floor or ceiling, a small fraction of its horizontal velocity is removed every frame:

```python
self.vel_x -= self.vel_x * friction
```

This makes it slow down and eventually stop instead of sliding forever.

### Dragging and throwing

`DraggableObject.handle_drag` checks whether the mouse is pressed inside the ball's hitbox. If it is, the program enters a small drag loop that redraws the ball and a line to the cursor. While this loop runs, the normal physics is paused. On release, the difference between the cursor position and the ball position becomes the launch velocity:

```python
self.vel_x = -dx * 10
self.vel_y = -dy * 10
```

The negative sign sends the ball the opposite way from the drag, and the multiplier of `10` sets how strong the throw feels.

## Adjustable Settings

These variables in `settings.py` are worth experimenting with to see how each one changes the behaviour:

| Variable | Default | What it does |
| --- | --- | --- |
| `g` | `980` | Gravity in pixels per second squared |
| `restitution` | `0.7` | Bounciness, from 0 (no bounce) to 1 (perfectly elastic) |
| `rest_threshold` | `15` | Impact speed below which the ball stops bouncing |
| `friction` | `0.01` | Fraction of horizontal speed lost per frame on a surface |
| `width`, `height` | `1500`, `1000` | Size of the window |
| `fps` | `120` | Frame rate cap of the main loop |

The size of the ball is set by `self.radius` (default `50`) in `PhysicsObject`.

## Known Limitations

Being honest about what is not finished is part of learning, so here is what I already know needs work:

- The mouse hitbox is a square around the ball rather than a true circle, so clicking in the corners of that square still grabs it.
- Friction is applied once per frame, which means it is slightly dependent on the frame rate. Scaling it by `delta_time` would fix that.
- Dragging uses a blocking loop that redraws only the dragged object, so other objects would freeze and disappear while you drag one. It needs to become a non-blocking drag state before a second object is added.
- Only one object exists, so there are no collisions between objects yet.

## Roadmap

- [x] Gravity, boundary collisions, and bounce
- [x] Friction on surfaces
- [x] Drag-and-throw with the mouse
- [x] Refactor into a reusable physics object class, with a draggable subclass
- [x] Remove the leftover mouse-position debug list
- [ ] Give each object its own mass, independent of its size
- [ ] Add more shapes: rectangles, triangles, and others
- [ ] Object-to-object collision detection and response

## Versions

- **v1.1.0:** Split the single script into separate files and classes (`PhysicsObject`, `DraggableObject`, `settings.py`). Behaviour is unchanged.
- **v1.0.0:** First release. A single ball with gravity, bouncing, friction, and drag-and-throw, all in one file.

## Project Structure

```
.
├── physicsengine.py    # entry point: window setup and the main game loop
├── settings.py         # shared constants: window size, gravity, restitution, friction
├── physicsobject.py    # PhysicsObject: gravity, collisions, friction, drawing
├── draggableobject.py  # DraggableObject: adds mouse drag-and-throw
└── README.md
```

## Built With

- [Python](https://www.python.org/)
- [PyGame](https://www.pygame.org/) for the window, input, and drawing
- The `math` module from the standard library

## Why I Built This

I wanted a hands-on way to learn how physics engines work, so I am building one myself and adding to it one concept at a time. Every feature here, from gravity to restitution to friction, comes from working out the idea, writing it in plain Python, and watching what happens on screen.

## License

MIT License

Copyright (c) 2026 Priyanshu_0203
