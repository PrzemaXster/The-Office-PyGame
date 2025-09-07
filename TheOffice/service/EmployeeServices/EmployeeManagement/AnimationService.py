from pygame import time

from model.Animation.AnimationEventListener import AnimationEventListener
from model.Animation.AnimationObject import AnimationObject

# Takes all static animation objects from the animation_event_listener and runs a loop
# through each obj animating them.
# Separately, it does animations on employees
class AnimationService:
    def __init__(self, animation_event_listener: AnimationEventListener):
        self.wait_time = 0.1 * 1000
        self.previous_time_map = {}
        self._animation_event_listener = animation_event_listener
        self.anim_object_list = []

    def animate_employee(self, employee):
        if not self.previous_time_map.__contains__(id(employee)):
            self.previous_time_map[id(employee)] = time.get_ticks()
        if time.get_ticks() - self.previous_time_map[id(employee)] > self.wait_time:
            self.previous_time_map[id(employee)] = time.get_ticks()
            if employee.direction == 'L':
                if employee.current_position == employee.WALK_LEFT:
                    employee.change_walking_sprite(employee.WALK_LEFT2)
                elif employee.current_position == employee.WALK_LEFT2:
                    employee.change_walking_sprite(employee.WALK_LEFT3)
                elif employee.current_position == employee.WALK_LEFT3:
                    employee.change_walking_sprite(employee.WALK_LEFT4)
                else:
                    employee.change_walking_sprite(employee.WALK_LEFT)
            elif employee.direction == 'R':
                if employee.current_position == employee.WALK_RIGHT:
                    employee.change_walking_sprite(employee.WALK_RIGHT2)
                elif employee.current_position == employee.WALK_RIGHT2:
                    employee.change_walking_sprite(employee.WALK_RIGHT3)
                elif employee.current_position == employee.WALK_RIGHT3:
                    employee.change_walking_sprite(employee.WALK_RIGHT4)
                else:
                    employee.change_walking_sprite(employee.WALK_RIGHT)

    def animate_objects(self):
        self.anim_object_list.extend(self._animation_event_listener.anim_start_queue)
        current_timestamp = time.get_ticks()
        for anim_object in self.anim_object_list:
            self._animate_object(anim_object, current_timestamp)
            if anim_object.animation_length_ms is not None and current_timestamp - anim_object.start_time > anim_object.animation_length_ms:
                self._animation_event_listener.notify_anim_end(anim_object)
        for anim_obj in self._animation_event_listener.anim_end_queue:
            self.anim_object_list.remove(anim_obj)
        self.clear_event_listener()


    def _animate_object(self, anim_obj: AnimationObject, current_timestamp):
        # actually do the animation
        # if interval between sprites is good, then change the current sprite
        if current_timestamp - anim_obj.last_sprite_time >= anim_obj.interval_per_sprite_ms:
            # update the current sprite, by just shifting current sprite position by one
            sprite_index = anim_obj.sprite_list.index(anim_obj.current_sprite) + 1
            if sprite_index >= len(anim_obj.sprite_list):
                sprite_index = 0
            anim_obj.current_sprite = anim_obj.sprite_list[sprite_index]
            anim_obj.last_sprite_time = current_timestamp

    def clear_event_listener(self):
        self._animation_event_listener.anim_start_queue.clear()
        self._animation_event_listener.anim_end_queue.clear()
