import pyglet
import res, batch
from Vector import *
from ScoreboardItem import *

class ScoreboardBar(pyglet.sprite.Sprite):

    def __init__(self, window_width, window_height):
        pyglet.sprite.Sprite.__init__(self, res.IMG_COLOR_BLACK, batch=batch.overlay1)
        self.scale_x = window_width
        self.scale_y = 44
        self.x = 0
        self.y = window_height - self.scale_y
        self.item_padding = 15
        self.items = {}

    def addPlayer(self, addr, name):
        self.items[addr] = ScoreboardItem(name, self.y + 7)
        self.repositionItems()

    def removePlayer(self, addr):
        item = self.items.get(addr, None)
        if item != None:
            item.nameLabel.delete()
            item.scoreLabel.delete()
            item.delete()
            self.items.pop(addr, None)
        self.repositionItems()

    def repositionItems(self):
        item_count = len(self.items)
        if item_count > 0:
            x = self.item_padding
            #segment = (self.scale_x - self.item_padding * 3) / item_count
            #if segment > 320:
            #    segment = 320
            for key in self.items:
                item = self.items[key]
                width = item.reposition(x)
                x += width + self.item_padding

    def playerScoreAdd(self, addr, amount):
        item = self.items.get(addr, None)
        if item == None: return
        item.score += amount
        item.scoreLabel.text = str(item.score)