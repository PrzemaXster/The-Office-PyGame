from model.ConferenceRoom.ConferenceRoom import ConferenceRoom
from model.Corridor.Corridor import Corridor
from model.DiningRoom.DiningRoom import DiningRoom
from model.ElevatorRoom.ElevatorRoom import ElevatorRoom
from model.GameRoom.GameRoom import GameRoom
from model.OfficeRoom.OfficeRoom import OfficeRoom
from model.Toilet.Toilet import Toilet


class BuildingService:
    def __init__(self):
        self.room_board = [[]]
        self.corridors = []

    def build_floor(self):
        self.room_board.append([])
        floor = len(self.room_board) - 1
        self.build_corridor((0, floor))
        self.build_corridor((1, floor))
        self.build_corridor((2, floor))
        self.build_elevator_room((3, floor))
        self.build_corridor((4, floor))
        self.build_corridor((5, floor))
        self.build_corridor((6, floor))

    # board_pos(x,y)
    # board_pos[0] - row of rooms (x)
    # board_pos[1] - column of floors  (y)
    def build_office(self, board_pos):
        self.validate_board_pos(board_pos)
        if board_pos[0] == len(self.room_board[board_pos[1]]):
            office = OfficeRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]].append(office)
        else:
            office = OfficeRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]][board_pos[0]] = office

    def build_dining_room(self, board_pos):
        self.validate_board_pos(board_pos)
        if board_pos[0] == len(self.room_board[board_pos[1]]):
            dining_room = DiningRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]].append(dining_room)
        else:
            dining_room = DiningRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]][board_pos[0]] = dining_room


    def build_game_room(self, board_pos):
        self.validate_board_pos(board_pos)
        if board_pos[0] == len(self.room_board[board_pos[1]]):
            game_room = GameRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]].append(game_room)
        else:
            game_room = GameRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]][board_pos[0]] = game_room

    def build_conference_room(self, board_pos):
        self.validate_board_pos(board_pos)
        if board_pos[0] == len(self.room_board[board_pos[1]]):
            conference_room = ConferenceRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]].append(conference_room)
        else:
            conference_room = ConferenceRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]][board_pos[0]] = conference_room

    def build_toilet(self, board_pos):
        self.validate_board_pos(board_pos)
        if board_pos[0] == len(self.room_board[board_pos[1]]):
            toilet = Toilet(board_pos, self.room_board)
            self.room_board[board_pos[1]].append(toilet)
        else:
            toilet = Toilet(board_pos, self.room_board)
            self.room_board[board_pos[1]][board_pos[0]] = toilet
    def build_corridor(self, board_pos):
        self.validate_board_pos(board_pos)
        if board_pos[0] == len(self.room_board[board_pos[1]]):
            corridor = Corridor(board_pos, self.room_board)
            self.room_board[board_pos[1]].append(corridor)
        else:
            corridor = Corridor(board_pos, self.room_board)
            self.room_board[board_pos[1]][board_pos[0]] = corridor

    def validate_board_pos(self, board_pos):
        if board_pos[1] >= len(self.room_board):
            raise Exception(board_pos[1], "exceeded the actual number of floors to build on:", len(self.room_board))
        elif board_pos[0] > len(self.room_board[board_pos[1]]):
            raise Exception(board_pos[0], "exceeded the actual number of rooms to build:", len(self.room_board[board_pos[1]]))

    def build_elevator_room(self, board_pos):
        self.validate_board_pos(board_pos)
        if board_pos[0] == len(self.room_board[board_pos[1]]):
            elevator = ElevatorRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]].append(elevator)
        else:
            elevator = ElevatorRoom(board_pos, self.room_board)
            self.room_board[board_pos[1]][board_pos[0]] = elevator
