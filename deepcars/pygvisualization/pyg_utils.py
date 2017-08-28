"""Module which provides some nice pygame functionalities that make development easier."""
from typing import Any, Callable, List, Tuple

import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT

from pygvisualization import Coordinate, WINDOW_SIZE, ASCII_DICT


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


# Refine!!
def simple_text(screen: pygame.display.set_mode, msgs: str, pos: str):
    """Simple Text Display Method which takes a line of text and a position and then either:
    * Prints String as option, displaying the first Letter of that String as the Hotkey to choose said Option
    * Prints text as info, no Hotkey Displayed

    It chooses to do the first one if position is `middle` and the second one if position is either `topleft`, `topright`.
    This is far from perfect but an alright way of quickly displaying text.
    """
    color = (10, 10, 10)
    font_size = 32 if pos == 'middle' else 18
    spacing = 25 if pos == 'middle' else 15

    font = pygame.font.Font(None, font_size)

    for multiplier, msg in enumerate(msgs):
        if pos == 'middle':
            text = font.render(f'({msg[0]}) {msg}', 1, color)
        else:
            text = font.render(f'{msg}', 1, color)

        textpos = text.get_rect()
        textpos.top = 20+spacing*multiplier

        if pos == 'middle':
            textpos.x = screen.get_rect().centerx-textpos.size[0]//2

        if pos == 'topleft':
            textpos.x = 10

        if pos == 'topright':
            textpos.right = WINDOW_SIZE-10


        screen.blit(text, textpos)
