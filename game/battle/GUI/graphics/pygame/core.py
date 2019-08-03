import pygame
from pygame.locals import *

__LOADED_IMAGES = {}

IMG_BASE_PATH = ''

def load_image(name, colorkey=None):
    """
    :todo: remove path
    :param name:
    :param colorkey:
    :return:
    """
    fullname = IMG_BASE_PATH + name

    if fullname not in __LOADED_IMAGES.keys():
        try:
            image = pygame.image.load(fullname).convert_alpha()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            __LOADED_IMAGES[fullname] = image
        except pygame.error as e:
            print(e)
            return None
    else:
        image = __LOADED_IMAGES[fullname]

    return image, image.get_rect()


def show_rect(surface, rect, color_to_use='#000000'):
    pygame.draw.rect(surface, pygame.Color(color_to_use), rect, 1)
