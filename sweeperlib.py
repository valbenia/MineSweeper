import pyglet
from pyglet.gl import glEnable, GL_TEXTURE_2D

MOUSE_LEFT = pyglet.window.mouse.LEFT
MOUSE_MIDDLE = pyglet.window.mouse.MIDDLE
MOUSE_RIGHT = pyglet.window.mouse.RIGHT

MOD_SHIFT = pyglet.window.key.MOD_SHIFT
MOD_CTRL = pyglet.window.key.MOD_CTRL
MOD_ALT = pyglet.window.key.MOD_ALT

graphics = {
    "window": None,
    "background": None,
    "bg_color": None,
    "batch": None,
    "sprites": [],
    "images": {}
}

handlers = {
    "timeouts": [],
}

glEnable(GL_TEXTURE_2D)

def load_sprites(path):
    
    pyglet.resource.path = [path]
    images = {}
    images["0"] = pyglet.resource.image("tile_empty.png")
    for i in range(1, 9):
        images[str(i)] = pyglet.resource.image("tile_{}.png".format(i))
    images["x"] = pyglet.resource.image("tile_mine.png")
    images[" "] = pyglet.resource.image("tile_back.png")
    images["f"] = pyglet.resource.image("tile_flag.png")
    graphics["images"] = images

def load_duck(path):
   
    pyglet.resource.path = [path]
    duck = pyglet.resource.image("duck.png")
    sling = pyglet.resource.image("sling.png")
    graphics["images"]["duck"] = duck
    graphics["images"]["sling"] = sling

def create_window(width=800, height=600, bg_color=(240, 240, 240, 255)):
   
    if graphics["window"] is None:
        graphics["window"] = pyglet.window.Window(width, height, resizable=True)
        graphics["bg_color"] = bg_color
        graphics["background"] = pyglet.sprite.Sprite(
            pyglet.image.SolidColorImagePattern(bg_color).create_image(width, height)
        )
        graphics["window"].set_visible(False)
        graphics["window"].on_close = close
    else:
        resize_window(width, height)

def resize_window(width, height):
    
    graphics["window"].set_size(width, height)
    graphics["background"] = pyglet.sprite.Sprite(
        pyglet.image.SolidColorImagePattern(graphics["bg_color"]).create_image(width, height)
    )


def set_mouse_handler(handler):

    if graphics["window"]:
        graphics["window"].on_mouse_press = handler
    else:
        print("Window hasn't been created!")

def set_drag_handler(handler):
    if graphics["window"]:
        graphics["window"].on_mouse_drag = handler
    else:
        print("Window hasn't been created!")
    
def set_release_handler(handler):
    
    if graphics["window"]:
        graphics["window"].on_mouse_release = handler
    else:
        print("Window hasn't been created!")
    
    
def set_keyboard_handler(handler):

    if graphics["window"]:
        graphics["window"].on_key_press = handler
    else:
        print("Window hasn't been created!")

def set_draw_handler(handler):


    if graphics["window"]:
        graphics["window"].on_draw = handler
    else:
        print("Window hasn't been created!")

def set_interval_handler(handler, interval=1/60):

    pyglet.clock.schedule_interval(handler, interval)
    handlers["timeouts"].append(handler)

def start():

    graphics["window"].set_visible(True)
    pyglet.app.run()

def close():

    for handler in handlers["timeouts"]:
        pyglet.clock.unschedule(handler)
    pyglet.app.exit()
    graphics["window"].set_visible(False)

def clear_window():

    graphics["window"].clear()


def draw_background():

    graphics["background"].draw()

def draw_text(text, x, y, color=(0, 0, 0, 255), font="serif", size=32):
   
    text_box = pyglet.text.Label(text,
        font_name=font,
        font_size=size,
        color=color,
        x=x, y=y,
        anchor_x="left", anchor_y="bottom"
    )
    text_box.draw()

def begin_sprite_draw():


    graphics["batch"] = pyglet.graphics.Batch()

def prepare_sprite(key, x, y):
    
    graphics["sprites"].append(pyglet.sprite.Sprite(
        graphics["images"][str(key).lower()],
        x,
        y,
        batch=graphics["batch"]
    ))

def draw_sprites():

    graphics["batch"].draw()
    graphics["sprites"].clear()

if __name__ == "__main__":
  
    load_sprites("sprites")
    create_window()

    def draw():
        clear_window()
        draw_background()
        begin_sprite_draw()
        for i, key in enumerate(graphics["images"].keys()):
            prepare_sprite(key, i * 40, 10)

        draw_sprites()

    def close_window(x, y, button, mods):
        close()

    set_draw_handler(draw)
    set_mouse_handler(close_window)

    start()
