from pygame import draw, font, Rect

from controller.BuildController import BuildingController
from controller.EmployeeController import EmployeeController
from controller.MouseController import MouseController
from service.EmployeeServices.EmployeeManagement.AnimationService import AnimationService
from service.Interface.InterfaceService import InterfaceService
from view.Draw.InterfaceDrawing import InterfaceDrawing


class Drawing:
    def __init__(self,
                 screen,
                 building_controller: BuildingController,
                 mouse_controller: MouseController,
                 employee_controller: EmployeeController,
                 animation_service: AnimationService,
                 interface_service: InterfaceService):
        self.init_texts()
        self.interface_drawing = InterfaceDrawing(screen, interface_service, self.font, self.text_rect)
        self.screen = screen
        self.building_controller = building_controller
        self.mouse_controller = mouse_controller
        self.employee_controller = employee_controller
        self.animation_service = animation_service
        self.interface_service = interface_service


    def draw(self):
        for floor in range(0, len(self.building_controller.get_room_board())):
            for room in self.building_controller.get_room_board()[floor]:
                self.screen.blit(room.image, room.rect)
                # for action_obj in room.action_objects:
                #     pygame.draw.rect(self.screen, (0, 0, 0), action_obj.rect)
        if self.mouse_controller.cursor.drags_room():
            self.screen.blit(self.mouse_controller.cursor.image, self.mouse_controller.cursor.rect.move(-150, -150))
        for emp in self.employee_controller.employee_service.employee_list:
            self.screen.blit(emp.image, emp.rect)

        self.interface_drawing.draw_interface()

        for animation in self.animation_service.anim_object_list:
            self.screen.blit(animation.current_sprite, animation.rect)

        draw.line(self.screen, (0, 0, 0), (397, 55), self.interface_service.clock_element.clk_pointer, 5)
        # self.screen.blit(self.hunger, self.text_rect.move(0, 125))
        # self.screen.blit(self.stress, self.text_rect.move(0, 100))
        # self.screen.blit(self.motivation, self.text_rect.move(0, 150))

    def update_text(self):
        self.stress = self.font.render(
            "Stress: " + str(self.employee_controller.employee_service.employee_list[0].needs.stress), True,
            (255, 255, 255))

        self.motivation = self.font.render(
            "Motivation: " + str(self.employee_controller.employee_service.employee_list[0].needs.motivation), True,
            (255, 255, 255))
        self.clock_time = self.font.render("Time: " + self.interface_service.get_clock_progress_str(), True,
                                           (255, 255, 255))
        self.interface_drawing.update_text()


    def init_texts(self):
        self.font = font.SysFont("Calibri", 24, True)
        self.text_rect = Rect(0, 0, 1, 1)

