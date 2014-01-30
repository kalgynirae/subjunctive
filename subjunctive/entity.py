from . import actions

class Entity:
    directional = False
    pushable = False

    def __init__(self, world, *, direction='right', name=None):
        self.direction = direction
        self.name = self.__class__.__name__ if name is None else name
        self.world = world

    def __str__(self):
        return self.name

    @property
    def image(self):
        return subjunctive.load('images/default.png')

    def move(self, direction):
        self.direction = direction
        new_location = self.world.locate(self).adjacent(direction)
        blocking_entity = self.world._entities.get(new_location)
        if blocking_entity:
            blocking_entity.push(direction, self)
        if not self.world._entities[new_location]:
            try:
                self.world.remove(self)
            except ValueError:
                # This means someone else removed us, so give up
                pass
            else:
                self.world.place(self, new_location)

    def push(self, direction, pusher=None):
        """Return what should happen when the entity is pushed

        Entities can override this method to get special behavior.

        Possible return values: "stay", "move", "vanish", "consume", "mad"
        """
        if self.pushable:
            self.move(direction)
