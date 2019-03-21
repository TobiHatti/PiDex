import pyglet
from pyglet.window import FPSDisplay


class GameWindow(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_location(400,100)
        self.frame_rate = 1/60.0
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 50


        sprite = pyglet.image.load("Charizard.gif")
        sprite_seq = pyglet.image.ImageGrid(sprite,1,5,item_width = 300, item_height = 300)
        sprite_texture = pyglet.image.TextureGrid(sprite_seq)
        sprite_animated = pyglet.image.Animation.from_image_sequence(sprite_texture[0:], 0.1, loop=True)

        self.fsprite = pyglet.sprite.Sprite(sprite_animated,400,400)

    def on_draw(self):
        self.clear()
        self.fsprite.draw()
        self.fps_display.draw()

    def update(self, dt):
        pass


    if __name__ == "__main__":
        pyglet.clock.schedule_interval(update, 1.0/60)
        pyglet.app.run()