from typing import Tuple
from tkinter import Canvas
import random as ra, turtle as tu

from pkg.config.config import *




class Drawer:
    """
    Draw a randomly generated 2D town plan when start() is called (blocking function), on the given tkinter canvas and parameters passed when instantiating.
    "turtle" module is used to draw. Working principle : 
    """

    def __init__(self, canvas : Canvas, parameters : dict) -> None :
        self.parameters = parameters
        self._ts = tu.TurtleScreen(canvas)
        # Unleash the turtle's speed : set the 'actions per refresh' number, and the delay
        self._ts.tracer(ACTIONS_PER_SCREEN_REFRESH, DELAY)
        self._turtle = tu.RawTurtle(self._ts)
        self._turtle.speed(0)



    @staticmethod
    def get_random_tuple(x_min, x_max, y_min, y_max) -> Tuple[int, int] :
        """Returns random coordinates respecting the specified limits."""
        return tuple ( (ra.randint(x_min, x_max), ra.randint(y_min, y_max)) )



    def start(self):
        """Starts generating and drawing the map on the canvas. Blocking function."""

        pass

