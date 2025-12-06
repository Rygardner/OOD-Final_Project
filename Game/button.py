"""
    This module has the button class
"""
import pygame


class button:
    """
        a button object and its functions
    """

    def __init__(self,
                 rect: pygame.Rect,
                 text: str,
                 text_color: tuple[int, int, int],
                 color: tuple[int, int, int],
                 size: int) -> None:
        pygame.font.init()
        self.font: pygame.font.Font = pygame.font.Font(None, size)
        self.rect: pygame.Rect = rect
        self.text: str = text
        self.text_color: tuple[int, int, int] = text_color
        self.color: tuple[int, int, int] = color

    def draw_button(self, surface: pygame.Surface) -> None:
        """
            draws button on screen with text
        """
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)

        # Render text centered in the rect
        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def button_clicked(self) -> bool:
        # If no display surface exists yet, skip mouse logic
        if pygame.display.get_surface() is None:
            return False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        return self.rect.collidepoint(mouse_pos) and mouse_pressed
