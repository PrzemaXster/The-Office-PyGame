import pygame

from controller.BuildController import BuildingController
from controller.EmployeeController import EmployeeController
from controller.KeyboardController import KeyboardController
from controller.MouseController import MouseController
from model.Company import Company
from model.Ground import Ground
from model.Interface.StaticElement import StaticElement
from service.Interface.InterfaceService import InterfaceService
from service.RoomType import RoomType


class Game:
    def __init__(self):
        pygame.init()
        self.init_screen()
        self.init_texts()
        self.init_objects()
        self.main_loop()

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.employee_controller.employee_service.emp_need_thread.destroy()
                    self.employee_controller.employee_service.emp_task_thread.destroy()
                    pygame.sys.exit(0)
                self.keyboard_controller.execute_event(event)
                self.mouse_controller.execute_event(event)
                self.employee_controller.grab_employee_event(event)
            self.screen.fill((155, 232, 255))
            self.employee_controller.drag_employee()
            self.employee_controller.manage_salaries()
            self.update_text()
            # self.mouse_controller.scroll_view()
            self.keyboard_controller.scroll_view()
            self.mouse_controller.move_cursor()
            self.employee_controller.move_employees()
            self.employee_controller.hire_employee(self.first_room.rect.midleft)
            self.interface_service.update_time()
            self.draw()
            self.clock.tick(30)
            pygame.display.flip()

    def update_text(self):
        self.stress = self.font.render(
            "Stress: " + str(self.employee_controller.employee_service.employee_list[0].needs.stress), True,
            (255, 255, 255))

        self.motivation = self.font.render(
            "Motivation: " + str(self.employee_controller.employee_service.employee_list[0].needs.motivation), True,
            (255, 255, 255))
        self.clock_time = self.font.render("Time: " + self.interface_service.get_clock_progress_str(), True, (255, 255, 255))
        if self.interface_service.view_type == self.interface_service.HIRE_EMPLOYEE and self.interface_service.hire_element.candidates_are_present():
            emp = self.interface_service.hire_element.get_selected_emp()
            abilities = emp.get("abilities")
            name = emp.get("name")
            salary = emp.get("salary")
            self.emp_name = self.font.render("Name: " + name, True, (255, 255, 255))
            self.stomach = self.font.render("Hunger: " + str(abilities[0]), True, (255, 255, 255))
            self.boredom = self.font.render("Boredom: " + str(abilities[1]), True, (255, 255, 255))
            self.anxiety = self.font.render("Anxiety: " + str(abilities[2]), True, (255, 255, 255))
            self.salary = self.font.render("Salary: " + str(salary), True, (255, 255, 255))
            self.experience = self.font.render("Experience: ", True, (255, 255, 255))  # could be shown by levels: low, medium, high
        elif self.interface_service.view_type == self.interface_service.STATISTICS:
            self.interface_service.statistics_element.update_text()

    def draw(self):
        for floor in range(0, len(self.building_controller.get_room_board())):
            for room in self.building_controller.get_room_board()[floor]:
                self.screen.blit(room.image, room.rect)
                # for action_obj in room.action_objects:
                #     pygame.draw.rect(self.screen,(0,0,0),action_obj.rect)
        if self.mouse_controller.cursor.drags_room():
            self.screen.blit(self.mouse_controller.cursor.image, self.mouse_controller.cursor.rect.move(-150, -150))
        for emp in self.employee_controller.employee_service.employee_list:
            self.screen.blit(emp.image, emp.rect)

        # draw all elements of interface
        for element in self.interface_service.element_list:
            # icons should always be displayed and elements should only be displayed if user clicked on icon
            if issubclass(element.__class__, StaticElement) or self.interface_service.view_type != self.interface_service.NO_TYPE:
                # draw hover effect
                if element.hover_effect == element.DROP_SHADOW:
                    self.screen.blit(element.hover_surface, element.rect)
                self.screen.blit(element.image, element.rect)

        if self.interface_service.emp_stat_element.hover_effect == self.interface_service.emp_stat_element.SHOW_STATISTICS:
            self.screen.blit(self.interface_service.emp_stat_element.background_surface, self.interface_service.emp_stat_element.rect)
            self.screen.blit(self.interface_service.emp_stat_element.name_text, self.interface_service.emp_stat_element.rect.move(10, 10))
            self.screen.blit(self.interface_service.emp_stat_element.hunger_text, self.interface_service.emp_stat_element.rect.move(10, 30))
            self.screen.blit(self.interface_service.emp_stat_element.stress_text, self.interface_service.emp_stat_element.rect.move(10, 50))
            self.screen.blit(self.interface_service.emp_stat_element.motivation_text,
                             self.interface_service.emp_stat_element.rect.move(10, 70))
            self.screen.blit(self.interface_service.emp_stat_element.sales_text, self.interface_service.emp_stat_element.rect.move(10, 90))
            self.screen.blit(self.interface_service.emp_stat_element.emp_name_text, self.interface_service.emp_stat_element.rect.move(110, 10))
            self.screen.blit(self.interface_service.emp_stat_element.hunger_bar, self.interface_service.emp_stat_element.rect.move(110, 35))
            self.screen.blit(self.interface_service.emp_stat_element.stress_bar, self.interface_service.emp_stat_element.rect.move(110, 55))
            self.screen.blit(self.interface_service.emp_stat_element.motivation_bar,
                             self.interface_service.emp_stat_element.rect.move(110, 75))
            self.screen.blit(self.interface_service.emp_stat_element.sales_number_text,
                             self.interface_service.emp_stat_element.rect.move(120, 90))

        # draw different views based on which icon user clicked
        if self.interface_service.view_type == self.interface_service.HIRE_EMPLOYEE:
            self.screen.blit(self.interface_service.hire_element.background_surface,
                             self.interface_service.hire_element.rect.move(-20, -20))
            if self.interface_service.hire_element.candidates_are_present():
                self.screen.blit(self.interface_service.hire_element.get_current_emp_image(), self.interface_service.hire_element.rect)
                self.screen.blit(self.emp_name, self.interface_service.hire_element.rect.move(70, 0))
                self.screen.blit(self.stomach, self.interface_service.hire_element.rect.move(70, 30))
                self.screen.blit(self.anxiety, self.interface_service.hire_element.rect.move(70, 60))
                self.screen.blit(self.boredom, self.interface_service.hire_element.rect.move(70, 90))
                self.screen.blit(self.salary, self.interface_service.hire_element.rect.move(70, 120))
                self.screen.blit(self.interface_service.hire_element.get_capital_text(),self.interface_service.hire_element.capital_rect)
        elif self.interface_service.view_type == self.interface_service.STATISTICS:
            self.screen.blit(self.interface_service.statistics_element.get_stat_image(), self.interface_service.statistics_element.rect)
            if self.interface_service.statistics_element.is_game_stats():
                for i in range(0, len(self.interface_service.statistics_element.game_stat_list)):
                    self.screen.blit(self.interface_service.statistics_element.game_stat_list[i],
                                     self.interface_service.statistics_element.game_stat_rect.move(0, 30 * i))
        elif self.interface_service.view_type == self.interface_service.PURCHASE_ROOM:
            self.screen.blit(self.interface_service.building_element.background_surface,
                             self.interface_service.building_element.rect.move(-20, -10))
            self.screen.blit(self.interface_service.building_element.cost_number_text,
                             self.interface_service.building_element.cost_rect)
            self.screen.blit(self.interface_service.building_element.get_room_image(), self.interface_service.building_element.rect)
            self.screen.blit(self.interface_service.building_element.get_capital_text(), self.interface_service.building_element.capital_rect)
        elif self.interface_service.view_type == self.interface_service.CALENDAR:
            self.screen.blit(self.interface_service.calendar_element.image, self.interface_service.calendar_element.rect)
            self.screen.blit(self.interface_service.calendar_element.get_current_page_image(),
                             self.interface_service.calendar_element.page_rect)
            self.screen.blit(self.interface_service.calendar_element.text_background,
                             self.interface_service.calendar_element.month_text_rect.move(-5, -5))
            self.screen.blit(self.interface_service.calendar_element.get_month_text(),
                             self.interface_service.calendar_element.month_text_rect)
            if self.interface_service.calendar_element.at_current_page():
                pygame.draw.rect(self.screen, (255, 0, 0), self.interface_service.calendar_element.page_marker_rect, 3)

        pygame.draw.line(self.screen, (0, 0, 0), (397, 55), self.interface_service.clock_element.clk_pointer, 5)
        # self.screen.blit(self.hunger, self.text_rect.move(0, 125))
        # self.screen.blit(self.stress, self.text_rect.move(0, 100))
        # self.screen.blit(self.motivation, self.text_rect.move(0, 150))

    def init_objects(self):
        self.ground = Ground(self.screen)
        self.company = Company()
        self.company.money = 20000

        self.interface_service = InterfaceService(self.company)
        self.building_controller = BuildingController()
        self.employee_controller = EmployeeController(self.building_controller.get_room_board(), self.ground, self.company,
                                                      self.interface_service)

        self.employee_controller.create_employee(100, 200)
        self.building_controller.build_room((0, 0), RoomType.CORRIDOR)
        self.building_controller.build_room((1, 0), RoomType.DINING_ROOM)
        self.building_controller.build_room((2, 0), RoomType.OFFICE_ROOM)
        self.building_controller.build_room((3, 0), RoomType.ELEVATOR)
        self.building_controller.build_room((4, 0), RoomType.CORRIDOR)
        self.building_controller.build_room((5, 0), RoomType.CONFERENCE_ROOM)
        self.building_controller.build_room((6, 0), RoomType.CORRIDOR)

        self.mouse_controller = MouseController(self.screen, self.employee_controller.employee_service.employee_list,
                                                self.building_controller, self.ground, self.interface_service)
        self.keyboard_controller = KeyboardController(self.employee_controller, self.building_controller, self.mouse_controller.cursor,
                                                      self.company, self.ground)

        self.first_room = self.building_controller.building_service.room_board[0][0]

        # self.employee_controller.create_employee(120, 280, "Bob2", self._company)
        self.employee_controller.employee_service.employee_list[0].needs.hunger = 20
        self.employee_controller.employee_service.employee_list[0].needs.stress = 20

    def init_texts(self):
        self.font = pygame.font.SysFont("Calibri", 24, True)
        self.text_rect = pygame.Rect(0, 0, 1, 1)

    def init_screen(self):
        pygame.display.init()
        self.res_list = [
            (1600, 900),
            (1440, 900),
            (1360, 768),
            (1280, 720),
            (800, 600)
        ]
        self.res_option = 4
        self.full_screen = False
        self.current_res = self.res_list[4]
        self.screen = pygame.display.set_mode(self.current_res)
        self.clock = pygame.time.Clock()


if __name__ == "__main__":
    Game()
