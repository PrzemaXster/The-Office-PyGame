from pygame import image, transform, Surface, font, Rect

from model.Interface.InterfaceElement import InterfaceElement
from service.RoomType import RoomType


class BuildingElement(InterfaceElement):
    def __init__(self, rect, img, company):
        super().__init__(rect, img)
        self._company = company
        self._room_image_list = [
            transform.scale(image.load("../resources/rooms/office.png"), (200, 200)),
            transform.scale(image.load("../resources/rooms/dining_room.png"), (200, 200)),
            transform.scale(image.load("../resources/rooms/game_room.png"), (200, 200)),
            transform.scale(image.load("../resources/rooms/conference_room.png"), (200, 200)),
            transform.scale(image.load("../resources/rooms/toilet.png"), (200, 200)),
            transform.scale(image.load("../resources/interface/elements/building/new_floor.png"), (200, 200)),
        ]
        self._room_cost_dict = {RoomType.OFFICE_ROOM: 5000, RoomType.DINING_ROOM: 4000, RoomType.GAME_ROOM: 4500,
                                RoomType.CONFERENCE_ROOM: 6000, RoomType.TOILET: 3500, RoomType.NEW_FLOOR: 20000}
        self._room_index = 0
        self.background_surface = Surface((320, 220))
        self.background_surface.set_alpha(180)
        self.background_surface.fill((0, 0, 0))
        self.cost_rect = Rect(rect.move(220, 100))
        self._sysfont = font.SysFont("Calibri", 30, True)
        self.cost_number_text = self._sysfont.render(str(self._room_cost_dict.get(self._room_index)), True, (255,255,255))
        self.capital_rect = Rect(20,550,50,30)

    def get_room_image(self):
        return self._room_image_list[self._room_index]

    def get_capital_text(self):
        return self._sysfont.render(str(self._company.money), True, (255, 255, 255), (0, 0, 0))

    def next_room(self):
        self._room_index += 1
        if self._room_index == len(self._room_image_list):
            self._room_index = 0
        self.cost_number_text = self._sysfont.render(str(self._room_cost_dict.get(self._room_index)), True, (255,255,255))

    def previous_room(self):
        self._room_index -= 1
        if self._room_index < 0:
            self._room_index = len(self._room_image_list) - 1
        self.cost_number_text = self._sysfont.render(str(self._room_cost_dict.get(self._room_index)), True, (255,255,255))

    def room_purchased(self):
        if self._company.money >= self._room_cost_dict.get(self._room_index):
            self._company.money -= self._room_cost_dict.get(self._room_index)
            return True
        else:
            return False
