from pygame import image, mask, Rect

from model.Room import Room
from model.Toilet.ToiletSeat import ToiletSeat


class Toilet(Room):
    def __init__(self, board_pos, room_board):
        super().__init__(board_pos, room_board)
        self.init_sprite()
        self.init_seats()

    def init_sprite(self):
        self.image = image.load("../resources/rooms/toilet.png")
        self.mask = mask.from_surface(self.image)
        (x, y) = self.get_base_coordinates()
        self.rect = Rect(x, y, self.image.get_width(),
                         self.image.get_height())

    def init_seats(self):
        self.action_objects = [
            ToiletSeat(self.rect.x + 70, self.rect.y + 220, self),
            ToiletSeat(self.rect.x + 130, self.rect.y + 220, self),
            ToiletSeat(self.rect.x + 190, self.rect.y + 220, self),
            ToiletSeat(self.rect.x + 250, self.rect.y + 220, self)
        ]