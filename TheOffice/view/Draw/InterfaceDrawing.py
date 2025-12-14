from pygame import draw

from model.Interface.StaticElement import StaticElement


class InterfaceDrawing:
    def __init__(self, screen, interface_service, font, text_rect):
        self.interface_service = interface_service
        self._screen = screen
        self.font = font
        self.text_rect = text_rect

    def draw_interface(self):
        # draw all elements of interface
        for element in self.interface_service.element_list:
            # icons should always be displayed and elements should only be displayed if user clicked on icon
            if issubclass(element.__class__,
                          StaticElement) or self.interface_service.view_type != self.interface_service.NO_TYPE:
                # draw hover effect
                if element.hover_effect == element.DROP_SHADOW:
                    self._screen.blit(element.hover_surface, element.rect)
                self._screen.blit(element.image, element.rect)

        self._draw_emp_stats_on_hover(self.interface_service.emp_stat_element)
        # draw different views based on which icon user clicked
        if self.interface_service.view_type == self.interface_service.HIRE_EMPLOYEE:
            self._screen.blit(self.interface_service.hire_element.background_surface,
                              self.interface_service.hire_element.rect.move(-20, -20))
            if self.interface_service.hire_element.candidates_are_present():
                self._screen.blit(self.interface_service.hire_element.get_current_emp_image(),
                                  self.interface_service.hire_element.rect)
                self._screen.blit(self.emp_name, self.interface_service.hire_element.rect.move(70, 0))
                self._screen.blit(self.stomach, self.interface_service.hire_element.rect.move(70, 30))
                self._screen.blit(self.anxiety, self.interface_service.hire_element.rect.move(70, 60))
                self._screen.blit(self.boredom, self.interface_service.hire_element.rect.move(70, 90))
                self._screen.blit(self.salary, self.interface_service.hire_element.rect.move(70, 120))
                self._screen.blit(self.interface_service.hire_element.get_capital_text(),
                                  self.interface_service.hire_element.capital_rect)
        elif self.interface_service.view_type == self.interface_service.STATISTICS:
            self._screen.blit(self.interface_service.statistics_element.get_stat_image(),
                              self.interface_service.statistics_element.rect)
            if self.interface_service.statistics_element.is_game_stats():
                for i in range(0, len(self.interface_service.statistics_element.game_stat_list)):
                    self._screen.blit(self.interface_service.statistics_element.game_stat_list[i],
                                      self.interface_service.statistics_element.game_stat_rect.move(0, 30 * i))
        elif self.interface_service.view_type == self.interface_service.PURCHASE_ROOM:
            self._screen.blit(self.interface_service.building_element.background_surface,
                              self.interface_service.building_element.rect.move(-20, -10))
            self._screen.blit(self.interface_service.building_element.cost_number_text,
                              self.interface_service.building_element.cost_rect)
            self._screen.blit(self.interface_service.building_element.get_room_image(),
                              self.interface_service.building_element.rect)
            self._screen.blit(self.interface_service.building_element.get_capital_text(),
                              self.interface_service.building_element.capital_rect)
        elif self.interface_service.view_type == self.interface_service.CALENDAR:
            self._screen.blit(self.interface_service.calendar_element.image,
                              self.interface_service.calendar_element.rect)
            self._screen.blit(self.interface_service.calendar_element.get_current_page_image(),
                              self.interface_service.calendar_element.page_rect)
            self._screen.blit(self.interface_service.calendar_element.text_background,
                              self.interface_service.calendar_element.month_text_rect.move(-5, -5))
            self._screen.blit(self.interface_service.calendar_element.get_month_text(),
                              self.interface_service.calendar_element.month_text_rect)
            if self.interface_service.calendar_element.at_current_page():
                draw.rect(self._screen, (255, 0, 0), self.interface_service.calendar_element.page_marker_rect,
                          3)
        elif self.interface_service.view_type == self.interface_service.EMP_FULL_STATS:
            self._screen.blit(self.interface_service.emp_stat_full_element.background_surface,
                              self.interface_service.emp_stat_full_element.rect)
            self._screen.blit(self.interface_service.emp_stat_full_element.title_text,
                              self.interface_service.emp_stat_full_element.stat_rect)
            self._screen.blit(self.interface_service.emp_stat_full_element.salary_text,
                              self.interface_service.emp_stat_full_element.stat_rect.move(-10, 30))
            self._screen.blit(self.interface_service.emp_stat_full_element.hire_date,
                              self.interface_service.emp_stat_full_element.stat_rect.move(-10, 60))
            self._screen.blit(self.interface_service.emp_stat_full_element.papers_sold_text,
                              self.interface_service.emp_stat_full_element.stat_rect.move(-10, 90))
            self._screen.blit(self.interface_service.emp_stat_full_element.emp_name_text,
                              self.interface_service.emp_stat_full_element.visual_rect)
        elif self.interface_service.view_type == self.interface_service.RELATIONSHIP_STATS:
            self._screen.blit(self.interface_service.relationship_stat_element.background_surface,
                              self.interface_service.relationship_stat_element.rect)
            self._screen.blit(self.interface_service.relationship_stat_element.title,
                              self.interface_service.relationship_stat_element.rel_stat_rect)
            for i in range(len(self.interface_service.relationship_stat_element.rel_text_list)):
                self._screen.blit(self.interface_service.relationship_stat_element.rel_text_list[i],
                                  self.interface_service.relationship_stat_element.rel_stat_rect.move(0,  50 + i * 20))


    def _draw_emp_stats_on_hover(self, emp_stat_element):
        if emp_stat_element.hover_effect == emp_stat_element.SHOW_STATISTICS:
            self._screen.blit(emp_stat_element.background_surface,
                              emp_stat_element.rect)
            self._screen.blit(emp_stat_element.name_text,
                              emp_stat_element.rect.move(10, 10))
            self._screen.blit(emp_stat_element.hunger_text,
                              emp_stat_element.rect.move(10, 30))
            self._screen.blit(emp_stat_element.stress_text,
                              emp_stat_element.rect.move(10, 50))
            self._screen.blit(emp_stat_element.motivation_text,
                              emp_stat_element.rect.move(10, 70))

            self._screen.blit(emp_stat_element.emp_name_text,
                              emp_stat_element.rect.move(110, 10))
            self._screen.blit(emp_stat_element.hunger_bar,
                              emp_stat_element.rect.move(110, 35))
            self._screen.blit(emp_stat_element.stress_bar,
                              emp_stat_element.rect.move(110, 55))
            self._screen.blit(emp_stat_element.motivation_bar,
                              emp_stat_element.rect.move(110, 75))
            self._screen.blit(emp_stat_element.bladder_text,
                              emp_stat_element.rect.move(10, 90))
            self._screen.blit(emp_stat_element.bladder_bar,
                              emp_stat_element.rect.move(110, 90))
            self._screen.blit(emp_stat_element.sales_number_text,
                              emp_stat_element.rect.move(120, 110))
            self._screen.blit(emp_stat_element.sales_text,
                              emp_stat_element.rect.move(10, 110))

    def update_text(self):
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
            self.experience = self.font.render("Experience: ", True,
                                               (255, 255, 255))  # could be shown by levels: low, medium, high
        elif self.interface_service.view_type == self.interface_service.STATISTICS:
            self.interface_service.statistics_element.update_text()