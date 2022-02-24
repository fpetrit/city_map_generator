from tkinter import Canvas
import random as ra, turtle as tu

class Drawer:
    """
    Draw a randomly generated 2D town plan when start() is called (blocking function), on the given tkinter canvas and with the given parameters.
    "turtle" module is used to draw. Working principle : 
    """

    def __init__(self, canvas : Canvas, parameters : dict) -> None:
        canvas = canvas
        self.parameters = parameters
        self.ts = tu.TurtleScreen(canvas)
        self.turtle = tu.RawTurtle(self.ts)

        """ 
        'permission' helps to delete the generation properly especially when it has not finished its work. 
        permission must be evaluated regularly, to stop working on the canvas, set 'is_working' to False,
        and allow the destruction of the canvas if it is evaluated to False."""
        self.permission = True
        self.is_working = True

        self.operations_list = []



    @staticmethod
    def get_random_tuple(x_min, x_max, y_min, y_max):
        return tuple ( (ra.randint(x_min, x_max), ra.randint(y_min, y_max)) )

    def start(self):
        width = int(self.parameters["width"])
        height = int(self.parameters["height"])

        turt = self.turtle
        self.ts.setworldcoordinates(0, 0, width, height)
        turt.screen.bgcolor("#DDDDDD")
        for i in range(3):
            turt.up()
            turt.setposition(Drawer.get_random_tuple(0, width, 0, height))
            turt.down()
            turt.setheading(0)
            for o in range(4):
                turt.forward(50)
                turt.right(90)