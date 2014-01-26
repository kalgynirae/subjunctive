def move(world, entity, direction):
    entity.direction = direction
    push(world, entity, direction)
    new_location = self.locate(entity).adjacent(direction)
    if not world._entities[new_location]:
        world.remove(entity)
        world.place(entity, new_location)

def push(world, direction):
    new_location = self.locate(entity).adjacent(direction)
    if world._entities[new_location]:
        world.push(world._entities[new_location], direction)

def remove(world, entity):
    world.remove(entity)
