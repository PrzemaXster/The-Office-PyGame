from service.EmployeeThreads.EmployeeTaskThread import EmployeeTaskThread


class TaskService:
    def __init__(self,thread : EmployeeTaskThread):
        self.task_thread = thread

    def insert_emp(self, emp, type):
        if type == "work":
            self.task_thread.insert_emp_work(emp)
        elif type == "hunger":
            self.task_thread.insert_emp_hunger(emp)
        elif type == "stress":
            self.task_thread.insert_emp_stress(emp)
        elif type == "motivation":
            self.task_thread.insert_emp_motivation(emp)
        elif type == "bladder":
            self.task_thread.insert_emp_bladder(emp)

    def pop_emp(self, emp, type):
        if type == "work":
            self.task_thread.pop_emp_work(emp)
        elif type == "hunger":
            self.task_thread.pop_emp_hunger(emp)
        elif type == "stress":
            self.task_thread.pop_emp_stress(emp)
        elif type == "motivation":
            self.task_thread.pop_emp_motivation(emp)
        elif type == "bladder":
            self.task_thread.pop_emp_bladder(emp)




