import logging

import pyglet

import subjunctive

class DeathError(Exception):
    pass

class Planet(subjunctive.World):
    background = pyglet.resource.image('images/green_planet.png')
    grid_offset = (231, 99)
    grid_size = (22, 22)
    tile_size = (13, 13)
    window_caption = "Think Green"

    def __init__(self):
        super().__init__()
        self.score = 0
        self.tick_count = 0

    def setup(self):
        self.spawn_random(Recycle, 25)
        self.spawn_random(Receptor, 7)
        self.spawn_random(Hazard, 7)

    def spawn_stuff(self):
        # This should run everytime an action happens. Dunno if that's actually
        # what Pyglet thinks it does, though.
        self.score -= 1
        self.tick_count += 1
        logging.debug("Grid.tick_count={}".format(self.tick_count))
        tc = self.tick_count ** 0.45
        if (self.tick_count % ((tc + 250) // tc) == 0 or
                self.count(Recycle) < 5):
            self.spawn_random(Recycle)
        if (self.tick_count % ((tc + 900) // tc) == 0 or
                self.count(Receptor) < 1):
            self.spawn_random(Receptor)
        if (self.tick_count % ((tc + 700) // tc) == 0 or
                self.count(Hazard) < 1):
            self.spawn_random(Hazard)

class Cursor(subjunctive.Entity):
    directional = True
    image = pyglet.resource.image('images/cursor.png')
    pushable = True

class Hazard(subjunctive.Entity):
    image = pyglet.resource.image('images/hazard.png')

    def respond_to_push(self, direction, pusher):
        if isinstance(pusher, Neutralize):
            raise Vanish
        raise DeathError

class Neutralize(subjunctive.Entity):
    image = pyglet.resource.image('images/neutralize.png')
    pushable = True

class Receptor(subjunctive.Entity):
    images = [pyglet.resource.image('images/receptor0.png'), 
              pyglet.resource.image('images/receptor4.png'),
              pyglet.resource.image('images/receptor3.png'), 
              pyglet.resource.image('images/receptor2.png'),
              pyglet.resource.image('images/receptor1.png')]

    def __init__(self):
        super().__init__()
        self.fuel = 0

    @property
    def image(self):
        return self.images[self.fuel]

class Recycle(subjunctive.Entity):
    image = pyglet.resource.image('images/recycle.png')
    pushable = True

if __name__ == '__main__':
    world = Planet()
    cursor = Cursor()
    world.place(cursor, world.center)
    world.setup()
    subjunctive.start(world, cursor)
