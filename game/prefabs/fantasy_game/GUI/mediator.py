from game.battle.GUI.mediator import AbstractNotifier
from game.battle.GUI.mediator import AbstractMediator

# TODO: move to window manager pygame wrapper
from pygame.time import wait


class AbstractGuiMediator(AbstractMediator):

    def reset_scene_components(self):
        self._widget_selected_action_display.set_text('Select action')

        self._widget_selected_target_display.set_text('')
        self._widget_selected_target_display.set_visible(False)

        self._feedback_display.set_visible(False)

        self._widget_player_actions_menu.reset_selection()
        self._widget_team1.reset_selection()
        self._widget_team2.reset_selection()

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
                    self.redraw_all()

                    move = self._battle_wrapper.get_AI_selection()
                    print(self._battle_wrapper.get_move_txt(move))
                    self._feedback_display.set_text(self._battle_wrapper.get_move_txt(move))
                    self.redraw_all()
                    wait(2000)

                    result = self._battle_wrapper.do_AI_move(move)
                    print(result)
                    self._feedback_display.set_text(result)
                    self.redraw_all()
                    wait(2000)

                    self._feedback_display.set_visible(False)

                    self.reset_scene_components()
                    self.redraw_all()
                    if self._battle_wrapper.game_over():
                        pass

        self.redraw_all()
