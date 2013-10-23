import argparse

import subjunctive

class Player(subjunctive.Entity): pass

class World(subjunctive.World):
    grid_size = (8, 8)
    tile_size = (16, 16)
    window_caption = "Floorpaint"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("level_file")
    args = parser.parse_args()

    world = World.load(args.level_file, 'levels/definitions.txt')
    subjunctive.start_game_with_keyboard_controlled_cursor(world, Player())
