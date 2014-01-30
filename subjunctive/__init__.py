import os.path
import sys

import sdl2
import sdl2.ext

from . import entity
from . import world

KEYBOARD_DIRECTIONS = {sdl2.SDLK_LEFT: 'left',
                       sdl2.SDLK_DOWN: 'down',
                       sdl2.SDLK_UP: 'up',
                       sdl2.SDLK_RIGHT: 'right'}

_paths = [os.path.dirname(__file__)]

def add_path(path):
    _paths.append(path)

def image(name):
    for path in _paths:
        try:
            surface = sdl2.ext.load_image(os.path.join(path, name))
        except sdl2.ext.common.SDLError:
            pass
        else:
            return surface
    raise KeyError("image %r could not be found" % name)
