from service.BuildingService import BuildingService
from service.RoomType import RoomType


class BuildingController:
    def __init__(self):
        self.building_service = BuildingService()

    # board_pos = (room, floor)
    def build_room(self, board_pos, room_type: int):
        if room_type == RoomType.OFFICE_ROOM:
            self.building_service.build_office(board_pos)
        elif room_type == RoomType.DINING_ROOM:
            self.building_service.build_dining_room(board_pos)
        elif room_type == RoomType.GAME_ROOM:
            self.building_service.build_game_room(board_pos)
        elif room_type == RoomType.CONFERENCE_ROOM:
            self.building_service.build_conference_room(board_pos)
        elif room_type == RoomType.TOILET:
            self.building_service.build_toilet(board_pos)
        elif room_type == RoomType.CORRIDOR:
            self.building_service.build_corridor(board_pos)
        elif room_type == RoomType.ELEVATOR:
            self.building_service.build_elevator_room(board_pos)

    def build_floor(self):
        self.building_service.build_floor()

    def get_room_board(self):
        return self.building_service.room_board
