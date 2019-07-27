import pygame

from pygame import Rect
from pygame.sprite import Group
from game.battle.GUI.graphics.pygame.component import WidgetSprite, SpriteSelector, TextWidget

from game.battle.GUI.graphics.pygame.core import load_image
from game.prefabs.fantasy_game.characters import Character, BaseAction

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

    def __init__(self, character: Character, widget: SpriteSelector):
        WidgetSprite.__init__(self, widget)
        self.index = None
        self.image = None

        self._icons = {
            'Knight': 'knight',
            'Wizard': 'wizard',
            'Daemon': 'sauron',
            'EvilNun': 'mt',
            'grave': 'grave',
        }

        self.image, self.rect = load_image(self._icons[type(character).__name__] + '.png')

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.character = character

    def set_index(self, index: int):
        self.index = index
        self._mediator_extraparam = str(index)

    def update(self):
        if self.character.pf() <= 0:
            self._active = False
        super().update()

    def get_display_text(self) -> str:
        return self.character.name


class PlayerActionsMenu(SpriteSelector):

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

    #def get_se



class HPBar:
    def __init__(self, chr_spr: ChrSprite):
        self._chr_spr = chr_spr

    def draw(self):
        middle = self._chr_spr.character.pf() / float(self._chr_spr.character.pf_max()) * self._chr_spr.rect.width
        print(middle)


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
        widget.set_text(ability_sprite.character.name + "\n" + ' HP ' + str(ability_sprite.character.pf()) + '/' + str(ability_sprite.character.pf_max()))
        widget.draw()



