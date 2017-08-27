"""Init Module for Car Sim Package."""
from typing import Dict, List, NamedTuple, Optional, Union


ASCII_DICT = {chr(key_code): key_code for key_code in range(128)}
WINDOW_SIZE = 600
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

from deepcars.pygvisualization.level_creator import create_new_map
from deepcars.pygvisualization.pyg_utils import is_pressed, simple_text
from deepcars.pygvisualization.simspace_creator import create_sim, sim_loop
from deepcars.pygvisualization.simulation import select_map
