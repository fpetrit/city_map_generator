import turtle as tu


class House:
    """A drawable house."""

    average_area = 91 # unit : m²

    def __init__(self, places) -> None :
        # A list of the x and y coordinates of the lower left corner, and the upper right corner, of the places (squares) taken by a drawable.
        # These places will not be overlapped by other drawables.
        self.places = places

    def draw(self, t : tu.RawTurtle) -> None :
        for place in self.places :
            # lower left corner, upper right corner, x and y coordinates
            ll, ur = place[0], place[1]
            width, height = ur[0] - ll[0], ur[1] - ll[1]
            t.up()
            t.goto(ur)
            t.setheading(270)
            t.down()
            for i in range(4):
                if i % 2 == 0 :
                    t.forward(height)
                else :
                    t.forward(width)
                t.right(90)

                

