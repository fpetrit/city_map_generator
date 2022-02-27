from typing import Tuple
from tkinter import Canvas
import random as ra, turtle as tu
from queue import Queue
from threading import Thread

from pkg.drawing.drawable.House import House

class Drawer:
    """
    Draw a randomly generated 2D town plan when start() is called (blocking function), on the given tkinter canvas and parameters passed when instantiating.
    "turtle" module is used to draw. Working principle : a queue.Queue is fill with drawnig instructions in a thread, dequeued and executed at the same time in
    the main thread (turtle and tkinter calls must be in the main thread).
    """

    def __init__(self, canvas : Canvas, parameters : dict) -> None :
        canvas = canvas
        self.parameters = parameters
        self.__ts = tu.TurtleScreen(canvas)
        self.__turtle = tu.RawTurtle(self.__ts)
        self.__turtle.speed(0)



    @staticmethod
    def get_random_tuple(x_min, x_max, y_min, y_max) -> Tuple[int, int] :
        """Returns random coordinates respecting the specified limits."""
        return tuple ( (ra.randint(x_min, x_max), ra.randint(y_min, y_max)) )



    def start(self):
        """Starts generating and drawing the map on the canvas. Blocking function."""

        # Create an infinite instructions queue
        self.__drawing_instructions = Queue(0)

        # Start the scheduling in a separate thread.
        schedule_thread = Thread(target = self.schedule)
        schedule_thread.start()
        # Start executing the instructions.
        self.draw()

        # Wait for the thread to end
        schedule_thread.join()



    def schedule(self) -> None :
        """Starts creating and queueing instructions. Must be called in a thread."""

        queue = self.__drawing_instructions

        # The lines below are just FOR TESTING

        for _ in range(20) :
            queue.put("house")

        queue.put(False)



    def draw(self) -> None :
        """Starts executing the drawing instructions in the queue. Blocks until it has dequeued an ending flag."""

        queue = self.__drawing_instructions
        tu = self.__turtle
        params = self.parameters
        instruction = -1
        coordinates_system = [0, int(params["width"]), 0, int(params["height"])]

        self.__ts.setworldcoordinates(0, 0, int(params["width"]), int(params["height"]))

        while instruction != False :
            # Get an instruction and do some work on the canvas.

            instruction = queue.get()

            # Switch with if, elif, ..., else

            # Determine a width, a heigth
            if instruction == "house" :

                
                place = [(self.get_random_tuple(*coordinates_system), self.get_random_tuple(*coordinates_system))]
                House(places = place).draw(tu)

