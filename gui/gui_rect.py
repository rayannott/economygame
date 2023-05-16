from abc import ABC, abstractmethod
from typing import Union

import pygame

from gui.gui_utils import FONT_NORM
from .gui_utils import BLACK, CP0, FONT_HUGE, FONT_SMALL, FONT_NORM, GREY, WHITE, WINDOW_SIZE, shift


class Label:
    def __init__(self, text: str, surface: pygame.Surface, font: pygame.font.Font, color: str, **kwargs) -> None:
        self.text = text
        self.surface = surface
        self.font = font
        self.color = color

        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(**kwargs)

    def update(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.draw()

    def draw(self):
        self.surface.blit(self.text_surface, self.rect)
    
    def set_text(self, set_to: str) -> None:
        self.text = set_to
    
    def set_color(self, set_to):
        self.color = set_to


class GUIRect(ABC):
    '''
    Base class for all rectangular gui objects (buttons, progress bars, etc.)
    '''
    def __init__(
            self, 
            topleft: tuple[float, float], 
            size: tuple[float, float], 
            surface: pygame.Surface,
            text: str = '',
            hoverhint: str = '',
            text_font: pygame.font.Font = FONT_NORM,
            parent: Union['Panel', None] = None
            ) -> None:
        
        super().__init__()
        self.topleft = topleft
        self.size = size
        self.surface = surface
        self.text = text
        self.text_font = text_font
        self.shift_by = parent.rect.topleft if parent else (0, 0)
        self.hoverhint = hoverhint
        self.visible = True
        self.active = True
        self.hovering = False # boolean flag updated every frame
        self.clickable = False
        self.depth = 1 if parent else 0
        self.color_text = WHITE
        self.color_hint = WHITE
        self.color_frame = WHITE

        self.rect = pygame.Rect(shift(self.topleft, self.shift_by), self.size)

        self.text_label = Label(self.text, self.surface, self.text_font, self.color_text, center=self.rect.center)
        self.hint_label = Label(self.hoverhint, self.surface, FONT_SMALL, self.color_hint, bottomleft=(3, WINDOW_SIZE[1] - 3))
    
    def set_visible(self, set_to: bool) -> None:
        self.visible = set_to
        
    def set_active(self, set_to: bool) -> None:
        self.active = set_to

    def clicked(self) -> bool:
        return self.active and self.hovering

    @abstractmethod
    def update(self, current_mouse_pos: tuple[int, int]):
        self.hovering = self.rect.collidepoint(*current_mouse_pos)
        if self.hoverhint and self.hovering:
            self.hint_label.update()
        self.draw()
        if self.visible:
            self.text_label.update()

    @abstractmethod
    def draw(self) -> None:
        if self.visible:
            pygame.draw.rect(self.surface, self.color_frame, self.rect, width=2 if self.hovering else 1, border_radius=3)

    def set_text(self, set_to: str) -> None:
        self.text_label.set_text(set_to)

    def set_frame_color(self, set_to: str):
        self.color_frame = set_to


class Button(GUIRect):
    def __init__(self, topleft: tuple[float, float], size: tuple[float, float], surface: pygame.Surface, 
                 text: str = '', hoverhint: str = '', text_font = FONT_NORM, parent = None) -> None:
        super().__init__(topleft, size, surface, text, hoverhint, text_font, parent)
        self.clickable = True
    
    def update(self, current_mouse_pos: tuple[int, int]):
        return super().update(current_mouse_pos)
    
    def draw(self) -> None:
        return super().draw()


class ProgressBar(GUIRect):
    def __init__(self, 
                topleft: tuple[float, float], 
                size: tuple[float, float], 
                surface: pygame.Surface, 
                progress: float = 0,
                display_progress: bool = True,
                text: str = '',
                hoverhint: str = '',
                parent = None) -> None:
        super().__init__(topleft, size, surface, text, hoverhint, parent=parent)
        self.progress = progress # number between 0 and 1
        self.display_progress = display_progress

        self.progress_rect = pygame.rect.Rect(0, 0, 0, 0)
        self.progress_rect.size = int(self.rect.width * self.progress * 0.97), int(self.rect.height * 0.85)
        self.progress_rect.center = self.rect.center

        self.progress_label = Label(f'{int(self.progress*100)}', self.surface, FONT_SMALL, WHITE, center=self.rect.topleft)
    
    def set_progress(self, set_to: float) -> None:
        if set_to <= 1.009:
            self.progress = set_to
        
    def change_progress(self, delta: float) -> None:
        if 0 <= self.progress + delta <= 1.009:
            self.progress += delta
    
    def update(self, current_mouse_pos: tuple[int, int]):
        self.progress_rect.size = int(self.rect.width * self.progress * 0.97), int(self.rect.height * 0.85)
        self.progress_rect.center = self.rect.center
        if self.display_progress:
            self.progress_label.set_text(f'{int(self.progress*100)}')
            self.progress_label.update()
        return super().update(current_mouse_pos)
    
    def draw(self) -> None:
        if self.visible:
            pygame.draw.rect(self.surface, GREY, self.progress_rect, border_radius=3)
        return super().draw()


class Panel(GUIRect):
    def __init__(self, topleft: tuple[float, float], size: tuple[float, float], 
                surface: pygame.Surface, hoverhint: str = '', parent = None) -> None:
        super().__init__(topleft, size, surface, '', hoverhint, parent=parent)
        self.gui_objects: dict[str, Union[Button, ProgressBar, Panel]] = {} # interactive objects like buttons
        self.labels: list[Label] = []

    def populate_one(self, label: str, gui_object: Union[Button, ProgressBar, 'Panel']) -> None:
        gui_object.depth += self.depth
        gui_object.hint_label.rect.centerx = gui_object.hint_label.rect.centerx + 150 * gui_object.depth
        self.gui_objects[label] = gui_object
    
    def populate_many(self, gui_objects: dict[str, Union[Button, ProgressBar, 'Panel']]) -> None:
        for k, v in gui_objects.items():
            self.populate_one(k, v)

    def add_labels(self, text_objects: list[Label]) -> None:
        for to in text_objects:
            to.rect.topleft = shift(to.rect.topleft, self.rect.topleft)
            self.labels.append(to)

    def draw(self) -> None:
        return super().draw()

    def update(self, current_mouse_pos: tuple[int, int]):
        for gui_obj in self.gui_objects.values():
            gui_obj.update(current_mouse_pos)
        if self.visible:
            for to in self.labels:
                to.update()
        return super().update(current_mouse_pos)

    def object_clicked(self) -> str:
        '''Returns a key of the clicked object'''
        for obj_key, gui_obj in self.gui_objects.items():
            if gui_obj.clicked():
                return obj_key
        return ''


class Notification(Panel):
    def __init__(self, text: str, surface: pygame.Surface, pos: tuple[int, int], duration_tics=5) -> None:
        self.lines = text.split('\n')
        max_len = len(max(self.lines, key=len))
        super().__init__(topleft=pos, size=(13 * max_len, 30 * len(self.lines)), surface=surface, hoverhint='', parent=None)
        self.duration_ticks = duration_tics
        self.color_frame = CP0[0]
        self.inner_rect = pygame.rect.Rect(shift(self.rect.topleft, (3, 3)), shift(self.rect.size, (-6, -6)))
        for i, one_line in enumerate(self.lines):
            self.add_labels(
                [
                    Label(one_line, self.surface, FONT_SMALL, BLACK, topleft=(5, 5 + 30*i))
                ]
            )

    def tick(self):
        if self.active:
            self.duration_ticks -= 1
            if self.duration_ticks <= 0:
                self.active = False
                self.visible = False
    
    def draw(self) -> None:
        super().draw()
        if self.visible:
            pygame.draw.rect(self.surface, WHITE, self.inner_rect, border_radius=3)
    
    def update(self, current_mouse_pos: tuple[int, int]):
        self.draw()
        if self.visible:
            for to in self.labels:
                to.update()
