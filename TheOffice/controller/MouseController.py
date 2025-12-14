import pygame

from controller.BuildController import BuildingController
from model.CursorObject import CursorObject
from service.EmployeeServices.EmployeeManagement.EmployeeManagementService import EmployeeManagementService
from service.Interface.InterfaceService import InterfaceService
from service.RoomType import RoomType


class MouseController:
    def __init__(self, screen, employee_list, building_controller: BuildingController, ground, interface_service: InterfaceService,employee_service : EmployeeManagementService):
        self.LEFT_CLICK = 1
        self.MIDDLE_CLICK = 2
        self.RIGHT_CLICK = 3

        self.screen = screen
        self.emp_list = employee_list
        self.building_controller = building_controller
        self.room_board = building_controller.building_service.room_board
        self.corridors = building_controller.building_service.corridors
        self.employee_service = employee_service
        self.interface_service = interface_service
        self.ground = ground
        self.speed = 15
        self.threshold = 70
        self.cursor = CursorObject()
        self.board_pos = (-1, -1)

    # currently dropped in favour of keyboard view scrolling
    def scroll_view(self):
        if pygame.mouse.get_pos()[0] >= self.screen.get_width() - self.threshold:
            self.move_objects(-self.speed, 0)
        elif pygame.mouse.get_pos()[0] <= self.threshold:
            self.move_objects(self.speed, 0)
        elif pygame.mouse.get_pos()[1] <= self.threshold:
            self.move_objects(0, self.speed)
        elif pygame.mouse.get_pos()[1] >= self.screen.get_height() - self.threshold:
            self.move_objects(0, -self.speed)

    def move_cursor(self):
        self.cursor.relocate(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        # if cursor collides with any slot then stick the room to the slot
        if self.cursor.drags_room():
            for floor in range(0, len(self.room_board)):
                for room in self.room_board[floor]:
                    if self.cursor.collides_with(room.rect):
                        self.cursor.rect.x = room.rect.x + 150
                        self.cursor.rect.y = room.rect.y + 150
                        self.board_pos = (self.room_board[floor].index(room), floor)

    def place_building(self):
        self.building_controller.build_room(self.board_pos, self.cursor.object_id)
        self.cursor.clear_cursor()

    def execute_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT_CLICK:
            if self.cursor.drags_room():
                self.place_building()
            for element in self.interface_service.element_list:
                if self.cursor.collides_with(element.rect):
                    element.click()
            if self.interface_service.purchased_room == RoomType.NEW_FLOOR:
                self.building_controller.build_floor()
                self.interface_service.purchased_room = RoomType.NONE
                return
            if self.interface_service.purchased_room != RoomType.NONE:
                self.cursor.set_cursor_object(self.interface_service.purchased_room)
                self.interface_service.purchased_room = RoomType.NONE
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT_CLICK:
            for emp in self.emp_list:
                if self.cursor.collides_with(emp.rect):
                    self.interface_service.emp_stat_full_element.click_actor(emp)
                    self.interface_service.relationship_stat_element.update_emp_relationships(emp,10, 0)
        self.hover_event()

    def hover_event(self):
        for element in self.interface_service.element_list:
            element.hover_effect = element.NO_EFFECT
            if self.cursor.collides_with(element.rect):
                element.hover(element)
        self.interface_service.emp_stat_element.hover_effect = self.interface_service.emp_stat_element.NO_EFFECT
        if self.interface_service.view_type == self.interface_service.NO_TYPE:
            for emp in self.emp_list:
                if emp.is_collide_with_mouse():
                    self.interface_service.emp_stat_element.hover_actor(self.interface_service.emp_stat_element, emp)

    def grab_employee_event(self, event):
        for i in range(0, len(self.employee_service.employee_list)):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT_CLICK:
                self.employee_service.pick_up_employee(i)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == self.LEFT_CLICK:
                self.employee_service.put_down_employee(i)


