from pyglet.gl import *

class PGDrawObj:
        
    def GL2C(p):
        return ( -(400 - p[0]) / 400 , -(240 - p[1]) / 240)

    class Triangle:
        def __init__(self,p1,p2,p3,color):

            p1 = PGDrawObj.GL2C(p1)
            p2 = PGDrawObj.GL2C(p2)
            p3 = PGDrawObj.GL2C(p3)

            self.vertex = [
                p1[0],p1[1],
                p2[0],p2[1],
                p3[0],p3[1]]
            self.color = [
                color[0],color[1],color[2],
                color[0],color[1],color[2],
                color[0],color[1],color[2]]

        def Render(self):
            self.vertices = pyglet.graphics.draw(3, GL_TRIANGLES, ('v2f',self.vertex),('c3B',self.color))

    class Quad:
        def __init__(self,p1,p2,p3,p4,color):

            p1 = PGDrawObj.GL2C(p1)
            p2 = PGDrawObj.GL2C(p2)
            p3 = PGDrawObj.GL2C(p3)
            p4 = PGDrawObj.GL2C(p4)

            self.indices = [0,1,2,2,3,0]
            self.vertex = [
                p1[0],p1[1],
                p2[0],p2[1],
                p3[0],p3[1],
                p4[0],p4[1]]
            self.color = [
                color[0],color[1],color[2],
                color[0],color[1],color[2],
                color[0],color[1],color[2],
                color[0],color[1],color[2]]

        def Render(self):
            self.vertices = pyglet.graphics.draw_indexed(4, GL_TRIANGLES, self.indices, ('v2f',self.vertex),('c3B',self.color))

class PDWindow(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        glClearColor(0.2,0.3,0.5,1.0)

        #self.triangle = PGDrawObj.Triangle((0,0),(200,200),(200,100),(255,0,255))
        self.tri = PGDrawObj.Triangle((0,0),(0,200),(200,300),(255,0,255))


    def on_draw(self):
        #self.clear()

        self.tri.Render()




if __name__ == "__main__":
    window = PDWindow(800,480,"PiDex")

    window.on_draw()

    pyglet.app.run()
