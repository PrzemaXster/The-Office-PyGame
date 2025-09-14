from model.Animation.AnimationObject import AnimationObject


class AnimationCollection(AnimationObject):
    def __init__(self, animation_list: list):
        self.animation_list = animation_list
        self.rect = self.Rect(animation_list)

    def trigger(self):
        for animation in self.animation_list:
            animation.trigger()

    def stop(self):
        for animation in self.animation_list:
            animation.stop()

    class Rect:
        def __init__(self, animation_list):
            self.animation_list = animation_list

        def move(self, x, y):
            for animation in self.animation_list:
                animation.rect.move(x, y)