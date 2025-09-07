from model.Employee.Employee import Employee
from service.EmployeeServices.Needs.TaskService import TaskService


class CollisionService:
    def __init__(self, room_board: dict, task_service_t: TaskService):
        self.room_board = room_board
        self.task_service_t = task_service_t

    @staticmethod
    def adjust_emp_to_action_object(emp, desk, room, desk_i):
        if type(room).__name__ == "DiningRoom":
            # print(desk_i)
            emp.rect.x = desk.rect.x
            emp.rect.y = desk.rect.y
            if desk_i % 2 != 0:
                emp.sitting_sprite_right()
                emp.rect = emp.rect.move(-25, - 24)
            else:
                emp.sitting_sprite_left()
                emp.rect = emp.rect.move(-2, - 26)
        elif type(room).__name__ == "OfficeRoom":
            emp.rect.x = desk.rect.x
            emp.rect.y = desk.rect.y
            emp.rect = emp.rect.move(10, - 10)
            emp.sitting_sprite_back()
        elif type(room).__name__ == "GameRoom":
            emp.rect.x = desk.rect.x
            emp.rect.y = desk.rect.y
            if desk_i < 2:
                emp.rect = emp.rect.move(0, -9)
                emp.sitting_sprite_back_game()
            elif desk_i == 2:
                emp.rect = emp.rect.move(7, - 25)
                emp.sitting_sprite_left()
            else:
                emp.rect = emp.rect.move(-24, - 22)
                emp.sitting_sprite_right()
        elif type(room).__name__ == "ConferenceRoom":
            emp.rect.x = desk.rect.x
            emp.rect.y = desk.rect.y
            if desk_i % 2 != 0:
                emp.sitting_sprite_right()
                emp.rect = emp.rect.move(-20, -15)
            else:
                emp.sitting_sprite_left()
                emp.rect = emp.rect.move(0, -15)
        elif type(room).__name__ == "Toilet":
            emp.rect.x = desk.rect.x + 10
            emp.rect.y = desk.rect.y + 45
            emp.sitting_sprite_disappear()


    def handle_emp_desk_collide(self, emp : Employee):
        for floor_i in range(0, len(self.room_board)):
            room_list = list(self.room_board[floor_i])
            for room_i in range(0, len(self.room_board[floor_i])):
                if emp.rect.colliderect(room_list[room_i].rect):
                    emp.coord = (room_i, floor_i)
                for desk_i in range(0, len(room_list[room_i].action_objects)):
                    if emp.rect.colliderect(room_list[room_i].action_objects[desk_i].rect):
                        if self.action_object_taken(room_list, room_i, desk_i) is False:
                            if type(room_list[room_i]).__name__ == "DiningRoom":
                                self.task_service_t.insert_emp(emp, "hunger")
                            elif type(room_list[room_i]).__name__ == "OfficeRoom":
                                self.task_service_t.insert_emp(emp, "work")
                            elif type(room_list[room_i]).__name__ == "GameRoom":
                                self.task_service_t.insert_emp(emp, "stress")
                            elif type(room_list[room_i]).__name__ == "ConferenceRoom":
                                self.task_service_t.insert_emp(emp, "motivation")
                            elif type(room_list[room_i]).__name__ == "Toilet":
                                self.task_service_t.insert_emp(emp, "bladder")
                            self.update_action_object_status(room_list[room_i].action_objects[desk_i])
                            emp.destination = None
                            emp.set_desk(room_list[room_i].action_objects[desk_i])
                            self.adjust_emp_to_action_object(emp, room_list[room_i].action_objects[desk_i], room_list[room_i], desk_i)

    def handle_emp_desk_detach_event(self, emp):
        if emp.assigned_furniture is not None:
            emp.remove_from_desk()
            self.task_service_t.pop_emp(emp, "hunger")
            self.task_service_t.pop_emp(emp, "work")
            self.task_service_t.pop_emp(emp, "stress")
            self.task_service_t.pop_emp(emp, "motivation")
            self.task_service_t.pop_emp(emp, "bladder")

    def action_object_taken(self, room_list, room_i, desk_i):
        action_object = room_list[room_i].action_objects[desk_i]
        # print(type(action_object.taken).__name__)
        # print("tru czynie tru",(action_object.taken == True and action_object.taken == True))
        return action_object.taken

    @staticmethod
    def update_action_object_status(action_object):
        action_object.taken = True

