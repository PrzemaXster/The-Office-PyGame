import random
import random

import pygame

from model.Company import Company
from service.EmployeeServices.EmployeeManagement.EmployeeManagementService import EmployeeManagementService
from service.Interface.InterfaceService import InterfaceService


class EmployeeController:
    def __init__(self, room_board, ground, company: Company, interface_service: InterfaceService):
        self.employee_names = [
            "George",
            "Michael",
            "Bob",
            "Kayle",
            "John",
            "Mark",
            "Dane",
            "Tom",
            "Bill",
            "Howard",
            "Harry"
        ]
        self.employee_service = EmployeeManagementService(room_board, ground)
        self.interface_service = interface_service
        self.company = company

    def manage_salaries(self):
        if self.interface_service.calendar_element.is_payday():
            self.employee_service.pay_employees()
        elif self.interface_service.calendar_element.is_day_after_payday:
            self.employee_service.reset_payment_system()

    def create_employee(self, x, y):
        self.employee_service.create_employee(x, y, self.employee_names[random.randint(0, len(self.employee_names) - 1)], self.company)

    def grab_employee_event(self, event):
        for i in range(0, len(self.employee_service.employee_list)):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.employee_service.pick_up_employee(i)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.employee_service.put_down_employee(i)

    def drag_employee(self):
        self.employee_service.drag_emp_if_selected()

    def move_employees(self):
        self.employee_service.check_employees_needs_and_move()

    def hire_employee(self, pos):
        if self.interface_service.hired_emp is not None:
            self.employee_service.create_specific_employee(pos[0], pos[1], self.interface_service.hired_emp.get("name")
                                                           , self.interface_service.hired_emp.get("abilities"),
                                                           self.interface_service.hired_emp.get("images_path"),
                                                           self.interface_service.hired_emp.get("salary"), self.company)
            self.interface_service.hired_emp = None
