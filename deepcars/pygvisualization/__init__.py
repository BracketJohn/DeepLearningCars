"""Init Module for Car Sim Package."""
from typing import Dict, List, NamedTuple, Optional, Union


ASCII_DICT = {chr(key_code): key_code for key_code in range(128)}
CAR_SIZE = 15, 25
COLLISION_TYPES = {'wall': 0, 'car': 1, 'start': 2}
WINDOW_SIZE = 750
MAP_DIR = 'maps'


class Coordinate(NamedTuple):
    """Ordinary x, y Coordinate."""

    x: int
    y: int


class SegmentPart(NamedTuple):
    """Segment consists out of a Start and an End Coordinate."""

    start: Coordinate
    end: Coordinate


Segment: List[SegmentPart] = list
SimMap: Dict[str, Union[SegmentPart, List[Optional[Segment]]]] = dict

from pygvisualization.level_creator import create_new_map
from pygvisualization.pyg_utils import is_pressed, simple_text
from pygvisualization.simspace_creator import create_sim, sim_loop
from pygvisualization.simulation import select_map
