import argparse
import os.path
import random

import subjunctive
from subjunctive.grid import Grid, left, right, up, down

subjunctive.resource.add_path(os.path.dirname(__file__))

class Player(subjunctive.entity.Entity):
    image = subjunctive.resource.image('images/tile-active.png')

class Block(subjunctive.entity.Entity):
    pass

class Tile(subjunctive.entity.Entity):
    image = subjunctive.resource.image('images/tile-inactive.png')

class World(subjunctive.world.World):
    tile_size = (16, 16)
    window_title = "Floorpaint"
    grid = subjunctive.grid.Grid(25, 25)
    
def generate_level(width, height):
    spaces = {(x, y): False for x in range(width)
                                    for y in range(height)}
 
    # algorithm blah blah
    x, y = 0, 0
    spaces[x, y] = True
    keepgoing = True
    num_steps = 0
    s = set()
    while keepgoing:
        choice_dir = random.choice(['down','up','right','left'])
        old_num_steps = num_steps
        s.add(choice_dir)
        if choice_dir == 'down':
            for i in range(random.randint(1,height/2)):
                if y+1<height and spaces[x, y+1]==False:
                    num_steps+=1
                    y+=1
                    spaces[x, y] = True
        elif choice_dir == 'up':
            for i in range(random.randint(1,height/2)):
                if y-1>0 and spaces[x, y-1]==False:
                    num_steps+=1
                    y-=1
                    spaces[x, y] = True
        elif choice_dir == 'right':
            for i in range(random.randint(1,width/2)):
                if x+1<width and spaces[x+1, y]==False:
                    num_steps+=1
                    x+=1
                    spaces[x, y] = True
        elif choice_dir == 'left':
            for i in range(random.randint(1,width/2)):
                if x-1>0 and spaces[x-1, y]==False:
                    num_steps+=1
                    x-=1
                    spaces[x, y] = True
        if old_num_steps != num_steps:
            s.clear()
        elif len(s) == 4:
            keepgoing =  False

        if num_steps>(width*height-20):
            keepgoing = False

    return spaces

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    grid = Grid(10, 10)
    world = World(grid)
    d = generate_level(10, 10)
    player = Player(world)
    world.place(player, grid.top_left)
    for (x, y), value in d.items():
        if not value:
            world.place(Block(world), grid.Location(x, y))
        elif x!=0 or y!=0: world.place(Tile(world), grid.Location(x, y))
    #definitions = {'o': Player, 'b': Wall, '-': None}
    #world, player = World.load('levels/01.txt', definitions, Player)

    def move_player(direction):
        player.move(direction)
    subjunctive.run(world, on_direction=move_player)
