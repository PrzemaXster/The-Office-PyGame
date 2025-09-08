class AnimationEventListener:
    def __init__(self):
        self.anim_start_queue = []
        self.anim_end_queue = []

    def add_new_anim(self, animation):
        self.anim_start_queue.append(animation)

    def notify_anim_end(self, animation):
        self.anim_end_queue.append(animation)
