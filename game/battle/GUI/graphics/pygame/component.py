import pygame

from pygame import Rect
from pygame.sprite import Group

from game.battle.GUI.graphics.pygame.core import load_image
from game.battle.GUI.mediator import AbstractSelectorComponent, AbstractTextComponent, ActionsMenuComponent

from game.battle.battle import AbstractCharacter, BaseAction


class AbstractWidgetSprite(pygame.sprite.Sprite):
    """
    a pygame Sprite with mouse interaction funcionality
    """
    user_clicked = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mouse_over = False
        self.rect = pygame.Rect(0,0,0,0)

    def get_display_text(self) -> str:
        raise NotImplementedError('Abstract method')


class SpriteSelector(AbstractSelectorComponent):

    _SPRITE_NONE = AbstractWidgetSprite()

    def __init__(self) -> None:
        super().__init__()

        self._sprites = Group()
        self._selected_sprite = AbstractWidgetSprite()
        self._mouseover_sprite = AbstractWidgetSprite()
        self._display_text = ''


    def get_display_text(self) -> str:
        return self._display_text

    def set_display_text(self, txt: str):
        self._display_text = txt

    def get_rect(self) -> Rect:
        raise NotImplementedError('abstract method')

    def reset_selection(self):
        self._selected_sprite = SpriteSelector._SPRITE_NONE

    def set_selected_sprite(self, sprite: AbstractWidgetSprite):
        self._selected_sprite = sprite

    def set_mouseover_sprite(self, sprite: AbstractWidgetSprite = None):
        self._mouseover_sprite = sprite
        self._display_text = sprite.get_display_text()

    def reset_onmouseover_sprite(self):
        self._mouseover_sprite = SpriteSelector._SPRITE_NONE

    def get_mouseover_sprite(self) -> AbstractWidgetSprite:
        return self._mouseover_sprite

    def update(self):
        self._sprites.update()


class WidgetSprite(AbstractWidgetSprite):

    def __init__(self, widget: SpriteSelector):
        super().__init__()
        self._widget = widget
        self._mediator_extraparam = None
        self._active = True

    def update(self):
        if not self._active:
            return

        was_mouse_over = self.mouse_over

        hitbox = self.rect
        x, y = pygame.mouse.get_pos()
        self.mouse_over = hitbox.collidepoint(x, y)

        if AbstractWidgetSprite.user_clicked and self.mouse_over:
            self._widget.set_mouseover_sprite(self)
            self._widget.mediator.notify_mouseover(self._widget, self._mediator_extraparam)

            self._widget.set_selected_sprite(self)
            self._widget.mediator.notify_click(self._widget, self._mediator_extraparam)

        if was_mouse_over and not self.mouse_over:
            self._widget.reset_onmouseover_sprite()
            self._widget.mediator.notify_mouseout(self._widget)

        if not was_mouse_over and self.mouse_over:
            self._widget.set_mouseover_sprite(self)
            self._widget.mediator.notify_mouseover(self._widget, self._mediator_extraparam)

    def get_display_text(self):
        return ''


class ActionButtonSprite(WidgetSprite):

    def __init__(self, action, action_index, widget: SpriteSelector):
        WidgetSprite.__init__(self, widget)
        self._action = action
        self._mediator_extraparam = action_index

        self.image, self.rect = load_image(type(action).__name__ + '.png')
        self.index = action_index

    def get_action(self) -> BaseAction:
        return self._action

    def get_display_text(self) -> str:
        return self.get_action().to_str()


class ChrSprite(WidgetSprite):

    icons = dict()

    def __init__(self, character: AbstractCharacter, widget: SpriteSelector):
        WidgetSprite.__init__(self, widget)
        self.index = None
        self.image = None
        self.image, self.rect = load_image(ChrSprite.icons[type(character).__name__] + '.png')

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.character = character

    def set_index(self, index: int):
        self.index = index
        self._mediator_extraparam = str(index)

    def update(self):
        if not self.character.active():
            self._active = False
        super().update()

    def get_display_text(self) -> str:
        return self.character.to_str()


class TeamWidget(SpriteSelector):

    def __init__(self, surface: pygame.Surface, division_middle:int = None, distance_from_middle = 0, sprites_spacing: int = 0, bottom = 0, left_side = True):

        super().__init__()

        self._distance_from_middle = distance_from_middle
        self._sprites_spacing = sprites_spacing
        self._left_side = left_side
        self._bottom = bottom
        self._division_middle = surface.get_rect().centerx if division_middle is None else division_middle
        self._surface = surface

        self._raw_chrs= list()

    def set_characters(self, characters: list):
        i = 0

        sprites = self._build_sprites(characters)

        self._sprites = Group()
        for sprite in sprites:
            if not self._left_side:
                sprite.image = pygame.transform.flip(sprite.image, 1, 0)
            sprite.set_index(i)
            self._sprites.add(sprite)
            i += 1

    def _build_sprites(self, characters: list):
        i = 0
        center_x = self._division_middle

        base_right = center_x - self._distance_from_middle
        base_left = center_x + self._distance_from_middle

        sprites = []
        for character in characters:
            sprite = ChrSprite(character, self)
            if self._left_side:
                sprite.rect.right = base_right - ((sprite.rect.width + self._sprites_spacing) * i)
            else:
                sprite.rect.left = base_left + ((sprite.rect.width + self._sprites_spacing) * i)

            sprite.rect.bottom = self._bottom
            i += 1

            sprites.append(sprite)
        return sprites

    def get_rect(self) -> Rect:
        sprites = self._sprites.sprites()

        sprite_template_index = len(sprites) - 1

        return Rect(
            sprites[sprite_template_index].rect.left,
            sprites[sprite_template_index].rect.top,
            (sprites[sprite_template_index].rect.width * len(sprites)) + (self._sprites_spacing * (len(sprites) - 1)),
            sprites[sprite_template_index].rect.height,
        )

    def draw(self):
        surface = self._surface

        dead_image, dead_rect = load_image('grave.png')
        for s in self._sprites.sprites():
            if s.character.pf() <= 0:
                s.image = dead_image

        self._sprites.draw(surface)

        # Rectangle over sprite under mouse
        for ability_sprite in self._sprites.sprites():
            self._draw_resume(ability_sprite)

            if ability_sprite.mouse_over:
                pygame.draw.rect(surface,pygame.Color('#00FF00'), ability_sprite.rect, 1)
                pygame.display.update(ability_sprite.rect)

    def _draw_resume(self, ability_sprite: ChrSprite):

        rect = pygame.Rect(
            ability_sprite.rect.left,
            ability_sprite.rect.top + ability_sprite.rect.height + 5,
            ability_sprite.rect.width,
            50
        )

        widget = TextWidget(self._surface, rect, 15)
        widget.set_text(ability_sprite.get_display_text())
        widget.draw()

class PlayerActionsMenu(ActionsMenuComponent, SpriteSelector):

    def __init__(self, surface: pygame.Surface, top: int, left: int, sprite_spacing: int = 0):

        super().__init__()

        self._actions = {}
        self._top = top
        self._left = left
        self._sprites_spacing = sprite_spacing
        self._surface = surface

    def set_actions(self, actions: dict):
        self._actions = actions
        player_actions_box = Group()
        n = 0
        for action_key in self._actions.keys():
            ability_sprite = ActionButtonSprite(self._actions[action_key], action_key, self)
            ability_sprite.rect.top = self._top
            ability_sprite.rect.left = self._left + n * (ability_sprite.rect.width + self._sprites_spacing)
            player_actions_box.add(ability_sprite)
            n += 1

        self._sprites = player_actions_box

    def draw(self):
        surface = self._surface

        self._sprites.draw(surface)

        # Rectangle over sprite under mouse
        for ability_sprite in self._sprites.sprites():

            if ability_sprite.mouse_over:
                pygame.draw.rect(surface,pygame.Color('#00FF00'), ability_sprite.rect, 2)
                pygame.display.update(ability_sprite.rect)


            if ability_sprite is self._selected_sprite:
                inflate_factor = self._sprites_spacing / 2
                pygame.draw.rect(surface,pygame.Color('#FF0000'), ability_sprite.rect.inflate(inflate_factor, inflate_factor), 2)
                pygame.display.update(ability_sprite.rect)


    def get_rect(self) -> Rect:
        sprites = self._sprites.sprites()

        return Rect(
            sprites[0].rect.left,
            sprites[0].rect.top,
            (sprites[0].rect.width * len(sprites)) + (self._sprites_spacing * (len(sprites) - 1)),
            sprites[0].rect.height,
        )


class TextWidget(AbstractTextComponent):

    def __init__(self, surface: pygame.Surface, rect: Rect, size):

        super().__init__()

        self._size = size
        self._txt_chunks = []
        self._items_to_draw = []
        self._lines_rects = []
        self._rect = rect
        self._raw_text = ''
        self._surface = surface
        self._visible = True

    def set_visible(self, visible: bool) -> None:
        self._visible = visible

    def visible(self) -> bool:
        return self._visible

    def do_draw(self):
        self._items_to_draw = []
        surface = self._surface
        for txt in self._txt_chunks:
            pf_widget = pygame.font.SysFont('Comic Sans MS', self._size)
            item_to_draw = pf_widget.render(txt, True, (255, 0, 0))
            self._items_to_draw.append(item_to_draw)

        self._build_lines_rects()
        pygame.draw.rect(surface, pygame.Color('#FFFFFF'), self.get_rect(), 0)
        i = 0
        for item_to_draw in self._items_to_draw:
            surface.blit(item_to_draw, self._lines_rects[i])
            i += 1

    def set_text(self, txt: str):
        self._txt_chunks = txt.split("\n")
        self._raw_text = txt


    def _build_lines_rects(self):
        self._lines_rects = []
        i = 0
        for item_to_draw in self._items_to_draw:
            item_to_draw_rect = item_to_draw.get_rect()
            item_to_draw_rect.top = self._rect.top + (item_to_draw_rect.height * i)
            item_to_draw_rect.left = self._rect.left

            self._lines_rects.append(item_to_draw_rect)
            i += 1
        return self._lines_rects


    def get_rect(self):
        return self._rect

