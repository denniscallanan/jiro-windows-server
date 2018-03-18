import random, noise
from Platform import *

class ObstacleFactory:
    
    seed1 = random.randint(-50000, 50000)
    seed2 = random.randint(-50000, 50000)

    @staticmethod
    def createObstaclePlatforms(x):
        '''rows = random.randint(2, 5)
        rowspacing = 720 / rows
        rowoffset = rowspacing / 3 - 360
        maxwidth = random.randint(300, 600)
        
        for r in range(rows):
            cols = random.randint(1, 2)
            colspacing = random.randint(25, 50)
            colwidth = (maxwidth - 2 * colspacing) / cols
            y = r * rowspacing + rowoffset
            if r == 0 or random.randint(0, 1) == 0:
                for c in range(cols):
                    Platform.instances.append(Platform(x + (colspacing * (c + 1)) + ((colwidth - colspacing) * c), y, colwidth, 50))

        '''

        '''rows = random.randint(2, 4)
        rowspacing = 720 / rows
        rowoffset = rowspacing / 3 - 360
        maxwidth = random.randint(500, 700)

        count = 0
        for r in range(rows):
            if random.randint(0, 2) < 2:
                y = r * rowspacing + rowoffset
                colwidth = random.randint(maxwidth / 2, maxwidth)
                Platform.instances.append(Platform(x + maxwidth / 2, y, colwidth, 25))
                count += 1

        if count == 0:
            y = random.randint(-360, 220)
            Platform.instances.append(Platform(x + maxwidth / 2, y, maxwidth, 25))

        return maxwidth + random.randint(20, 50)'''

        #width = random.randint(350, 500)
        width = noise.pnoise1((ObstacleFactory.seed1 + x + 0.5) / 1000) * 150 + 300
        spacing = random.randint(140, 240)
        y = noise.pnoise1((ObstacleFactory.seed2 + x + 0.5) / 1) * 330
        Platform.instances.append(Platform(x + width / 2, y, width, 25))
        
        return width + spacing
