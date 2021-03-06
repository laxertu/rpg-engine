from game.battle.wrapper import BattleWrapper


class GuiComponent:

    mediator = None

    def __init__(self):
        super().__init__()
        self._visible = True

    def update(self):
        pass

    def set_visible(self, visible: bool):
        self._visible = visible

    def visible(self) -> bool:
        return self._visible

    def draw(self):
        if self.visible():
            self.do_draw()

    def do_draw(self):
        pass

class AbstractTextComponent(GuiComponent):

    def set_text(self, txt: str):
        raise NotImplementedError('Abstract Method')


class AbstractSelectorComponent(GuiComponent):

    def get_display_text(self) -> str:
        """
        TODO: move to more specific class
        :return:
        """
        return ''

    def set_display_text(self, txt: str):
        """
        TODO: move to more specific class
        :return:
        """
        pass


    def draw(self):
        pass

    def reset_selection(self):
        pass

class ActionsMenuComponent(AbstractSelectorComponent):
    def set_actions(self, actions: dict):
        raise NotImplementedError('Abstract Method')


class WindowManager:
    def init_scene(self):
        raise NotImplementedError('Abstract Method')

    def erase_screen(self):
        raise NotImplementedError('Abstract Method')

    @staticmethod
    def update_display_text(display: AbstractTextComponent, txt: str):
        display.set_text(txt)

    def display_all(self):
        raise NotImplementedError('Abstract Method')

    def display_endgame(self):
        raise NotImplementedError('Abstract method')

class AbstractMediator:
    def __init__(self,
                 tw1: AbstractSelectorComponent, tw2: AbstractSelectorComponent,
                 pam:ActionsMenuComponent,
                 sad: AbstractTextComponent, std: AbstractTextComponent,
                 bw: BattleWrapper,
                 wm: WindowManager,
                 fd: AbstractTextComponent
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

    def notify_mouseover(self, sender: GuiComponent) -> None:
        pass
    def notify_mouseout(self, sender: GuiComponent) -> None:
        pass
    def notify_click(self, sender: GuiComponent, param: None) -> None:
        pass

    def init_scene(self):
        self._window_manager.init_scene()
        self.reset_scene_components()
        self.redraw_all()

    def reset_scene_components(self):
        pass

    def redraw_all(self):
        self._window_manager.erase_screen()
        self._widget_team1.draw()
        self._widget_team2.draw()
        self._widget_player_actions_menu.draw()

        self._widget_selected_action_display.draw()
        self._widget_selected_target_display.draw()
        self._feedback_display.draw()


        self._window_manager.display_all()
