from pygame import font
from pygame.surface import Surface

from model.Employee.Employee import Employee
from model.Interface.ActorInteractionInterfaceElement import ActorInteractionInterfaceElement
from model.Interface.InterfaceElement import InterfaceElement


class EmployeeStatElement(ActorInteractionInterfaceElement):
    def __init__(self, rect, image, on_hover):
        super().__init__(rect, image, on_hover=on_hover)
        self.background_surface = Surface((170, 140))
        self.background_surface.set_alpha(180)
        self.background_surface.fill((0, 0, 0))
        self._sysfont = font.SysFont("Calibri", 18, True)
        self.name_text = self._sysfont.render("Name: ", True, (255, 255, 255))
        self.hunger_text = self._sysfont.render("Hunger: ", True, (255, 255, 255))
        self.stress_text = self._sysfont.render("Stress:", True, (255, 255, 255))
        self.motivation_text = self._sysfont.render("Motivation: ", True, (255, 255, 255))
        self.bladder_text = self._sysfont.render("Bladder: ", True, (255, 255, 255))
        self.sales_text = self._sysfont.render("Sales: ", True, (255, 255, 255))
        self.sales_number_text = self._sysfont.render("", True, (255, 255, 255))
        self.emp_name_text = self._sysfont.render("",True,(255,255,255))
        self.hunger_bar = Surface((100, 10))
        self.hunger_bar.fill((255, 0, 0))
        self.stress_bar = Surface((100, 10))
        self.stress_bar.fill((0, 255, 0))
        self.bladder_bar = Surface((100, 10))
        self.bladder_bar.fill((255, 255, 0))
        self.motivation_bar = Surface((100, 10))
        self.motivation_bar.fill((0, 0, 255))

    def update_emp_stats(self, emp: Employee):
        self.rect.x = emp.rect.x + 60
        self.rect.y = emp.rect.y - 80
        self.hunger_bar = Surface((emp.needs.hunger / 2, 10))
        self.hunger_bar.fill((255, 0, 0))
        self.stress_bar = Surface((emp.needs.stress / 2, 10))
        self.stress_bar.fill((0, 255, 0))
        self.motivation_bar = Surface((emp.needs.motivation / 2, 10))
        self.motivation_bar.fill((0, 0, 255))
        self.bladder_bar = Surface((emp.needs.bladder / 2, 10))
        self.bladder_bar.fill((255, 255 , 0))
        self.sales_number_text = self._sysfont.render(str(emp.stats.papers_sold), True, (255, 255, 255))
        self.emp_name_text = self._sysfont.render(str(emp.name), True, (255, 255, 255))
