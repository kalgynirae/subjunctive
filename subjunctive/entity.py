import pyglet

class Entity:
    directional = False
    pushable = False

    def __init__(self, world, *, direction='right', name=None):
        # Create the sprite first to avoid problems with overridden setters
        # that try to access the sprite
        self.sprite = pyglet.sprite.Sprite(self.image, batch=world.batch)
        self.direction = direction
        self.name = self.__class__.__name__ if name is None else name
        self.world = world

    def __str__(self):
        return self.name

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction
        if self.directional:
            _rotate(self.sprite, direction)

    @property
    def image(self):
        return pyglet.resource.image('images/default.png')

    @image.setter
    def image(self, image):
        self.sprite.image = image

    def respond_to_push(self, direction, pusher, world):
        """Return what should happen when the entity is pushed

        Entities can override this method to get special behavior.

        Possible return values: "stay", "move", "vanish", "consume", "mad"
        """
        return "move" if self.pushable else "stay"

def _rotate(sprite, direction):
    rotation = {'left': 180, 'down': 90, 'up': 270, 'right': 0}
    sprite.rotation = rotation[direction]
