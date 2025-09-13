from pygame import time
from pygame.threads import Thread


class EmployeeTaskThread(Thread):

    def __init__(self):
        self.work_dict = {}
        self.hunger_dict = {}
        self.stress_dict = {}
        self.motivation_dict = {}
        self.bladder_dict = {}
        self.stop = False
        super().__init__()

    def empty_dict(self):
        return len(self.work_dict) == 0 and len(self.hunger_dict) == 0 and len(self.stress_dict) == 0 and len(self.motivation_dict) == 0 and len(self.bladder_dict) == 0

    def insert_emp_work(self, emp):
        self.work_dict[id(emp)] = emp

    def insert_emp_hunger(self, emp):
        self.hunger_dict[id(emp)] = emp

    def insert_emp_stress(self, emp):
        self.stress_dict[id(emp)] = emp

    def insert_emp_bladder(self, emp):
        self.bladder_dict[id(emp)] = emp

    def insert_emp_motivation(self, emp):
        self.motivation_dict[id(emp)] = emp

    def pop_emp_work(self, emp):
        if self.work_dict.__contains__(id(emp)):
            self.work_dict.pop(id(emp))

    def pop_emp_hunger(self, emp):
        if self.hunger_dict.__contains__(id(emp)):
            self.hunger_dict.pop(id(emp))

    def pop_emp_stress(self, emp):
        if self.stress_dict.__contains__(id(emp)):
            self.stress_dict.pop(id(emp))

    def pop_emp_motivation(self, emp):
        if self.motivation_dict.__contains__(id(emp)):
            self.motivation_dict.pop(id(emp))

    def pop_emp_bladder(self, emp):
        if self.bladder_dict.__contains__(id(emp)):
            self.bladder_dict.pop(id(emp))

    def run(self):
        while not self.stop:
            if not self.empty_dict():
                for employee in self.work_dict.values():
                    employee.make_sale()
                for employee in self.hunger_dict.values():
                    employee.needs.eat()
                for employee in self.stress_dict.values():
                    employee.needs.play()
                for employee in self.motivation_dict.values():
                    employee.needs.meet()
                for employee in self.bladder_dict.values():
                    employee.needs.pee()
                time.wait(4000)

    def destroy(self):
        self.stop = True
