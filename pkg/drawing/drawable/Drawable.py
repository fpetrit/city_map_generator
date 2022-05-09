"""
This file contains a drawable abstract class. It describes how the drawable objects, components of the map drawing, should work.
It contains several drawables classes. Each of them can draw several others drawables.

Randomized placement :
Each drawable has a position represented by a rectangle that delimits it. To avoid overlaps, the area available for an object
to draw in is divided in rectangles of equal sizes. Each rectangle has an index that can be choose randomly, and coordinates.
All the area division and random placements jobs are done by a helper class "Area".
For example a drawable may need random child placements, more or less circular, or on a line.
"""

from abc import ABC, abstractmethod
from turtle import RawTurtle
from typing import Tuple


# drawables positions are represented by rectangles, described by two points : top left corner (x, y), bottom right corner (x, y)
coordinates = Tuple(Tuple(int, int), Tuple(int,int))



class Drawable(ABC):

    @classmethod
    @property
    @abstractmethod
    def default_paramaters(cls) -> dict:
        raise NotImplementedError



    @property.setter
    def parameters(self, new_parameters):
        """The parameters setter keeps the default ones from the class, only updating the parameters
            specified in the new parameters dict."""

        if hasattr(self, __parameters):
            __parameters = self.default_paramaters
            print("default set")

        for new_param, new_value in new_parameters.items():
            __parameters[new_param] = new_value



    def __init__(self, parameters : dict, position : coordinates):
        # Update the parameters with parent's ones
        self.parameters, self.position = parameters, position

        # Randomize the final new parameters
        self.randomize()



    @abstractmethod
    def randomize(self):
        """Here random values should be assigned to new parameters according to what is already in self.parameters of 
            the child instance. For example by following laws of probabilitiy own to the child class."""
        pass



    @abstractmethod
    def draw(turtle : RawTurtle):
        """Should draw the object with the turtle module."""
        pass