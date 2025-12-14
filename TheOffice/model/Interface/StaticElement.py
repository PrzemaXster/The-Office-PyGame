from model.Interface.InterfaceElement import InterfaceElement


# Element that never disappears
class StaticElement(InterfaceElement):
    """
    Interface Element that never disappears, e.g toolbar icons, clock.
    Anything that isn't a StaticElement will only be displayed if the self.view_type != self.NO_TYPE.
    """
    def __init__(self, rect, image, on_click=None, on_hover=None):
        super().__init__(rect, image, on_click, on_hover)
