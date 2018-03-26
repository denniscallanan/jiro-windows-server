import random
from Astroid import *

class EnemySpawner:
    def __init__(self):
        self.spawntimer = 5
        self.nextspawntimer = 5

    def update(self, dt, bounds):
        self.spawntimer -= dt
        if self.spawntimer < 0:
            self.spawntimer += self.nextspawntimer
            self.nextspawntimer /= 1.005
            position = Vector(random.randint(int(bounds[0].x / 1.5), int(bounds[1].x / 1.5)), bounds[1].y)
            if random.randint(0, 8) == 0:
                radius = random.randint(30, 60)
                Astroid(position, radius, random.randint(9000, 12000) / radius, random.randint(260, 280), res.IMG_ASTROID2)
            else:
                radius = random.randint(15, 90)
                Astroid(position, radius, random.randint(3000, 4000) / radius, random.randint(230, 310), res.IMG_ASTROID1)