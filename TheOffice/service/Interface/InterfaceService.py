from pygame import image, time
from pygame.rect import Rect

from model.Interface.BuildingElement import BuildingElement
from model.Interface.CalendarElement import CalendarElement
from model.Interface.ClockElement import ClockElement
from model.Interface.EmployeeStatElement import EmployeeStatElement
from model.Interface.HireElement import HireElement
from model.Interface.InterfaceElement import InterfaceElement
from model.Interface.StaticElement import StaticElement
from model.Interface.StatisticsElement import StatisticsElement
from service.RoomType import RoomType


class InterfaceService:
    def __init__(self, company):
        self._time_dist = 900
        self._timestamp = time.get_ticks()
        self.calendar_element = CalendarElement(Rect(250, 170, 283, 192),
                                                image.load("../resources/interface/elements/calendar/calendar.png"))
        self.clock_element = ClockElement(Rect(20, 0, 1, 45), image.load("../resources/interface/elements/clock.png"))
        self.building_element = BuildingElement(Rect(250, 170, 283, 192), image.load("../resources/rooms/office.png"), company)
        self.hire_element = HireElement(Rect(290, 200, 60, 140), image.load("../resources/employees/male/emp1/employee.png"), company)
        self.statistics_element = StatisticsElement(Rect(250, 170, 283, 192),
                                                    image.load("../resources/interface/elements/statistics/game_stats.png"), company)
        self.emp_stat_element = EmployeeStatElement(Rect(0, 0, 0, 0), None)

        self.arrow_right_element = InterfaceElement(Rect(570, 170, 100, 170), image.load("../resources/interface/elements/right.png"),
                                                    self.switch_view_right, self.drop_shadow)
        self.arrow_left_element = InterfaceElement(Rect(120, 170, 100, 170), image.load("../resources/interface/elements/left.png"),
                                                   self.switch_view_left, self.drop_shadow)
        self.accept_element = InterfaceElement(Rect(290, 395, 90, 90), image.load("../resources/interface/icons/accept.png"),
                                               self.click_accept, self.drop_shadow)
        self.reject_element = InterfaceElement(Rect(410, 400, 80, 80), image.load("../resources/interface/icons/reject.png"),
                                               self.click_reject, self.drop_shadow)
        self.calendar_icon = StaticElement(Rect(220, 8, 75, 60), image.load("../resources/interface/icons/calendar.png"),
                                           self.click_calendar, self.drop_shadow)
        self.statistics_icon = StaticElement(Rect(120, 8, 75, 60), image.load("../resources/interface/icons/stats.png"),
                                             self.click_statistics, self.drop_shadow)

        self.build_icon = StaticElement(Rect(520, 8, 75, 60), image.load("../resources/interface/icons/build.png"), self.click_build,
                                        self.drop_shadow)
        self.hire_icon = StaticElement(Rect(620, 8, 75, 60), image.load("../resources/interface/icons/hire.png"), self.click_hire,
                                       self.drop_shadow)
        self.element_list = [self.arrow_left_element, self.arrow_right_element, self.accept_element, self.reject_element,
                             self.clock_element, self.calendar_icon, self.build_icon, self.hire_icon, self.statistics_icon]

        self.NO_TYPE = 0
        self.PURCHASE_ROOM = 1
        self.HIRE_EMPLOYEE = 2
        self.SETTINGS = 3
        self.CALENDAR = 4
        self.STATISTICS = 5
        self.view_type = self.NO_TYPE
        self.purchased_room = RoomType.NONE
        self.hired_emp = None

    def update_time(self):
        if time.get_ticks() - self._timestamp > self._time_dist:
            self.clock_element.tick()
            theta = 360 * self.clock_element.progress / 100
            self.clock_element.update_clock(theta)
            if self.clock_element.progress == 99:
                self.calendar_element.update()
                if self.calendar_element.current_date.day % 7:
                    self.click_reject()
                    self.hire_element.generate_candidates()
            self._timestamp = time.get_ticks()

    def get_clock_progress_str(self):
        return self.clock_element.get_progress_str()

    # on clicks
    def switch_view_right(self):
        if self.view_type == self.HIRE_EMPLOYEE:
            self.hire_element.next_employee()
        elif self.view_type == self.STATISTICS:
            self.statistics_element.next_stat()
        elif self.view_type == self.PURCHASE_ROOM:
            self.building_element.next_room()
        elif self.view_type == self.CALENDAR:
            self.calendar_element.next_page()

    def switch_view_left(self):
        if self.view_type == self.HIRE_EMPLOYEE:
            self.hire_element.previous_employee()
        elif self.view_type == self.statistics_element:
            self.statistics_element.previous_stat()
        elif self.view_type == self.PURCHASE_ROOM:
            self.building_element.previous_room()
        elif self.view_type == self.CALENDAR:
            self.calendar_element.previous_page()

    def click_accept(self):
        if self.view_type == self.PURCHASE_ROOM:
            if self.building_element.room_purchased():
                self.purchased_room = self.building_element._room_index
            else:
                return
        elif self.view_type == self.HIRE_EMPLOYEE:
            self.hired_emp = self.hire_element.hire_selected_emp()
            self.hire_element.reset_selection()
        self.view_type = self.NO_TYPE

    def click_reject(self):
        self.view_type = self.NO_TYPE

    def click_calendar(self):
        if self.view_type != self.NO_TYPE:
            self.view_type = self.NO_TYPE
        else:
            self.view_type = self.CALENDAR

    def click_build(self):
        if self.view_type != self.NO_TYPE:
            self.view_type = self.NO_TYPE
        else:
            self.view_type = self.PURCHASE_ROOM

    def click_hire(self):
        if self.view_type != self.NO_TYPE:
            self.view_type = self.NO_TYPE
        else:
            self.view_type = self.HIRE_EMPLOYEE

    def click_statistics(self):
        if self.view_type != self.NO_TYPE:
            self.view_type = self.NO_TYPE
        else:
            self.view_type = self.STATISTICS

    # on hovers
    def drop_shadow(self, element: InterfaceElement):
        element.hover_effect = element.DROP_SHADOW
