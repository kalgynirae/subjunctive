import logging
import random

import pyglet
import pyglet.gl as gl

logging.basicConfig(level=logging.DEBUG)

pyglet.resource.path.append('@subjunctive')
pyglet.resource.reindex()

class God:
    __slots__ = []
God = God()

class OutOfBounds(Exception):
    pass

def make_location_class(grid_size):
    """Make a specialized Location class that validates its input

    Instances of the returned class will raise an exception if they are
    constructed with values that are out-of-bounds.

    """
    class Location:
        __slots__ = ['__x', '__y']
        max = grid_size

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

        def __hash__(self):
            return hash((self.x, self.y))

        def __init__(self, x, y):
            if not (isinstance(x, int) and isinstance(y, int)):
                raise TypeError("Location object needs integers")
            if not 0 <= x < self.max[0] or not 0 <= y < self.max[1]:
                raise OutOfBounds
            self.__x = x
            self.__y = y

        def __repr__(self):
            return "Location({}, {})".format(self.x, self.y)

        @property
        def x(self):
            return self.__x

        @property
        def y(self):
            return self.__y

        def adjacent(self, direction):
            if direction == 'left':
                return self.__class__(self.x - 1, self.y)
            elif direction == 'down':
                return self.__class__(self.x, self.y - 1)
            elif direction == 'up':
                return self.__class__(self.x, self.y + 1)
            elif direction == 'right':
                return self.__class__(self.x + 1, self.y)
            else:
                raise ValueError("Invalid direction: {}".format(direction))
    # TODO: do some Python hackery to make the name of this class more helpful
    # Location.__name__ = class_ + '.Location'
    return Location

class World(pyglet.window.Window):
    background = None
    grid_offset = (0, 0)
    grid_size = (16, 16)
    tile_size = (16, 16)
    window_caption = "Subjunctive!"

    @property
    def center(self):
        return self.Location(self.grid_size[0] // 2, self.grid_size[1] // 2)

    def __init__(self):
        if self.background is not None:
            width = self.background.width
            height = self.background.height
        else:
            width = self.grid_size[0] * self.tile_size[0]
            height = self.grid_size[1] * self.tile_size[1]
        super().__init__(width=width, height=height,
                         caption=self.window_caption)

        # Enable rendering with transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.Location = make_location_class(self.grid_size)

        # Construct the list of available locations
        # We're using a set so the lookup time is fast
        # But really we're not sure that a set is the best solution
        self._available_locations = {self.Location(x, y)
                                     for x in range(self.grid_size[0])
                                     for y in range(self.grid_size[1])}
        print(self._available_locations)
        self._entities = {}

    def count(self, entity_type):
        return sum(1 for e in self._entities if isinstance(e, entity_type))

    def on_draw(self):
        if self.background:
            self.background.blit(0, 0)
        for location, entity in self._entities.items():
            entity.image.blit(*self._pixels(location))

    def _pixels(self, location):
        return (location.x * self.tile_size[0] + self.grid_offset[0],
                location.y * self.tile_size[1] + self.grid_offset[1])

    def place(self, entity, location):
        logging.debug("Placing {} at {}".format(entity, location))
        if location in self._entities:
            raise ValueError("Location {} already contains {}"
                             "".format(location, self._entities[location]))
        self._entities[location] = entity
        self._available_locations.remove(location)
        entity._location = location

    def push(self, entity, direction, pusher=God):
        try:
            new_location = entity._location.adjacent(direction)
        except OutOfBounds:
            return False
        do_push = entity.respond_to_push(direction, pusher)
        if do_push and new_location in self._entities:
            do_push = self.push(self._entities[new_location], direction, entity)
        if do_push:
            entity.direction = direction
            self.remove(entity)
            self.place(entity, new_location)
        return do_push

    def remove(self, entity):
        if self._entities[entity._location] is entity:
            del self._entities[entity._location]
            self._available_locations.add(entity._location)
            entity._location = None
        else:
            raise ValueError("Entity {} is not in location {}"
                             "".format(entity, entity._location))

    def spawn_random(self, entity_type, number=1):
        new_entities = []
        for i in range(number):
            location = random.choice(list(self._available_locations))
            e = entity_type()
            self.place(e, location)
            new_entities.append(e)
        return new_entities

class Entity:
    image = pyglet.resource.image('images/default.png')

    pushable = False

    def __init__(self, name="John Smith"):
        self.direction = None
        self.location = None
        self.name = name

    def __str__(self):
        return self.name

    def respond_to_push(self, direction, pusher):
        return self.pushable

def start(world, cursor):
    @world.event
    def on_text_motion(motion):
        directions = {pyglet.window.key.MOTION_LEFT: 'left',
                      pyglet.window.key.MOTION_DOWN: 'down',
                      pyglet.window.key.MOTION_UP: 'up',
                      pyglet.window.key.MOTION_RIGHT: 'right'}
        if directions.get(motion, False):
            world.push(cursor, directions[motion])
    pyglet.app.run()
