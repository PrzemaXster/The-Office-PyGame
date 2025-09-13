import pygame
from pygame import K_a

from controller.BuildController import BuildingController
from controller.EmployeeController import EmployeeController
from model.CursorObject import CursorObject
from model.Ground import Ground
from service.RoomType import RoomType


class KeyboardController:
    def __init__(self, employee_controller: EmployeeController, building_controller: BuildingController, cursor: CursorObject, company,
                 ground: Ground):
        self.employee_controller = employee_controller
        self.building_controller = building_controller
        self.ground = ground
        self.cursor = cursor
        self.company = company

        self.screen = ground.screen
        self.room_board = building_controller.building_service.room_board
        self.corridors = building_controller.building_service.corridors
        self.last_room = self.room_board[0][
            len(self.room_board[0]) - 1]
        self.left_boundary = pygame.Rect(0, 0, 0, 0)
        self.right_boundary = pygame.Rect(self.last_room.rect.right, 0, 0, 0)
        self.emp_list = employee_controller.employee_service.employee_list
        self._speed = 15

    def execute_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key is pygame.K_q:
                self.employee_controller.create_employee(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif e.key is pygame.K_1:
                self.cursor.set_cursor_object(RoomType.OFFICE_ROOM)
            elif e.key is pygame.K_2:
                self.cursor.set_cursor_object(RoomType.DINING_ROOM)
            elif e.key is pygame.K_3:
                self.cursor.set_cursor_object(RoomType.GAME_ROOM)
            elif e.key is pygame.K_f:
                self.building_controller.build_floor()

    def scroll_view(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] and self.left_boundary.x < 0:
            self.move_objects(self._speed, 0)
        if keys[pygame.K_d] and self.right_boundary.x > self.screen.get_width():
            self.move_objects(-self._speed, 0)
        if keys[pygame.K_w] and self.room_board[len(self.room_board)-1][0].rect.y < 0:
            self.move_objects(0, self._speed)
        if keys[pygame.K_s] and self.ground.y > self.screen.get_height() * 6 / 7 + 10:
            self.move_objects(0, -self._speed)

    def move_objects(self, x, y):
        for emp in self.emp_list:
            emp.rect = emp.rect.move(x, y)
            emp.vision_field = emp.vision_field.move(x, y)
        # for each action object in each room in each floor move them according to camera position
        for floor in self.room_board:
            for room in floor:
                room.rect = room.rect.move(x, y)
                for a_obj in room.action_objects:
                    a_obj.rect = a_obj.rect.move(x, y)
        for corridor in self.corridors:
            corridor.rect = corridor.rect.move(x, y)
        self.ground.move(y)
        self.left_boundary = self.left_boundary.move(x,0)
        self.right_boundary = self.right_boundary.move(x,0)
