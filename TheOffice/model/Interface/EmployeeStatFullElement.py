from datetime import date

from pygame import font
from pygame.surface import Surface

from model.Employee.Employee import Employee
from model.Interface.ActorInteractionInterfaceElement import ActorInteractionInterfaceElement


class EmployeeStatFullElement(ActorInteractionInterfaceElement):
    def __init__(self, rect, image, company, _on_click):
        super().__init__(rect, image, on_click=_on_click)
        self.company = company
        self.background_surface = Surface((300, 190))
        self.background_surface.set_alpha(150)
        self.background_surface.fill((0, 0, 0))

        self._title_font = font.SysFont("Calibri", 25, True)
        self._body_font = font.SysFont("Calibri", 18, True)

        self.title_text = self._title_font.render("Statistics", True, (255, 255, 255))
        self.name_text = self._body_font.render("", True, (255, 255, 255))
        self.salary_text = self._body_font.render("Salary:        ", True, (255, 255, 255))
        self.hire_date = self._body_font.render("Days Working:    ", True, (255, 255, 255))
        self.papers_sold_text = self._body_font.render("Papers Sold:    ", True, (255, 255, 255))
        self.money_made_text = self._body_font.render("Money Made:    ", True, (255, 255, 255))
        self.sold_per_hour_text = self._body_font.render("Papers Sale Per Hour:    ", True, (255, 255, 255))
        self.stat_rect = rect.copy().move(20, 20)
        self.visual_rect = rect.copy().move(200, 30)

    def update_emp_full_stats(self, emp: Employee):
        self.name_text = self._body_font.render(emp.name, True, (255, 255, 255))
        self.salary_text = self._body_font.render("Salary:        " + str(emp.stats.salary), True, (255, 255, 255))
        self.hire_date = self._body_font.render("Hire Date:    " + emp.stats.hire_date.strftime("%d/%m/%Y"), True, (255, 255, 255))
        self.papers_sold_text = self._body_font.render("Papers Sold:    " + str(emp.stats.papers_sold), True,(255, 255, 255))
        self.money_made_text = self._body_font.render("Money Made:    " + str(emp.stats.papers_sold * self.company.PAPER_COST), True, (255, 255, 255))
        self.sold_per_hour_text = self._body_font.render("Papers Sale Per Hour:    ", True, (255, 255, 255))
        self.sales_number_text = self._title_font.render(str(emp.stats.papers_sold), True, (255, 255, 255))
        self.emp_name_text = self._body_font.render(str(emp.name), True, (255, 255, 255))
