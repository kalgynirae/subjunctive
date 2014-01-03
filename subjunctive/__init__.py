import pyglet

from . import entity
from . import world

KEYBOARD_DIRECTIONS = {pyglet.window.key.MOTION_LEFT: 'left',
                       pyglet.window.key.MOTION_DOWN: 'down',
                       pyglet.window.key.MOTION_UP: 'up',
                       pyglet.window.key.MOTION_RIGHT: 'right'}
