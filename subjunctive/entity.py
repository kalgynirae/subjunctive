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

    def respond_to_push(self, direction, pusher, world):
        """Return what should happen when the entity is pushed

        Entities can override this method to get special behavior.

        Possible return values: "stay", "move", "vanish", "consume", "mad"
        """
        return "move" if self.pushable else "stay"
