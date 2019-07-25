from game.prefabs.fantasy_game.GUI.wrapper import BattleWrapper

from pygame.time import wait

class WindowManager:
    def init_scene(self):
        raise NotImplementedError('Abstract Method')

    def erase_screen(self):
        raise NotImplementedError('Abstract Method')

    def display_all(self):
        raise NotImplementedError('Abstract Method')

    def set_gui_interaction_enabled(self, enabled: bool = True):
        raise NotImplementedError('Abstract Method')


class AbstractNotifier:
    pass

class AbstractMediator:
    def notify_mouseover(self, sender: AbstractNotifier) -> None:
        pass
    def notify_mouseout(self, sender: AbstractNotifier) -> None:
        pass
    def notify_click(self, sender: AbstractNotifier, param: None) -> None:
        pass

class GuiComponent(AbstractNotifier):

    mediator = AbstractMediator()
    interaction_enabled = True


    def __init__(self):
        super().__init__()
        self._visible = True

    def update(self):
        pass

    def draw(self):
        pass

class TextComponent(GuiComponent):

    def set_text(self, txt: str):
        raise NotImplementedError('Abstract Method')

    def set_visible(self, visible: bool):
        self._visible = visible

    def visible(self):
        return self._visible

    def draw(self):
        if self.visible():
            self._draw()

    def _draw(self):
        raise NotImplementedError('Abstract Method')


class SpriteContainerComponent(GuiComponent):

    def get_display_text(self) -> str:
        return ''

    def draw(self):
        pass

    def reset_selection(self):
        pass

class ActionsMenuComponent(SpriteContainerComponent):
    def set_actions(self, actions: dict):
        raise NotImplementedError('Abstract Method')




class AbstractGuiMediator(AbstractMediator):

    def __init__(self,
                 tw1: SpriteContainerComponent, tw2: SpriteContainerComponent,
                 pam:ActionsMenuComponent,
                 sad: TextComponent, std: TextComponent,
                 bw: BattleWrapper,
                 wm: WindowManager,
                 fd: TextComponent
                 ):

        # widgets
        self._widget_team1 = tw1
        self._widget_team2 = tw2

        self._widget_selected_action_display = sad
        self._widget_selected_target_display = std
        self._widget_player_actions_menu = pam

        # business logic
        self._battle_wrapper = bw
        self._window_manager = wm

        # setup widgets
        self._widget_player_actions_menu.set_actions(self._battle_wrapper.get_possible_moves())

        self._feedback_display = fd

        self._selected_action = None
        #self._selected_target = None

    def init_scene(self):
        self._window_manager.init_scene()
        self._widget_selected_target_display.set_visible(False)
        self._feedback_display.set_visible(False)

        self.redraw_all()

    def redraw_all(self):
        self._window_manager.erase_screen()
        self._widget_team1.draw()
        self._widget_team2.draw()
        self._widget_player_actions_menu.draw()

        self._widget_selected_action_display.draw()
        self._widget_selected_target_display.draw()
        self._feedback_display.draw()


        self._window_manager.display_all()

    def _update_selected_action_display(self, txt):
        self._widget_selected_action_display.set_text(txt)

    def _update_selected_target_display(self, txt):
        self._widget_selected_target_display.set_text(txt)

class PlayerTurnMediator(AbstractGuiMediator):


    def notify_mouseover(self, sender: AbstractNotifier, param=None) -> None:



        if sender is self._widget_player_actions_menu:
            txt = self._widget_player_actions_menu.get_display_text()
            self._widget_selected_action_display.set_text(txt)

        if sender is self._widget_team2:
            if self._selected_action is not None:
                txt = self._battle_wrapper.get_action_simuation_text(self._selected_action, param)
                self._widget_selected_target_display.set_text(txt)

        self.redraw_all()

    def notify_mouseout(self, sender: AbstractNotifier):
        self.redraw_all()

    def notify_click(self, sender: AbstractNotifier, param=None):
        if sender is self._widget_player_actions_menu:
            self._selected_action = param
            self._widget_selected_target_display.set_text('Select target')
            self._widget_selected_target_display.set_visible(True)

        if self._selected_action is not None:
            if sender is self._widget_team2:

                move_result_txt = self._battle_wrapper.do_player_move(str(self._selected_action), str(param))
                self._feedback_display.set_text(move_result_txt)
                self._feedback_display.set_visible(True)
                self._widget_player_actions_menu.reset_selection()
                self._widget_team2.reset_selection()
                self.redraw_all()
                wait(2000)

                if self._battle_wrapper.game_over():
                    pass
                else:
                    #AI move simulation
                    self._window_manager.set_gui_interaction_enabled(False)

                    move = self._battle_wrapper.get_AI_selection()
                    print(self._battle_wrapper.get_move_txt(move))
                    self._feedback_display.set_text(self._battle_wrapper.get_move_txt(move))
                    self.redraw_all()
                    wait(2000)

                    result = self._battle_wrapper.do_AI_move(move)
                    self._feedback_display.set_text(result)
                    self.redraw_all()
                    wait(2000)
                    self._widget_player_actions_menu.set_actions(self._battle_wrapper.get_possible_moves())
                    self._widget_selected_action_display.set_text('')
                    self._widget_selected_target_display.set_text('')
                    self._widget_selected_target_display.set_visible(False)
                    self._window_manager.set_gui_interaction_enabled(True)
                    if self._battle_wrapper.game_over():
                        pass

        self.redraw_all()
