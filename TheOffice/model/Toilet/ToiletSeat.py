from pygame import Rect

from model.Furniture import Furniture


class ToiletSeat(Furniture):
    def __init__(self, x, y, room):
        Furniture.__init__(self)
        self.rect = Rect(x, y, 47, 110)
        self.room = room
