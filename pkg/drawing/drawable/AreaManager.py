from typing import List, Tuple

from .Drawable import Drawable

# drawables positions are represented by rectangles, described by two points : top left corner (x, y), bottom right corner (x, y)
t_coordinates = Tuple[Tuple[int, int], Tuple[int,int]]


class AreaManager():
    """All the area division and random placements jobs are done by this helper class.
        For example a drawable may need random children drawables placements, more or less circular, or on a line."""


    def __init__(self, space_boundaries : t_coordinates):
        self.children : List[Drawable] = []
        self.space_boundaries = space_boundaries



    def register(self, children : List[Drawable]):
        for child in children:
            if not child in self.children:
                self.children.append(child)



    def assign_random_coordinates() -> List[t_coordinates]:
        pass
