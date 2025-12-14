from pygame import Rect, Surface, time

from model.Animation.AnimationEventListener import AnimationEventListener


class AnimationObject:
    def __init__(self, rect: Rect, sprite_list: list, animation_event_listener: AnimationEventListener,
                 interval_per_sprite_ms=125, animation_time_ms=None):
        self.rect = rect
        self.sprite_list = sprite_list
        self.current_sprite = sprite_list[0]
        self.animation_event_listener = animation_event_listener
        self.animation_length_ms = animation_time_ms
        self.interval_per_sprite_ms = interval_per_sprite_ms
        self.start_time = 0
        self.last_sprite_time = 0

    def trigger(self):
        self.animation_event_listener.add_new_anim(self)
        self.start_time = time.get_ticks()

    def stop(self):
        self.animation_event_listener.notify_anim_end(self)
