import pygame
from pygame.locals import *

from game.prefabs.fantasy_game.GUI.widgets import PlayerActionsMenu, TeamWidget, TextWidget, BaseSprite
from game.prefabs.fantasy_game.GUI.wrapper import BattleWrapper
from game.prefabs.fantasy_game.GUI.core import load_image

from game.prefabs.fantasy_game.GUI.mediator import GuiComponent, PlayerTurnMediator, WindowManager

class WindowManagerWrapper(WindowManager):

    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._background = None


    def init_scene(self):
        # basic init
        pygame.init()
        pygame.mixer.quit()
        pygame.display.set_caption('sandbox')
        background = pygame.Surface(self._screen.get_size())
        bg_image, bg_image_rect = load_image('bg.png')
        background.blit(bg_image, bg_image_rect)
        self._background = background

    def erase_screen(self):
        self._screen.blit(self._background, (0, 0))

    def display_all(self):
        pygame.display.flip()


class StandardManager:
    def __init__(self, team1, team2):
        self._screen = pygame.display.set_mode((1024, 768))
        self._background = None
        # team 1
        self._team_widget_1 = TeamWidget(
            self._screen,
            distance_from_middle=10,
            sprites_spacing=5,
            bottom=self._screen.get_rect().height - 100,
            left_side=True
        )
        self._team_widget_1.set_characters(team1)

        # team 2
        self._team_widget_2 = TeamWidget(
            self._screen,
            distance_from_middle=10,
            sprites_spacing=5,
            bottom=self._screen.get_rect().height - 100,
            left_side=False
        )
        self._team_widget_2.set_characters(team2)

        self._selected_action_display = TextWidget(surface=self._screen, size=20, rect=pygame.Rect(200, 10, 300, 100))
        self._selected_target_display = TextWidget(surface=self._screen, size=20, rect=pygame.Rect(550, 10, 300, 100))
        self._player_actions_menu = PlayerActionsMenu(surface=self._screen, top=10, left=10, sprite_spacing=10)

        self._feedback_display = TextWidget(surface=self._screen, size=20, rect=pygame.Rect(200, 120, 300, 100))


        bw = BattleWrapper(team1, team2)
        wm = WindowManagerWrapper(self._screen)

        self._bw = bw
        self._player_actions_menu.set_actions(bw.get_possible_moves())
        self._is_over = False

        GuiComponent.mediator = PlayerTurnMediator(
            self._team_widget_1,
            self._team_widget_2,
            self._player_actions_menu,
            self._selected_action_display,
            self._selected_target_display,
            bw,wm,
            self._feedback_display
        )

        GuiComponent.mediator.init_scene()

    def next(self):
        going = True
        for event in pygame.event.get():

            if event.type == QUIT:
                going = False

            elif pygame.key.get_pressed()[K_ESCAPE]:
                going = False

            if not self._is_over:
                if event.type == MOUSEBUTTONDOWN:
                    BaseSprite.user_clicked = True
                    self._update_interactive_widgets()
                    BaseSprite.user_clicked = False

                # iteration code here
                if self._bw.game_over():
                    self._the_end(self._screen)
                    self._is_over = True
                else:
                    self._update_interactive_widgets()

        return going



    def _the_end(self, screen):
        rt_widget = pygame.font.SysFont('Comic Sans MS', 100)
        rect_to_use = pygame.Rect(280, 150, 500, 20)
        widget = rt_widget.render('The end', True, (255, 0, 0), (255, 255, 255))
        screen.blit(widget, rect_to_use)

        pygame.display.flip()

    def _update_interactive_widgets(self):
        self._player_actions_menu.update()
        self._team_widget_1.update()
        self._team_widget_2.update()
