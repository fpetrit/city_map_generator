from ..config.config import *
from ..drawer.Drawer import Drawer

import tkinter as tk
from tkinter import ttk, filedialog as fd
from typing import Dict




class Generation :
    """A class that creates and handles a tkinter frame dedicated to a single town generation (drawing).
       Its start() method starts the drawing (thanks to an instance of Drawer()) and is blocking until the end of the generation. 
       It provides features related to a generation : save as, delete, save the parameters as a json or txt file."""



    # We count the instantiations to limit their number.
    instances_total_number = 0



    def __init__(self, master, parameters : Dict[str, str]) -> None :
        Generation.instances_total_number += 1
        self.parameters = parameters
        self.__frame = self.__layout(master)
        self.drawer = Drawer(self.canvas, self.parameters)


    def start(self) -> None :
        """Starts the generation : blocking until the end."""
        # Start the drawer
        self.drawer.start()
        # Activate the buttons after the generation is done.
        self.get_frame().nametowidget("buttons_frame.delete_button").state(["!disabled"])
        self.get_frame().nametowidget("buttons_frame.save_button").state(["!disabled"])



    def get_frame(self) -> ttk.Frame :
        """Returns the main frame."""
        return self.__frame



    def __layout(self, master : tk.Widget) -> ttk.Frame :
        """Constructs the tkinter widgets.
           Returns the main container frame."""

        # Images stored as attributes because they must not be out of scope.
        self.cross = tk.PhotoImage(file= r"././assets/cross.png")
        self.download = tk.PhotoImage(file= r"././assets/download.png")
        
        # Creation of the main frame
        main_frame = ttk.Frame(master)

        # Creation of a title frame for the generation
        title_frame = ttk.Frame(main_frame, name="title_frame")
        title_frame.pack(side="top", pady=20, fill="x")
        ttk.Label(title_frame, text=self.parameters["title"], name="title", font=("Abadi", 16)).pack(anchor="center")

        # Creation of a canvas frame and his scrollable tkinter canvas, the "turtle" module will use it to draw
        canvas_frame = ttk.Frame(main_frame, padding="20 5")
        canvas_frame.pack(fill="both", expand=True)
        canvas_frame.pack_propagate(False)
        self.canvas = tk.Canvas(canvas_frame, name="canvas", height=int(self.parameters["height"]), width=int(self.parameters["width"]), highlightbackground="red", highlightthickness=3)
        self.canvas.pack(anchor="center")
        self.canvas.configure(scrollregion=canvas_frame.bbox("all"))
        # The user can scroll the canvas with the mouse wheel (binding the MouseWheel event)
        self.canvas.bind("<MouseWheel>", lambda event : self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        # Creations of buttons : delete generation, save as
        buttons_frame = ttk.Frame(main_frame, name="buttons_frame")
        buttons = [ ttk.Button(buttons_frame, image=self.cross, name="delete_button", command=self.__delete_generation, state="disabled"),
                    ttk.Button(buttons_frame, image=self.download, name="save_button", command=self.__save_as, state="disabled") ]
        col = 0
        buttons_frame.grid_anchor("center")
        # Configuration with a loop
        for button in buttons :
            button.grid(row=0, column=col, padx=10)
            col += 1
    
        buttons_frame.pack(side="bottom", fill="x", pady=15)

        # Display the main frame
        main_frame.pack(fill="both", expand=True)

        return main_frame



    # BUTTONS CALLBACKS



    def __delete_generation(self) -> None :
        """Deletes the generation."""
        self.get_frame().destroy()



    def __save_as(self) :
        """Opens a file dialog and save the genertion."""
        types = [("postscript file", ".ps"), ("All file", "*")]
        file = fd.asksaveasfilename(title = APP_TITLE + " - " "Save your generation as...", initialfile = self.parameters["title"], defaultextension = "ps", filetypes = types)
        self.canvas.postscript(file=file, colormode="color")
    
        

    # Save parameters ?



    # Bit-mapped images conversion ?