import random

from pygame import time, mouse

from model.Company import Company
from model.Employee.Employee import Employee
from model.Ground import Ground
from service.EmployeeServices.EmployeeManagement.AnimationService import AnimationService
from service.EmployeeServices.EmployeeManagement.CollisionService import CollisionService
from service.EmployeeServices.EmployeeManagement.DestinationSearchService import DestinationSearchService
from service.EmployeeServices.Needs.NeedsService import NeedsService
from service.EmployeeServices.Needs.TaskService import TaskService
from service.EmployeeThreads.EmployeeNeedThread import EmployeeNeedThread
from service.EmployeeThreads.EmployeeTaskThread import EmployeeTaskThread


class EmployeeManagementService:
    def __init__(self, room_board, ground: Ground, animation_service: AnimationService):
        self.employee_list = []
        self.init_extras()
        self.room_board = room_board
        self.ground = ground
        self.init_threads()
        self.animation_service = animation_service
        self.init_services()

    def check_employees_needs_and_move(self):
        for emp in self.employee_list:
            self.check_emp_needs_and_move(emp)
            if not emp.is_sitting_down():
                self.gravity_employee(emp)

    def check_emp_needs_and_move(self, emp: Employee):
        if emp.destination is None:
            # the moment when employee starts feeling the need
            if emp.is_empty_bladder():
                if emp.is_not_fulfilling_needs() or (emp.is_relaxed() and emp.is_satiated()):
                    self.task_service_t.pop_emp(emp, "motivation")
                    self.task_service_t.pop_emp(emp, "work")
                    self.task_service_t.pop_emp(emp, "stress")
                    self.task_service_t.pop_emp(emp, "hunger")
                    self.dest_service.search_for_room(emp, "Toilet")
            elif emp.is_hungry():
                if emp.is_not_fulfilling_needs() or (emp.is_relaxed() and emp.is_full_bladder()):
                    self.task_service_t.pop_emp(emp, "work")
                    self.task_service_t.pop_emp(emp, "stress")
                    self.task_service_t.pop_emp(emp, "motivation")
                    self.task_service_t.pop_emp(emp, "bladder")
                    self.dest_service.search_for_room(emp, "DiningRoom")
            elif emp.is_stressed():
                if emp.is_not_fulfilling_needs() or (emp.is_satiated() and emp.is_full_bladder()):
                    self.task_service_t.pop_emp(emp, "motivation")
                    self.task_service_t.pop_emp(emp, "work")
                    self.task_service_t.pop_emp(emp, "hunger")
                    self.task_service_t.pop_emp(emp, "bladder")
                    self.dest_service.search_for_room(emp, "GameRoom")
            # when employee just stands on ground
            elif emp.is_idle():
                self.task_service_t.pop_emp(emp, "stress")
                self.task_service_t.pop_emp(emp, "motivation")
                self.task_service_t.pop_emp(emp, "hunger")
                self.task_service_t.pop_emp(emp, "bladder")
                self.dest_service.search_for_room(emp, "OfficeRoom")
        # movement logic towards destination
        if emp.destination is not None and not emp.is_collide_with_mouse() and self.ground.is_touching_adjusted(emp) and not emp.block_move:
            if emp.is_sitting_down():
                emp.remove_from_desk()
            self.move_emp_towards_destination(emp)
            if self.dest_service.emp_arrived_at_destination(emp):
                destination = self.dest_service.search_for_spot(emp)
                # employee is at the spot and sitting down
                if destination is None:
                    self.collision_service.update_action_object_status(emp.destination)
                    self.collision_service.adjust_emp_to_action_object(emp, emp.destination, emp.destination.room,
                                                                       emp.destination.room.action_objects.index(emp.destination))
                    emp.set_desk(emp.destination)
                self.dest_service.change_destination(emp, destination)

    def create_employee(self, x, y, name: str, company: Company):
        emp = Employee(x, y, name, company)
        self.employee_list.append(emp)
        self.needs_service_t.insert_emp(emp)

    def create_specific_employee(self, x, y, name: str, abilities: tuple, images_path:str, salary: int, company: Company):
        emp = Employee(x, y, name, company, abilities, images_path, salary)
        self.employee_list.append(emp)
        self.needs_service_t.insert_emp(emp)

    def init_extras(self):
        self.dragged_emp_i = -1
        self.dragged_emp_x = -1
        self.falling_emp_y = -1

        self.dragged_emp_x_queue = []
        self.cursor = 0
        self.FIRST = 3
        self.SECOND = 2
        self.THIRD = 1
        self.LAST = 0

        self.initial_ticks = [time.get_ticks()]

    def init_threads(self):
        self.emp_task_thread = EmployeeTaskThread()
        self.emp_need_thread = EmployeeNeedThread()
        self.task_service_t = TaskService(self.emp_task_thread)
        self.needs_service_t = NeedsService(self.emp_need_thread)
        self.emp_task_thread.start()
        self.emp_need_thread.start()

    def init_services(self):
        self.dest_service = DestinationSearchService(self.room_board, self.task_service_t)
        self.collision_service = CollisionService(self.room_board, self.task_service_t)

    def drag_emp_if_selected(self):
        if self.dragged_emp_i != -1:
            if self.employee_list[self.dragged_emp_i].rect.centerx > self.dragged_emp_x + 5:
                self.employee_list[self.dragged_emp_i].change_dragging_sprite("R")
                self.dragged_emp_x = self.employee_list[self.dragged_emp_i].rect.centerx
            elif self.employee_list[self.dragged_emp_i].rect.centerx < self.dragged_emp_x - 5:
                self.employee_list[self.dragged_emp_i].change_dragging_sprite("L")
                self.dragged_emp_x = self.employee_list[self.dragged_emp_i].rect.centerx
            else:
                self.employee_list[self.dragged_emp_i].change_dragging_sprite("C")
                self.dragged_emp_x = self.employee_list[self.dragged_emp_i].rect.centerx

            self.dragged_emp_x_queue.append(self.employee_list[self.dragged_emp_i].rect.centerx)
            if len(self.dragged_emp_x_queue) > 4:
                self.dragged_emp_x_queue.pop(self.LAST)
                if self.employee_is_shaken():
                    if self.delay_by_frames(100, 1):
                        self.employee_list[self.dragged_emp_i].change_shaking_sprite()
                    if self.delay_by_frames(1500, 0):
                        self.employee_list[self.dragged_emp_i].needs.decrease_stress()
                        if not self.employee_list[self.dragged_emp_i].is_stressed():
                            self.employee_list[self.dragged_emp_i].needs.meet()

            self.employee_list[self.dragged_emp_i].rect.centerx = mouse.get_pos()[0]
            self.employee_list[self.dragged_emp_i].rect.centery = mouse.get_pos()[1]

    def employee_is_shaken(self):
        return self.dragged_emp_x_queue[self.SECOND] + 10 < self.dragged_emp_x_queue[self.LAST] and self.dragged_emp_x_queue[self.FIRST] > \
               self.dragged_emp_x_queue[self.THIRD] + 10

    def pick_up_employee(self, index):
        if self.employee_list[index].rect.collidepoint(mouse.get_pos()):
            self.dragged_emp_i = index
            self.collision_service.handle_emp_desk_detach_event(self.employee_list[self.dragged_emp_i])

    def put_down_employee(self, index):
        if self.employee_list[index].rect.collidepoint(mouse.get_pos()):
            self.employee_list[self.dragged_emp_i].destination = None
            self.collision_service.handle_emp_desk_collide(self.employee_list[self.dragged_emp_i])
        self.dragged_emp_i = -1

    def move_emp_towards_destination(self, emp :Employee):
        x=0
        emp.direction = ''
        if emp.destination.rect.x > emp.rect.x + 4:
            x = emp._abilities.speed
            emp.direction = 'R'
        elif emp.destination.rect.x < emp.rect.x - 4:
            x = -emp._abilities.speed
            emp.direction = 'L'
        emp.rect = emp.rect.move(x, 0)
        emp.vision_field.x = emp.rect.x
        self.animation_service.animate_employee(emp)

    def gravity_employee(self, emp: Employee):
        if not self.ground.is_touching(emp):
            emp.rect = emp.rect.move(0, 12)
            if emp.rect.centery > self.falling_emp_y + 20 and not emp.is_collide_with_mouse():
                emp.change_falling_sprite()
                self.falling_emp_y = emp.rect.centery
            else:
                self.falling_emp_y = -1

    def delay_by_frames(self, frames, initial_tick_id):
        if initial_tick_id == len(self.initial_ticks):
            self.initial_ticks.append(time.get_ticks())

        delay = time.get_ticks() - self.initial_ticks[initial_tick_id]
        if delay > frames:
            self.initial_ticks[initial_tick_id] = time.get_ticks()
        return delay >= frames

    def pay_employees(self):
        if not self.employee_list[0].got_paid:
            for employee in self.employee_list:
                employee.get_paid()

    def reset_payment_system(self):
        if self.employee_list[0].got_paid:
            for employee in self.employee_list:
                employee.got_paid = False


