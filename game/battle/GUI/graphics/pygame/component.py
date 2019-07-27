import pygame

from pygame import Rect
from pygame.sprite import Group
from game.battle.GUI.mediator import AbstractSelectorComponent, AbstractTextComponent


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

