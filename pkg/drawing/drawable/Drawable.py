"""
This file contains a drawable abstract class. It describes how the drawable objects, components of the map drawing, should work.
It contains several drawables classes. Each of them can draw several others drawables.

Randomized placement :
Each drawable has a position represented by a rectangle that delimits it. To avoid overlaps, the area available for an object
to draw in is divided in rectangles of equal sizes. Each rectangle has an index that can be choose randomly, and coordinates.
All the area division and random placements jobs are done by a helper class "Area".
"""

from abc import ABC, abstractmethod
from turtle import RawTurtle
from typing import Tuple

from .AreaManager import AreaManager


# drawables positions are represented by rectangles, described by two points : top left corner (x, y), bottom right corner (x, y)
t_coordinates = Tuple[Tuple[int, int], Tuple[int,int]]



class Drawable(ABC):

    @classmethod
    @property
    @abstractmethod
    def default_paramaters(cls) -> dict:
        raise NotImplementedError



    def __init__(self, parameters : dict):
        # Update the parameters with the most precise ones
        self.parameters = self.parameters_autocomplete(parameters)



    def parameters_autocomplete(parameters) -> dict:
        return parameters



    @abstractmethod
    def draw(self, turtle : RawTurtle):
        """Should draw the object with the turtle module. super() must be called."""
        
        try:
            if not "position" in self.parameters.keys():
                raise Exception("Drawable cannot be drawn because it has no 'position' parameter.")
        except Exception as e:
            print(e)
            return False
        
        self.position = self.parameters["position"]
        self.space_manager = AreaManager()
        