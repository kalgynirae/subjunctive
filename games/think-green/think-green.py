import os.path

import sdl2
import sdl2.ext

import subjunctive

subjunctive.add_path(os.path.dirname(__file__))

class DeathError(Exception):
    pass

class Planet(subjunctive.world.World):
    background = subjunctive.image('images/green_planet.png')
    grid_offset = (231, 215)
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
        self._window.show()

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
    image = subjunctive.image('images/cursor.png')
    pushable = True

class Hazard(subjunctive.entity.Entity):
    image = subjunctive.image('images/hazard.png')

    def push(self, direction, pusher=None):
        if isinstance(pusher, Neutralize):
            self.world.score += 1000 * int(self.world.combo**1.5)
            self.world.combo += 1
            self.world.remove(pusher)
            self.world.remove(self)
        else:
            raise DeathError

class Neutralize(subjunctive.entity.Entity):
    image = subjunctive.image('images/neutralize.png')
    pushable = True

class PushRedirector(subjunctive.entity.Entity):
    image = subjunctive.image('images/cursor.png')

    def push(self, direction, pusher=None):
        if direction == 'right':
            subjunctive.actions.push(self.world, 'up')
        else:
            subjunctive.actions.move(self.world, self, direction)

class Receptor(subjunctive.entity.Entity):
    images = [subjunctive.image('images/receptor0.png'),
              subjunctive.image('images/receptor4.png'),
              subjunctive.image('images/receptor3.png'),
              subjunctive.image('images/receptor2.png'),
              subjunctive.image('images/receptor1.png')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fuel = 0

    @property
    def image(self):
        return self.images[self.fuel]

    def push(self, direction, pusher=None):
        if isinstance(pusher, Recycle):
            self.fuel += 1
            self.world.score += self.world.combo**2 * 50
            self.world.combo += 1
            if self.fuel == len(self.images):
                self.world.replace(self, Neutralize(self.world))
            self.world.remove(pusher)

class Recycle(subjunctive.entity.Entity):
    image = subjunctive.image('images/recycle.png')
    pushable = True

if __name__ == '__main__':
    sdl2.ext.init()
    world = Planet()
    cursor = Cursor(world, name="John Smith")
    world.setup(cursor)
    world._draw()

    def keydown_callback(direction):
        if direction:
            world.tick(cursor)
            previous_combo = world.combo
            cursor.move(direction)
            if world.combo == previous_combo:
                world.combo = 1

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
            elif event.type == sdl2.SDL_KEYDOWN:
                keydown_callback(subjunctive.KEYBOARD_DIRECTIONS.get(event.key.keysym.sym))
        world._draw()
        sdl2.timer.SDL_Delay(10)
