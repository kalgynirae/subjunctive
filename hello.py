import pyglet

window = pyglet.window.Window()
label = pyglet.text.Label("Hello, world!", font_name='Linux Libertine',
                            font_size=36, x=window.width//2,
                            y=window.height//2, anchor_x='center',
                            anchor_y='center')
image = pyglet.image.load('/home/lumpy/pictures/colin_tube.jpg')

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)
    label.draw()

@window.event
def on_key_press(symbol, modifiers):
    print("Key {} was pressed".format(symbol))

@ window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        print("You clicked!")

window.push_handlers(pyglet.window.event.WindowEventLogger())

pyglet.app.run()
