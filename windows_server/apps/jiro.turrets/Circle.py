import pyglet, math

class Circle:
    def __init__(self, dx, dy, r, color, batch, group=None):
        color = [int(c) for c in color]
        num_points = int(math.pi * r * 2)
        verts = []
        colors = []
        for i in range(num_points):
            angle = float(i) / num_points * math.pi * 2
            x = r * math.cos(angle) + dx
            y = r * math.sin(angle) + dy
            verts += [x, y]
            colors += color
        self.vertex_list = batch.add(num_points, pyglet.gl.GL_POINTS, group, ('v2f', verts), ('c3B', colors))
        self.error = "Circle instance has no attribute 'draw'\nDraw the corresponding batch instead using 'Batch.draw'"

    def delete(self):
        self.vertex_list.delete()

    def draw(self):
        raise AttributeError(self.error)