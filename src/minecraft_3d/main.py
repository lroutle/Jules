from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Create a ground plane
ground = Entity(model='plane', scale=(100, 1, 100), color=color.lime, texture='white_cube', texture_scale=(100,100), collider='box')

# Create a cube
cube = Entity(model='cube', color=color.orange, scale=(2,2,2), position=(5, 1, 5), collider='box')

# Add a first person controller
player = FirstPersonController(y=2, origin_y=-.5)

app.run()
