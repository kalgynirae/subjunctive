import os.path
import sys

import sdl2
import sdl2.ext

from . import actions
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

def run(window, keydown_callback):
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
            elif event.type == sdl2.SDL_KEYDOWN:
                keydown_callback(KEYBOARD_DIRECTIONS.get(event.key.keysym.sym))
        window._draw()
        sdl2.timer.SDL_Delay(10)
