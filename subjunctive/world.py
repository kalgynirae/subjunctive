import logging
import random
import sys

import sdl2.ext

class God:
    __slots__ = []
God = God()

class OutOfBounds(Exception):
    pass

def _make_location_class(grid_size):
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

    return Location

class World:
    background = None
    grid_offset = (0, 0)
    grid_size = (8, 8)
    score_offset = None
    tile_size = (16, 16)
    window_title = "Subjunctive!"

    @property
    def center(self):
        return self.Location(self.grid_size[0] // 2, self.grid_size[1] // 2)

    def __init__(self):
        super().__init__()

        if self.background is not None:
            width = self.background.w
            height = self.background.h
        else:
            width = self.grid_size[0] * self.tile_size[0]
            height = self.grid_size[1] * self.tile_size[1]

        # Create a grid-aware Location class
        self.Location = _make_location_class(self.grid_size)
        self.Location.__qualname__ = self.__class__.__qualname__ + ".Location"

        # Set up locations
        self._entities = {self.Location(x, y): None
                          for x in range(self.grid_size[0])
                          for y in range(self.grid_size[1])}

        self.score = 0
        if self.score_offset:
            # Create a score label
            x, y = self.score_offset
            #self.score_label = pyglet.text.Label(
            #    "", bold=True, color=(0, 0, 0, 255), x=x, y=y)

        self._window = sdl2.ext.Window(self.window_title, (width, height))
        self._surface = self._window.get_surface()

    def clear(self):
        self._entities = {self.Location(x, y): None
                          for x in range(self.grid_size[0])
                          for y in range(self.grid_size[1])}

    def count(self, entity_type):
        """Return the number of entity_type entities currently in the world"""
        return sum(1 for e in self._entities.values()
                   if isinstance(e, entity_type))

    @classmethod
    def load(cls, level_file, definitions_file):
        """Part of incomplete level-file-loading code"""
        # TODO: Load definitions from the file
        types = {'-': None, 'a': Entity}

        with open(level_file) as f:
            lines = [line for line in map(str.strip, f) if line != '']

        width, height = len(lines[0]), len(lines)
        world = cls()
        world.grid_size = width, height

        for ny, line in enumerate(lines, start=1):
            y = height - ny
            for x, char in enumerate(line):
                try:
                    entity_type = types[char]
                except KeyError:
                    logging.error("Character {!r} is not defined; ignoring"
                                  "".format(char))
                else:
                    if entity_type:
                        world.place(entity_type(), world.Location(x, y))

        return world

    def locate(self, entity):
        """Return entity's location in the world

        If entity is not in the world, ValueError is raised.
        """
        for location, suspect in self._entities.items():
            if suspect is entity:
                return location
        raise ValueError("{} not in world".format(entity))

    def _draw(self):
        if self.background:
            sdl2.SDL_BlitSurface(self.background, None, self._surface, None)
        # Update the position of each sprite
        for location, entity in self._entities.items():
            if entity:
                w, h = entity.image.w, entity.image.h
                x, y = self._pixels(location)
                #if s.rotation == 90:
                #    y += s.surface.h
                #elif s.rotation == 180:
                #    x += s.surface.w
                #    y += s.surface.h
                #elif s.rotation == 270:
                #    x += s.surface.w
                #s.position = (x, y)
                sdl2.SDL_BlitSurface(entity.image, None, self._surface,
                                     sdl2.SDL_Rect(x, y, w, h))

        # Draw the score
        #if self.score_offset:
        #    self.score_label.text = str(self.score)
        #    self.score_label.draw()
        self._window.refresh()

    def _pixels(self, location):
        return (location.x * self.tile_size[0] + self.grid_offset[0],
                location.y * self.tile_size[1] + self.grid_offset[1])

    def place(self, entity, location):
        """Place entity at location

        If there is already an entity at location, ValueError is raised.
        """
        logging.debug("Placing {} at {}".format(entity, location))
        if self._entities[location] is not None:
            raise ValueError("Location {} already contains {}"
                             "".format(location, self._entities[location]))
        self._entities[location] = entity

    def push(self, entity, direction, pusher=God):
        """Push entity in the given direction"""
        entity.respond_to_push(direction, pusher, self)

    def _read_level(self, path):
        """Part of incomplete level-file-loading code"""
        columns = []
        with open(path, "r") as leveltext_file:
            rows = leveltext_file.read().splitlines()
            for i in rows:
                columns.append(i.split())
        return rows, columns

    def remove(self, entity):
        """Remove entity from the world

        If entity is not in the world, ValueError is raised.
        """
        location = self.locate(entity)
        self._entities[location] = None
        return location

    def replace(self, entity, new_entity):
        """Replace entity with new_entity

        If entity is not in the world, ValueError is raised.
        """
        location = self.remove(entity)
        self.place(new_entity, location)

    def _place_objects(self, obj_list, rows, columns):
        """Part of incomplete level-file-loading code"""
        for ly, i in enumerate(rows):
            for lx, j in enumerate(columns[ly]):
                try:
                    e = obj_list[j]()
                    self.place(e, self.Location(lx,self.grid_size[1]-ly-1))
                except KeyError:
                    pass

    def spawn_random(self, entity_type, number=1, avoid=None, edges=True):
        """Spawn number new entity_types at random locations

        If avoid is an entity, new entities will not spawn in the same row or
        column as that entity.

        If edges is True, entities can spawn on the edges of the board.
        """
        logging.debug("Spawning {} {}s".format(number, entity_type))
        invalid_x, invalid_y = [], []
        if avoid:
            invalid_x.append(avoid.x)
            invalid_y.append(avoid.y)
        if not edges:
            gx, gy = self.grid_size
            invalid_x += [0, gx - 1]
            invalid_y += [0, gy - 1]
        available_locations = [loc for loc, entity in self._entities.items()
                               if not entity and loc.x not in invalid_x
                                             and loc.y not in invalid_y]
        new_entities = []
        for _ in range(number):
            if not available_locations:
                break
            location = random.choice(available_locations)
            entity = entity_type(self)
            self.place(entity, location)
            new_entities.append(entity)
            available_locations.remove(location)
        return new_entities

if '--debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
