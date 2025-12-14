from model.Interface.InterfaceElement import InterfaceElement


class ActorInteractionInterfaceElement(InterfaceElement):
    """
    Superclass of all interface elements that trigger when clicking on an actor (e.g. employee, room etc.).
    They keep a reference to an object in the click_element() method.

    They are explicitly used in the MouseController while iterating through a specific type of actor.
    """

    def __init__(self, rect, image, on_click=None, on_hover=None):
        super().__init__(rect, image, on_click, on_hover)

    def click_actor(self, actor):
        if self._on_click is not None:
            self._on_click(actor)


    def hover_actor(self, element, actor):
        if self._on_hover is not None:
            self._on_hover(element, actor)
