from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

class Block(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = 'grass',
            color = color.hsv(0,0,random.uniform(0.9,1.0)),
            highlight_color = color.lime,
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            if key == 'right mouse down':
                block = Block(position = self.position + mouse.normal)

for z in range(20):
    for x in range(20):
        block = Block(position=(x,0,z))

player = FirstPersonController(y=2, origin_y=-.5)

app.run()
