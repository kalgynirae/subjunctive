import os.path

import sdl2
import sdl2.ext

import subjunctive

subjunctive.resource.add_path(os.path.dirname(__file__))

class DeathError(Exception):
    pass

class Planet(subjunctive.world.World):
    background = subjunctive.resource.image('images/green_planet.png')
    dead_background = subjunctive.resource.image('images/red_planet.png')
    grid = subjunctive.grid.Grid(22, 22)
    grid_offset = (231, 215)
    score_offset = (600, 40)
    tile_size = (13, 13)
    window_title = "Think Green"

    def __init__(self):
        super().__init__()
        self.combo = 1
        self.score = 100
        self.tick_count = 0

    def die(self):
        self.background = self.dead_background

    def setup(self, cursor):
        self.place(cursor, self.grid.center)
        self.spawn_random(Recycle, number=25, avoid=self.grid.center,
                          edges=False)
        self.spawn_random(Receptor, number=7, avoid=self.grid.center,
                          edges=False)
        self.spawn_random(Hazard, number=7, avoid=self.grid.center,
                          edges=False)

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

class TitleScreen(subjunctive.world.World):
    background = subjunctive.resource.image('images/title.png')

class Cursor(subjunctive.entity.Entity):
    image = subjunctive.entity.directional(
                up=subjunctive.resource.image('images/cursor-up.png'),
                down=subjunctive.resource.image('images/cursor-down.png'),
                left=subjunctive.resource.image('images/cursor-left.png'),
                right=subjunctive.resource.image('images/cursor-right.png'))

class Death(subjunctive.entity.Entity):
    image = subjunctive.resource.image('images/death.png')

class Hazard(subjunctive.entity.Entity):
    image = subjunctive.resource.image('images/hazard.png')

    def push(self, direction, pusher=None):
        if isinstance(pusher, Neutralize):
            self.world.score += 1000 * int(self.world.combo**1.5)
            self.world.combo += 1
            self.world.remove(pusher)
            self.world.remove(self)
        else:
            self.world.replace(self, Death(self.world))
            raise DeathError

class Neutralize(subjunctive.entity.Entity):
    image = subjunctive.resource.image('images/neutralize.png')
    pushable = True

class Receptor(subjunctive.entity.Entity):
    images = [subjunctive.resource.image('images/receptor0.png'),
              subjunctive.resource.image('images/receptor4.png'),
              subjunctive.resource.image('images/receptor3.png'),
              subjunctive.resource.image('images/receptor2.png'),
              subjunctive.resource.image('images/receptor1.png')]

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
    image = subjunctive.resource.image('images/recycle.png')
    pushable = True

if __name__ == '__main__':
    subjunctive.run(TitleScreen(), on_select=subjunctive.exit)

    while True:
        world = Planet()
        cursor = Cursor(world, name="John Smith")
        world.setup(cursor)

        def move_cursor(direction):
            world.tick(cursor)
            previous_combo = world.combo
            cursor.move(direction, orient=True)
            if world.combo == previous_combo:
                world.combo = 1

        try:
            subjunctive.run(world, on_direction=move_cursor)
        except DeathError:
            world.die()
            subjunctive.run(world, on_select=subjunctive.exit)
