# TODO: move to window manager pygame wrapper
from pygame.time import wait
from game.battle.GUI.mediator import AbstractMediator, GuiComponent


class DefaultMediator(AbstractMediator):
    def reset_scene_components(self):
        self._widget_selected_action_display.set_text('Select action')
        self._widget_player_actions_menu.set_actions(self._battle_wrapper.get_possible_moves())

        self._widget_selected_target_display.set_text('')
        self._widget_selected_target_display.set_visible(False)

        self._feedback_display.set_visible(False)

        self._widget_player_actions_menu.reset_selection()
        self._widget_team1.reset_selection()
        self._widget_team2.reset_selection()


    def notify_mouseover(self, sender: GuiComponent, param=None) -> None:
        if sender is self._widget_player_actions_menu:
            self._window_manager.update_display_text(
                self._widget_selected_action_display,
                self._widget_player_actions_menu.get_display_text()
            )

        if sender is self._widget_team2:
            if self._selected_action is not None:
                self._window_manager.update_display_text(
                    self._widget_selected_target_display,
                    self._battle_wrapper.get_action_simuation_text(self._selected_action, param)
                )
        self.redraw_all()

    def notify_mouseout(self, sender: GuiComponent):
        self.redraw_all()

    def notify_click(self, sender: GuiComponent, param=None):
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
                    self._window_manager.display_endgame()
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

                    self.reset_scene_components()
                    self.redraw_all()

                    self._feedback_display.set_visible(False)

                    #self.reset_scene_components()
                    self.redraw_all()

        if self._battle_wrapper.game_over():
            self._window_manager.display_endgame()
        else:
            self.redraw_all()
