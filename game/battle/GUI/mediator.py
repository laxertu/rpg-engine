from game.prefabs.fantasy_game.GUI.wrapper import BattleWrapper



class AbstractNotifier:
    pass


class WindowManager:
    def init_scene(self):
        raise NotImplementedError('Abstract Method')

    def erase_screen(self):
        raise NotImplementedError('Abstract Method')

    def display_all(self):
        raise NotImplementedError('Abstract Method')

    def set_gui_interaction_enabled(self, enabled: bool = True):
        raise NotImplementedError('Abstract Method')

class DefaultMediator:

    def notify_mouseover(self, sender: AbstractNotifier) -> None:
        pass
    def notify_mouseout(self, sender: AbstractNotifier) -> None:
        pass
    def notify_click(self, sender: AbstractNotifier, param: None) -> None:
        pass



class GuiComponent(AbstractNotifier):

    mediator = DefaultMediator()
    interaction_enabled = True


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

class TextComponent(GuiComponent):

    def set_text(self, txt: str):
        raise NotImplementedError('Abstract Method')


class SpriteContainerComponent(GuiComponent):

    def get_display_text(self) -> str:
        """
        TODO: move to more specific class
        :return:
        """
        pass

    def draw(self):
        pass

    def reset_selection(self):
        pass

class ActionsMenuComponent(SpriteContainerComponent):
    def set_actions(self, actions: dict):
        raise NotImplementedError('Abstract Method')

class AbstractMediator(DefaultMediator):
    """
    TODO: rename with concrete class
    """

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
        self.init_scene_components()
        self.redraw_all()

    def init_scene_components(self):
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

GuiComponent.mediator = DefaultMediator()