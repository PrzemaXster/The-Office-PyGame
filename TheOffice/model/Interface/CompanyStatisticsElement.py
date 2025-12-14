from pygame import font, Rect
from pygame import image

from model.Company import Company
from model.Interface.InterfaceElement import InterfaceElement


class CompanyStatisticsElement(InterfaceElement):
    def __init__(self, rect, img, company: Company):
        super().__init__(rect, img)
        self._company = company
        self._stat_image_list = [image.load("../resources/interface/elements/statistics/game_stats.png")]
        self._sysfont = font.SysFont("Calibri", 30, True)
        self.game_stat_rect = rect.move(20, 20)
        self.game_stat_list = [
            self._sysfont.render("Capital: ", True, 0),
            self._sysfont.render("Papers sold: ", True, 0),
            self._sysfont.render("Employees: ", True, 0)
        ]
        self._stat_index = 0
        self._GAME_STATS = 0

    def get_stat_image(self):
        return self._stat_image_list[self._stat_index]

    def next_stat(self):
        self._stat_index += 1
        if self._stat_index == len(self._stat_image_list):
            self._stat_index = 0

    def previous_stat(self):
        self._stat_index -= 1
        if self._stat_index < 0:
            self._stat_index = len(self._stat_image_list) - 1

    def update_text(self):
        self.game_stat_list = [
            self._sysfont.render("Capital: " + str(self._company.money), True, 0),
            self._sysfont.render("Papers sold: " + str(self._company.papers_sold), True, 0),
            self._sysfont.render("Employees: " + str(self._company.employee_num), True, 0)
        ]

    def is_game_stats(self):
        return self._stat_index == self._GAME_STATS
