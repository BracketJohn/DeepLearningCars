"""Module which provides some nice functionalities that are used by more than one Module."""
from typing import Any, Callable, List, Tuple

from deepcars.pygvisualization import Coordinate, WINDOW_SIZE, ASCII_DICT

import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT


def is_pressed(event: pygame.event, keys: List[str]) -> bool:
    """Take list of keys and checks if one of them is pressed or if certain event happened, i.e. QUIT."""
    if any(k == 'quit' for k in keys):
        if event.type == QUIT:
            return True
        keys.remove('quit')

    if any(k == 'lmouse_down' for k in keys):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return True
        keys.remove('lmouse_down')

    if any(k == 'rmouse_down' for k in keys):
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            return True
        keys.remove('rmouse_down')

    if any(k == 'mouse_move' for k in keys):
        if event.type == MOUSEMOTION:
            return True
        keys.remove('mouse_move')

    if any(k == 'lmouse_up' for k in keys):
        if event.type == MOUSEBUTTONUP and event.button == 1:
            return True
        keys.remove('lmouse_up')

    if any(k == 'rmouse_up' for k in keys):
        if event.type == MOUSEBUTTONUP and event.button == 3:
            return True
        keys.remove('rmouse_up')

    return any(event.type == KEYDOWN and event.key == ASCII_DICT.get(k, None)
               for k in keys)


def to_pygame(coord: Coordinate) -> Tuple[int]:
    """Small hack to convert pymunk to pygame coordinates."""
    return int(coord.x), int(-coord.y+WINDOW_SIZE)


def caption_manager(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Remember Caption of Caller and reset after Subroutine is finished. Allows infinite Call Stack while maintaining Captions of Caller."""
    def caption_resetter(*args, **kwargs):
        caller_caption = kwargs.pop('caller_caption')

        func(*args, **kwargs)

        pygame.display.set_caption(caller_caption)

    return caption_resetter


# ToDo: Remove redundancy/Move Menu option part here as well, instead of just the text.
def simple_text_menu(screen: pygame.display.set_mode, options: str) -> None:
    """Create Basic Text Menu from list of Options."""
    simple_text(screen, options, is_option=True)


# Refine!!
def simple_text(screen: pygame.display.set_mode, text_lines: List[str], is_option: bool=False, pos: Coordinate=None):
    font_size = 32 if is_option else 18
    spacing = 25 if is_option else 15
    font = pygame.font.Font(None, font_size)

    color = (10, 10, 10)

    for mult, line in enumerate(text_lines):
        if is_option:
            text = font.render(f'({line[0]}) {line}', 1, color)
        else:
            text = font.render(f'{line}', 1, color)

        if pos:
            textpos = text.get_rect()
            textpos.x, textpos.y = pos.x, pos.y+spacing*mult
        else:
            textpos = text.get_rect()
            textpos.center = screen.get_rect().centerx, 40+spacing*mult

        screen.blit(text, textpos)

