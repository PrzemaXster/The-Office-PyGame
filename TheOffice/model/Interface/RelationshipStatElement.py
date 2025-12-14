from pygame import font, Surface

from model.Employee.Employee import Employee
from model.Interface.ActorInteractionInterfaceElement import ActorInteractionInterfaceElement


class RelationshipStatElement(ActorInteractionInterfaceElement):
    def __init__(self, rect, image, _on_click=None):
        super().__init__(rect, image, on_click=_on_click)
        self.background_surface = Surface((300, 190))
        self.background_surface.set_alpha(150)
        self.background_surface.fill((0, 0, 0))
        self._title_font = font.SysFont("Calibri", 25, True)
        self._body_font = font.SysFont("Calibri", 18, True)
        self.title = self._title_font.render("Relationships", True, (255, 255, 255))
        self.rel_text_list = []
        self.rel_stat_rect = rect.copy().move(20, 20)

    def update_emp_relationships(self, employee: Employee, limit, offset):
        rel_subset = list(employee.relations.items())[offset:offset + limit]
        self.rel_text_list.clear()
        for emp, rel in rel_subset:
            self.rel_text_list.append(self._body_font.render(emp.name + "  :  " + str(rel) , True, (255, 255, 255)))
