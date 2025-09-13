from pygame import time
from pygame.threads import Thread


class EmployeeNeedThread(Thread):
    def __init__(self):
        super().__init__()
        self.emp_dict = {}
        self.stop = False

    def insert_emp(self, employee):
        self.emp_dict[id(employee)] = employee

    def empty_dict(self):
        if len(self.emp_dict) == 0:
            return True
        return False

    def pop_emp(self, employee):
        self.emp_dict.pop(id(employee))

    def get_emp(self, identity):
        return self.emp_dict.get(identity)

    def run(self):
        need_i = 0
        while not self.stop:
            if self.empty_dict() == False:
                for employee in self.emp_dict.values():
                    if need_i <= 1:
                        if employee.is_working():
                            employee.needs.decrease_stress()
                            employee.needs.decrease_bladder()
                    if need_i == 1:
                        employee.needs.decrease_hunger()
                    elif need_i == 2:
                        employee.needs.decrease_motivation()
                        need_i = 0
                need_i += 1
                time.wait(7000)

    def destroy(self):
        self.stop = True
