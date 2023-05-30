'''
All curcilar gui objects
'''

from abc import ABC, abstractmethod
from typing import Optional

import pygame

from gui.gui_rect import Label, Panel
from gui.gui_utils import FONT_SMALL, WHITE, WINDOW_SIZE


class GUICircle(ABC):
    def __init__(
            self,
            center: tuple[float, float],
            radius: float,
            surface: pygame.Surface,
            hoverhint: str = '',
            parent: Optional[Panel] = None
        ) -> None:
        super().__init__()
        self.center = center
        self.radius = radius
        self.surface = surface
        self.hoverhint = hoverhint
        self.parent = parent
        self.active = True
        self.visible = True
        self.hovering = False # boolean flag updated every frame
        self.depth = 1 if parent else 0

        self.color_frame = WHITE

        self.hint_label = Label(self.hoverhint, self.surface, FONT_SMALL, WHITE, bottomleft=(3, WINDOW_SIZE[1] - 3))
    
    def set_visible(self, set_to: bool) -> None:
        self.visible = set_to

    def set_active(self, set_to: bool) -> None:
        self.active = set_to

    def set_frame_color(self, set_to: str):
        self.color_frame = set_to

    def clicked(self) -> bool:
        return self.active and self.hovering

    @abstractmethod
    def draw(self) -> None:
        if self.visible:
            pygame.draw.circle(self.surface, self.color_frame, self.center, self.radius, width=2 if self.hovering else 1)

    @abstractmethod
    def update(self, current_mouse_pos: tuple[int, int]):
        self.hovering = (current_mouse_pos[0] - self.center[0])**2 + (current_mouse_pos[1] - self.center[1])**2 < self.radius**2
        if self.hoverhint and self.hovering:
            self.hint_label.update()
        self.draw()


class DummyCircle(GUICircle):
    def __init__(self, center: tuple[float, float], radius: float, surface: pygame.Surface, hoverhint: str = '', parent: Panel | None = None) -> None:
        super().__init__(center, radius, surface, hoverhint, parent)
    
    def draw(self) -> None:
        return super().draw()
    
    def update(self, current_mouse_pos: tuple[int, int]):
        return super().update(current_mouse_pos)


class ProgressCircle(GUICircle):
    pass
