from pygame import Surface


class InterfaceElement:
    """
    Superclass of all interface elements.

    It's stored in InterfaceService in element_list.
    """

    def __init__(self, rect, image, on_click=None, on_hover=None):
        self.rect = rect
        self.image = image
        self.hover_surface = Surface(self.rect.size)
        self.hover_surface.set_alpha(128)
        self.hover_surface.fill((255, 255, 255))

        self._on_click = on_click
        self._on_hover = on_hover
        self.NO_EFFECT = 0
        self.DROP_SHADOW = 1
        self.SHOW_STATISTICS = 2
        self.hover_effect = self.NO_EFFECT

    def click(self):
        """
        A pointer to a function called _on_click which triggers when the element is clicked.
        It's actual implementation is stored in InterfaceElement, to have access to a wide variety of tools/objects.
        """
        if self._on_click is not None:
            self._on_click()

    def hover(self, element):
        """
        Basically same as above, but also passes reference to the clicked interface element, like a button.
        """
        if self._on_hover is not None:
            self._on_hover(element)
