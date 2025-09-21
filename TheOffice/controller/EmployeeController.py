import random
import random

import pygame

from model.Company import Company
from service.EmployeeServices.EmployeeManagement.AnimationService import AnimationService
from service.EmployeeServices.EmployeeManagement.EmployeeManagementService import EmployeeManagementService
from service.Interface.InterfaceService import InterfaceService


class EmployeeController:
    def __init__(self, room_board, ground, company: Company, interface_service: InterfaceService,
                 animation_service: AnimationService):
        self.animation_service = animation_service
        self.interface_service = interface_service
        self.company = company
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
        self.employee_service = EmployeeManagementService(room_board, ground, self.animation_service)

    def manage_salaries(self):
        if self.interface_service.calendar_element.is_payday():
            self.employee_service.pay_employees()
        elif self.interface_service.calendar_element.is_day_after_payday:
            self.employee_service.reset_payment_system()

    def create_employee(self, x, y):
        self.employee_service.create_employee(x, y,
                                              self.employee_names[random.randint(0, len(self.employee_names) - 1)],
                                              self.company)
        emp = self.employee_service.employee_list[0]
        emp.stats.hire_date = self.interface_service.calendar_element.current_date


    def drag_employee(self):
        self.employee_service.drag_emp_if_selected()

    def move_employees(self):
        self.employee_service.check_employees_needs_and_move()

    def hire_employee(self, pos):
        if self.interface_service.hired_emp is not None:
            self.employee_service.create_specific_employee(pos[0], pos[1], self.interface_service.hired_emp.get("name")
                                                           , self.interface_service.hired_emp.get("abilities"),
                                                           self.interface_service.hired_emp.get("images_path"),
                                                           self.interface_service.hired_emp.get("salary"),
                                                           self.interface_service.calendar_element.current_date,
                                                           self.company)
            self.interface_service.hired_emp = None
