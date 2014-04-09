from collections import namedtuple
from enum import Enum

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.Location = _location_class(self, ['x', 'y'])

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield self.Location(x, y)

    @property
    def bottom_left(self):
        return self.Location(self.height - 1, 0)

    @property
    def bottom_right(self):
        return self.Location(self.height - 1, self.width - 1)

    @property
    def center(self):
        return self.Location(self.width // 2, self.height // 2)

    @property
    def top_left(self):
        return self.Location(0, 0)

    @property
    def top_right(self):
        return self.Location(0, self.width - 1)


class PolarGrid:
    def __init__(self, radius, slices):
        self.radius = radius
        self.slices = slices
        self.Location = _location_class(self, ['r', 's'])

    def __iter__(self):
        for r in range(self.r):
            for s in range(self.c):
                yield self.Location(r, c)

    def adjacent(self, location, direction):
        r, s = location
        r += direction.dr
        s += direction.ds
        return self.Location(r, s)

    def valid_coordinates(self, r, s):
        return 0 <= r < self.radius and 0 <= s < self.slices

    class Direction(Enum):
        cw = (0, -1)
        ccw = (0, 1)
        in_ = (-1, 0)
        out = (1, 0)

        def __init__(self, dr, ds):
            self.dr = dr
            self.ds = ds

    def Location(self, r, s):
        return self._Location(self, r, s)

def _location_class(grid, parameters):
    if len(parameters) < 1:
        raise ValueError("Must have at least one parameter")
    actual_params = ['__%s' % name for name in parameters]
    parameter_list = ", ".join(name for name in parameters)

    class_definition = _location_class_template.format(
        parameters = parameters,
        actual_params = actual_params,
        parameter_list = parameter_list,
    )
    d = {'grid': grid}
    exec(class_definition, d)
    return d['Location']

_location_class_template = """
class Location:
    #__slots__ = {actual_params!r}

    def __eq__(self, other):
        return all(getattr(self, name) == getattr(other, name)
                   for name in {parameters!r})

    def __hash__(self):
        return hash(tuple(getattr(self, name) for name in {parameters!r}))

    def __init__(self, {parameter_list}):
        if not grid.valid_coordinates({parameter_list}):
            raise OutOfBounds
        for name in {parameters!r}:
            setattr(self, '__%s' % name, locals()[name])

    def __iter__(self):
        yield from (getattr(self, name) for name in {parameters!r})

    def __repr__(self):
        return 'Location(%s)'.format(', '.join(
                '%s=%s' % (name, getattr(self, name))
                for name in {parameters!r}))

    def __getattr__(self, name):
        if name in {parameters!r}:
            return getattr(self, '__%s' % name)
        else:
            raise AttributeError

    def adjacent(self, direction):
        return grid.adjacent(self, direction)

Location.__qualname__ = grid.__class__.__qualname__ + '.Location'
"""


class OutOfBounds(Exception):
    pass
