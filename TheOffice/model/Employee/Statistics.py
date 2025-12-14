from datetime import date


class Statistics:
    def __init__(self, salary, hire_date : date):
        self.papers_sold = 0
        self.days = 0
        self.base = 1
        self.hire_date = hire_date
        self.salary = salary