import argparse

import subjunctive

class Player(subjunctive.entity.Entity):
    def move(self, *args, **kwargs):
        try:
            new_location = self.world.locate(self).adjacent(direction)
        except grid.OutOfBounds:
            return
        try:
            self.world.place(self, new_location)
        except ValueError:
            return

class Wall(subjunctive.entity.Entity):
    pass

class World(subjunctive.world.World):
    tile_size = (16, 16)
    window_caption = "Floorpaint"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("level_file")
    args = parser.parse_args()

    definitions = {'o': Player, 'b': Wall, '-': None}
    world = World.load(args.level_file, definitions)
    player = Player(world)
    world.place(player, world.center)

    def move_player(direction):
        player.move(direction, orient=True)
    subjunctive.run(world, on_direction=move_player)
