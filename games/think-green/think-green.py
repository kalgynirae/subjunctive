import pyglet

import subjunctive

class DeathError(Exception):
    pass

class Planet(subjunctive.world.World):
    background = pyglet.resource.image('images/green_planet.png')
    grid_offset = (231, 99)
    grid_size = (22, 22)
    score_offset = (600, 40)
    tile_size = (13, 13)
    window_caption = "Think Green"

    def __init__(self):
        super().__init__()
        self.combo = 1
        self.score = 100
        self.tick_count = 0

    def setup(self, cursor):
        self.place(cursor, self.center)
        self.spawn_random(Recycle, number=25, avoid=self.center, edges=False)
        self.spawn_random(Receptor, number=7, avoid=self.center, edges=False)
        self.spawn_random(Hazard, number=7, avoid=self.center, edges=False)

    def tick(self, cursor):
        self.score -= 1
        self.tick_count += 1
        tc = self.tick_count ** 0.45
        cursor_loc = self.locate(cursor)
        if (self.tick_count % ((tc + 250) // tc) == 0 or
                self.count(Recycle) < 5):
            self.spawn_random(Recycle, avoid=cursor_loc, edges=False)
        if (self.tick_count % ((tc + 900) // tc) == 0 or
                self.count(Receptor) < 1):
            self.spawn_random(Receptor, avoid=cursor_loc, edges=False)
        if (self.tick_count % ((tc + 700) // tc) == 0 or
                self.count(Hazard) < 1):
            self.spawn_random(Hazard, avoid=cursor_loc, edges=False)

class Cursor(subjunctive.entity.Entity):
    directional = True
    image = pyglet.resource.image('images/cursor.png')
    pushable = True

class Hazard(subjunctive.entity.Entity):
    image = pyglet.resource.image('images/hazard.png')

    def respond_to_push(self, direction, pusher, world):
        if isinstance(pusher, Neutralize):
            world.score += 1000 * int(world.combo**1.5)
            world.combo += 1
            world.remove(pusher)
            world.remove(self)
        else:
            raise DeathError

class Neutralize(subjunctive.entity.Entity):
    image = pyglet.resource.image('images/neutralize.png')
    pushable = True

class PushRedirector(subjunctive.entity.Entity):
    image = pyglet.resource.image('images/cursor.png')

    def respond_to_push(self, direction, pusher, world):
        if direction == 'right':
            push(world, 'up')
        else:
            subjunctive.actions.move(world, self, direction)

class Receptor(subjunctive.entity.Entity):
    images = [pyglet.resource.image('images/receptor0.png'),
              pyglet.resource.image('images/receptor4.png'),
              pyglet.resource.image('images/receptor3.png'),
              pyglet.resource.image('images/receptor2.png'),
              pyglet.resource.image('images/receptor1.png')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fuel = 0

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, fuel):
        self._fuel = fuel
        self.image = self.images[fuel]

    def respond_to_push(self, direction, pusher, world):
        if isinstance(pusher, Recycle):
            self.fuel += 1
            world.score += world.combo**2 * 50
            world.combo += 1
            if self.fuel == len(self.images):
                world.replace(self, Neutralize(world))
            world.remove(pusher)

class Recycle(subjunctive.entity.Entity):
    image = pyglet.resource.image('images/recycle.png')
    pushable = True

if __name__ == '__main__':
    world = Planet()
    cursor = Cursor(world, name="John Smith")
    world.setup(cursor)

    @world.event
    def on_text_motion(motion):
        world.tick(cursor)
        previous_combo = world.combo
        direction = subjunctive.KEYBOARD_DIRECTIONS.get(motion, False)
        if direction:
            world.push(cursor, direction)
        if world.combo == previous_combo:
            world.combo = 1

    try:
        pyglet.app.run()
    except DeathError:
        print("You died.")
