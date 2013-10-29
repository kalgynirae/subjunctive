import logging

import pyglet

import subjunctive

class Planet(subjunctive.World):
    background = pyglet.resource.image('images/green_planet.png')
    grid_offset = (231, 99)
    grid_size = (22, 22)
    tile_size = (13, 13)
    window_caption = "Think Green"

    def setup(self):
        self.spawn_random(Recycle, 25)
        self.spawn_random(Receptor, 7)
        self.spawn_random(Hazard, 7)

class Cursor(subjunctive.Entity):
    directional = True
    image = pyglet.resource.image('images/cursor.png')
    pushable = True

class Hazard(subjunctive.Entity):
    image = pyglet.resource.image('images/hazard.png')

class Neutralize(subjunctive.Entity):
    image = pyglet.resource.image('images/neutralize.png')
    pushable = True

class Receptor(subjunctive.Entity):
    image = pyglet.resource.image('images/receptor0.png')

class Recycle(subjunctive.Entity):
    image = pyglet.resource.image('images/recycle.png')
    pushable = True

if __name__ == '__main__':
    world = Planet()
    cursor = Cursor(world)
    world.place(cursor, world.center)
    world.setup()
    subjunctive.start(world, cursor)
