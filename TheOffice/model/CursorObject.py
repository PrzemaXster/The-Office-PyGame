from pygame import Rect, image


class CursorObject:
    def __init__(self):
        self.image = None
        self.rect = Rect(0, 0, 1, 1)
        self.init_images()
        self.object_id = -1

    def clear_cursor(self):
        self.image = None
        self.object_id = -1

    def relocate(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def collides_with(self, rect):
        return self.rect.colliderect(rect)

    def set_cursor_object(self, cursor_object_id: int):
        self.image = self.images_list[cursor_object_id]
        self.object_id = cursor_object_id

    def drags_room(self):
        return self.image is not None


    def init_images(self):
        self.images_list = [
            image.load("../resources/rooms/office.png"),
            image.load("../resources/rooms/dining_room.png"),
            image.load("../resources/rooms/game_room.png"),
            image.load("../resources/rooms/conference_room.png"),
            image.load("../resources/rooms/toilet.png")
        ]