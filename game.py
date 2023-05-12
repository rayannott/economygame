

import pygame

from player import Player
from gui.gui_rect import Button, Label, ProgressBar, Panel
from gui.pygame_utils import BLACK, FRAMERATE, WINDOW_SIZE, FONT_HUGE, FONT_HINT, CP0


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.player = Player()
        self.ingame_time: float = 0. # time the game was active, seconds
        self.victory = False

        # setup pygame
        pygame.display.set_caption('Game')
        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)

        self.background = pygame.Surface(WINDOW_SIZE)
        self.background.fill(pygame.Color(BLACK))

        self.clock = pygame.time.Clock()

        self.is_running = True


        # setup GUIs
        self.btn = Button((120, 120), (220, 60), self.window_surface, 'Hello', 'this is a test button', FONT_HUGE)
        self.progr = ProgressBar((200, 200), (200, 40), self.window_surface, 0.0, True, 'health')
        self.panel = Panel((430, 300), (400, 400), self.window_surface, 'panel')

        self.panel.populate_one(
            'btn', 
            Button((10, 60), (120, 40), self.window_surface, 'hey', 'this is a test panel button', parent=self.panel)
        )
        self.panel.populate_one(
            'pb',
            ProgressBar((10, 120), (120, 40), self.window_surface, 0.7, parent=self.panel, text='testing')
        )
        self.panel.add_text_objects(
            [Label('[test text]', self.window_surface, FONT_HINT, CP0[0], topleft=(10, 10))]
        )

    def update(self):
        ...

    def run(self):
        '''
        Infinite game loop
        '''
        while self.is_running:
            self.clock.tick(FRAMERATE)
            self.window_surface.blit(self.background, (0, 0))
            pos = pygame.mouse.get_pos()

            self.btn.update(pos)
            self.progr.update(pos)
            self.panel.update(pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn.clicked():
                        self.progr.change_progress(0.05)
                    if self.panel.clicked():
                        print('panel')
                        if self.panel.gui_objects['btn'].clicked():
                            self.panel.gui_objects['pb'].change_progress(-0.01) # type: ignore


            pygame.display.update()

    def tick(self):
        '''
        This function is executed every tick (that is, every second)
        '''
        ...
