# 2D Physics Engine

A 2D physics engine built from scratch in **Python** using **Pygame**.

This project started as a simple experiment with gravity and a bouncing circle and is being developed incrementally to understand how real-time physics simulation works under the hood.

Rather than relying on an existing physics engine, the goal is to implement the fundamental physics systems manually and understand the mathematics and programming behind them.

> **Status:** Work in progress — this repository currently represents the version of the engine developed up to the implementation of friction and mouse-based dragging.

---

## Features

The current version includes:

* Gravity
* Delta-time based movement
* Vertical acceleration and velocity
* Floor and ceiling collisions
* Left and right wall collisions
* Restitution / bounciness
* Resting threshold to prevent endless micro-bounces
* Horizontal movement
* Friction while touching horizontal surfaces
* Mouse-based dragging and launching
* Boundary-aware dragging
* Real-time simulation using Pygame

---

## How It Works

The engine uses a simple real-time physics loop.

Each frame, the program:

1. Calculates the time elapsed since the previous frame.
2. Applies gravity to the object's vertical velocity.
3. Updates the object's position using its velocity.
4. Checks for collisions with the floor and ceiling.
5. Checks for collisions with the left and right walls.
6. Applies friction when the object is touching a horizontal surface.
7. Updates horizontal position.
8. Handles mouse interaction.
9. Draws the object to the screen.

The basic structure is:

```text
Acceleration
     ↓
Velocity
     ↓
Position
     ↓
Collision Detection
     ↓
Collision Response
     ↓
Friction
     ↓
Rendering
```

---

## Physics

### Gravity

Gravity is represented as an acceleration:

```python
g = 980
```

The engine uses delta time so that movement is based on elapsed time rather than simply applying a fixed amount every frame.

Vertical velocity is updated using:

```python
vel_y += g * delta_time
```

The position is then updated using:

```python
y += vel_y * delta_time
```

This gives the object progressively increasing downward velocity as it falls.

The value `980` is treated as approximately **980 pixels per second squared**, rather than being interpreted as literal meters per second squared.

---

### Delta Time

The engine uses Pygame's clock to calculate delta time:

```python
delta_time = clock.tick(120) / 1000.0
```

The value is converted from milliseconds to seconds.

Using delta time allows the physics calculations to operate in terms of time rather than assuming that every frame takes exactly the same amount of time.

---

### Collision With Boundaries

The object has four boundaries:

* Floor
* Ceiling
* Left wall
* Right wall

For example:

```python
floor = height - radius
ceiling = radius
left_wall = radius
right_wall = width - radius
```

When the object reaches a boundary, its position is corrected so that it cannot move outside the playable area.

For example, when the object reaches the floor:

```python
if self.y >= self.floor:
    self.y = self.floor
```

The velocity is then reversed to produce a bounce.

---

### Restitution

Restitution controls how much velocity is retained after a collision.

The current value is:

```python
restitution = 0.9
```

The basic collision response is:

```python
vel_y = -vel_y * restitution
```

A restitution of:

```text
1.0 → perfectly elastic bounce
0.0 → no bounce
0.9 → retains most of its velocity
```

The same concept is applied to horizontal wall collisions.

---

### Rest Threshold

Without a stopping condition, an object can continue making extremely small bounces indefinitely.

To prevent this, the engine uses:

```python
rest_threshold = 15
```

If the velocity after a collision becomes smaller than this threshold, it is set to zero:

```python
if abs(vel_y) < rest_threshold:
    vel_y = 0.0
```

This allows objects to eventually come to rest instead of continuously performing tiny numerical bounces.

---

### Friction

Friction is currently implemented as horizontal velocity damping when the object is touching the floor or ceiling.

```python
if self.vel_x != 0 and (self.y == self.floor or self.y == self.ceiling):
    self.vel_x -= self.vel_x * friction
```

The current friction value is:

```python
friction = 0.01
```

This gradually reduces horizontal velocity while the object is in contact with a horizontal surface.

The current implementation is intentionally simple and is not intended to be a complete physical friction model.

---

## Mouse Interaction

The engine also allows the object to be grabbed with the mouse.

When the mouse is pressed while inside the object's hitbox, the program enters a temporary dragging state.

The object's movement is paused while it is being dragged.

When the mouse button is released, the difference between the original object position and the final mouse position is used to determine the launch velocity.

Conceptually:

```text
Grab object
     ↓
Move mouse
     ↓
Release
     ↓
Calculate displacement
     ↓
Convert displacement into velocity
     ↓
Launch object
```

This creates a simple slingshot-style interaction.

The direction is inverted when converting the mouse displacement into velocity so that pulling the object in one direction launches it in the opposite direction.

---

## Boundary-Aware Dragging

The dragging system also checks whether the object is already touching a boundary.

For example, if the object is against the floor, dragging it further downward should not generate a downward launch velocity.

The engine therefore prevents certain components of the launch vector when the object is already constrained by a boundary.

This helps prevent the mouse interaction from immediately attempting to launch the object through a wall or outside the simulation area.

---

## Project Structure

The current project is contained in a single Python file.

The main components are:

```text
2D Physics Engine
│
├── Pygame initialization
├── Physics constants
├── Physics object
│   ├── Position
│   ├── Velocity
│   ├── Gravity
│   ├── Boundary collisions
│   ├── Restitution
│   └── Friction
│
├── Draggable object
│   └── Mouse interaction
│
└── Main simulation loop
    ├── Input
    ├── Physics update
    └── Rendering
```

The code is intentionally kept relatively simple while the underlying concepts are being learned.

---

## Technologies

### Python

The main programming language used to build the engine.

### Pygame

Used for:

* Creating the window
* Drawing the physics object
* Reading mouse input
* Handling events
* Controlling the simulation clock

### Math

Python's built-in `math` module is used for mathematical calculations.

---

## Running the Project

### Requirements

You need:

* Python 3
* Pygame

Install Pygame with:

```bash
pip install pygame
```

Then run the Python file:

```bash
python physics_engine.py
```

A Pygame window should open containing the physics simulation.

---

## Controls

### Mouse

**Click and hold** the physics object to grab it.

**Move the mouse** to position the object.

**Release the mouse button** to launch the object based on the dragging direction and distance.

---

## Current Limitations

This is an early-stage physics engine, so there are several intentional limitations.

Currently:

* The engine primarily handles a single circular physics object.
* There is no object-to-object collision system yet.
* There are no different shapes or rigid-body geometries.
* Rotation is not implemented.
* There is no angular velocity.
* Friction is represented using a simple velocity damping model.
* Collision detection is based on the simulation's discrete updates.
* The physics system is not intended to be a physically accurate replacement for established physics engines.

These limitations are part of the development process rather than bugs that the project is currently attempting to solve all at once.

---

## Development Philosophy

The main purpose of this project is **learning by implementation**.

Instead of starting with a complete physics library and attempting to understand it afterward, the engine is being developed one concept at a time.

The progression began with a basic falling object and gradually introduced:

```text
Basic movement
      ↓
Gravity
      ↓
Delta time
      ↓
Floor collision
      ↓
Bouncing
      ↓
Wall & ceiling collisions
      ↓
Rest threshold
      ↓
Mouse interaction
      ↓
Dragging / launching
      ↓
Friction
```

Each addition introduces another concept involved in real-time physics simulation.

The project will continue to evolve as more concepts are understood and implemented.

---

## Future Development

Possible future additions include:

* Multiple physics objects
* Object-to-object collision detection
* Collision impulses
* Mass
* Momentum
* Different shapes
* Better collision resolution
* Forces
* Improved friction
* Static objects
* Rotation
* Angular velocity
* Torque
* More advanced rigid-body physics
* Performance improvements
* More accurate numerical integration

The exact direction will depend on what I want to explore next.

---

## Disclaimer

This project is primarily an **educational and experimental implementation of 2D physics**.

It is not intended to compete with established physics engines such as Box2D or Chipmunk.

The purpose is to understand the concepts behind physics simulation by building them from the ground up.
