import os.path

import subjunctive

subjunctive.resource.add_path(os.path.dirname(__file__))

class Player(subjunctive.entity.Entity):
    image = subjunctive.resource.image('images/tile-active.png')

class Wall(subjunctive.entity.Entity):
    pass

class World(subjunctive.world.World):
    tile_size = (16, 16)
    window_title = "Floorpaint"

if __name__ == '__main__':

    definitions = {'o': Player, 'b': Wall, '-': None}
    world, player = World.load('levels/01.txt', definitions, Player)

    def move_player(direction):
        player.move(direction)
    subjunctive.run(world, on_direction=move_player)
