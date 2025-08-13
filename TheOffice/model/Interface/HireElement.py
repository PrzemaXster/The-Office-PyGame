import random

from pygame import transform, image, Surface, font
from pygame.rect import Rect

from model.Interface.InterfaceElement import InterfaceElement


class HireElement(InterfaceElement):
    def __init__(self, rect, img, company):
        super().__init__(rect, img)
        self._company = company
        self._emp_list = [
            {"name": "Steve", "abilities": (6, 4, 7), "images_path": "../resources/employees/male/emp2/", "salary": 3400},
            {"name": "Joe", "abilities": (7, 4, 2), "images_path": "../resources/employees/male/emp3/", "salary": 3400},
            {"name": "Marle", "abilities": (3, 8, 8), "images_path": "../resources/employees/female/emp1/", "salary": 3400},
        ]
        self._init_emp_lists()
        self._emp_index = 0
        self.background_surface = Surface((240, 190))
        self.background_surface.set_alpha(150)
        self.background_surface.fill((0, 0, 0))
        self._sysfont = font.SysFont("Calibri", 30, True)
        self.capital_rect = Rect(20, 550, 50, 30)
        self.MALE = 0
        self.FEMALE = 1

    def get_current_emp_image(self):
        return transform.scale(image.load(self._emp_list[self._emp_index].get("images_path") + "employee.png"), (60, 140))

    def get_selected_emp(self):
        return self._emp_list[self._emp_index]

    def hire_selected_emp(self):
        if len(self._emp_list) == 0:
            return None
        return self._emp_list.pop(self._emp_index)

    def get_capital_text(self):
        return self._sysfont.render(str(self._company.money), True, (255, 255, 255), (0, 0, 0))

    def next_employee(self):
        self._emp_index += 1
        if self._emp_index == len(self._emp_list):
            self._emp_index = 0

    def previous_employee(self):
        self._emp_index -= 1
        if self._emp_index < 0:
            self._emp_index = len(self._emp_list) - 1

    def reset_selection(self):
        self._emp_index = 0

    def generate_candidates(self):
        self._emp_list = []
        self.reset_selection()
        for i in range(0, random.randint(1, 4)):
            self._generate_candidate()

    def candidates_are_present(self):
        return len(self._emp_list) > 0

    def _generate_candidate(self):
        if random.randint(0, 1) == self.MALE:
            self._emp_list.append(
                {"name": self._emp_names_male[random.randint(0, len(self._emp_names_male) - 1)],
                 "abilities": (random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)),
                 "images_path": self._emp_images_male[random.randint(0, len(self._emp_images_male) - 1)],
                 "salary": random.randint(3000, 4000)})
        else:
            self._emp_list.append(
                {"name": self._emp_names_female[random.randint(0, len(self._emp_names_female) - 1)],
                 "abilities": (random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)),
                 "images_path": self._emp_images_female[random.randint(0, len(self._emp_images_female) - 1)],
                 "salary": random.randint(3000, 4000)})

    def _init_emp_lists(self):
        self._emp_names_male = [
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
        self._emp_names_female = [
            "Karen",
            "Jamie",
            "Miranda",
            "Britney",
            "Courtney",
            "Kelsey",
            "Candice",
            "Nina",
            "Natalie",
            "Margaret",
            "Sofie"
        ]
        self._emp_images_male = [
            "../resources/employees/male/emp1/",
            "../resources/employees/male/emp2/",
            "../resources/employees/male/emp3/"
        ]
        self._emp_images_female = [
            "../resources/employees/female/emp1/"
        ]
