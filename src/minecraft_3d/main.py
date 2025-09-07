from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Create a cube
cube = Entity(model='cube', color=color.orange, scale=(2,2,2))

# Add a first person controller
player = FirstPersonController()

app.run()
