import random
from Astroid import *

class EnemySpawner:
    def __init__(self):
        self.spawntimer = 3

    def update(self, dt, bounds):
        self.spawntimer -= dt
        if self.spawntimer < 0:
            self.spawntimer += 3
            radius = random.randint(30, 90)
            Astroid(Vector(random.randint(int(bounds[0].x / 1.5), int(bounds[1].x / 1.5)), bounds[1].y), radius, random.randint(3000, 4000) / radius, random.randint(230, 310), res.IMG_ASTROID1)