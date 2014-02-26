import sdl2
import sdl2.ext

from . import grid
from . import entity
from . import resource
from . import world

class SubjunctiveExit(Exception):
    pass

def exit(*args, **kwargs):
    raise SubjunctiveExit

window = None
def run(world, *, on_direction=None, on_select=None):
    global window
    if window is None:
        if world.background is not None:
            width = world.background.w
            height = world.background.h
        else:
            width = world.grid.width * world.tile_size[0]
            height = world.grid.height * world.tile_size[1]
        window = sdl2.ext.Window(world.window_title, (width, height))
        window.show()

    try:
        while True:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    raise KeyboardInterrupt
                elif event.type == sdl2.SDL_KEYDOWN:
                    sym = event.key.keysym.sym
                    if on_direction is not None:
                        direction = grid.KEYBOARD.get(sym)
                        if direction is not None:
                            on_direction(direction)
                    if on_select is not None:
                        if sym in [sdl2.SDLK_RETURN, sdl2.SDLK_SPACE]:
                            on_select()
            world._draw(window)
            sdl2.timer.SDL_Delay(20)
    except SubjunctiveExit:
        pass

sdl2.ext.init()
