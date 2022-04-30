import pkg.config as conf
from .Generation import *

import tkinter as tk
from tkinter import ttk
from typing import Union, Tuple, Dict, List




class Window(tk.Tk):
    """
    A class providing a GUI and an access to the user's inputs to other classes.
    It also runs the main loop of the program.
    """



    def __init__(self, winsize : Tuple[int, int], theme_color = conf.APP_THEME_COLOR):
        super().__init__()
        self.title(conf.APP_TITLE)
        self.size = winsize
        self.iconbitmap("./assets/plan_ville.ico")
        self.theme_color = theme_color
        self.minsize(winsize[0], winsize[1])
        self.config(bg=self.theme_color)

        self.__setup()



    def __setup(self):
        # Apply the default styles
        style = ttk.Style(self)
        style.configure("TEntry", background=self.theme_color, foreground="#000", focuscolor="yellow")
        style.configure("TLabel", background=self.theme_color, foreground="#FFF", font=("Times", 10))
        style.configure("TFrame", background=self.theme_color)
        style.configure("TNoteBook", background=self.theme_color, )
        style.configure("TButton", background="#353535", relief="raised")
        style.map("TButton", background = [("active", "green")] )

        # Build the container frame
        container = ttk.Frame(self, name="container")
        self.__note_book = ttk.Notebook(container, name="note_book", padding=0)
        self.__note_book.pack(side="top", fill="both", expand=True)
        self.__note_book.pack_propagate(False)
        container.pack(fill="both", expand=True)

        # Build the first frame
        self.__build_first_frame(self.__note_book)



    def __build_first_frame(self, master):
        # Build the first frame
        first_frame = ttk.Frame(master, name="first_frame")
        first_frame.pack(fill="both", expand=True)
        self.__note_book.add(first_frame, text="Parameters")

        # Build the title frame
        title_frame = ttk.Frame(first_frame, name="app_title")
        title_frame.pack(fill="both", side="top", pady=25)
        ttk.Label(title_frame, name="h1", text="City map generator", font=("Abadi", 25)).pack(side="top", pady=5)
        ttk.Label(title_frame, name="h2", text="Please choose your settings", font=("Abadi", 13)).pack(side="top", pady=5)

        # Build the paramerters frame
        # 1 : entries
        parameters_frame = ttk.Frame(first_frame, name="parameters")
        self.__build_entries(parameters_frame)
        parameters_frame.pack(fill="both", expand=True)
        # 2 : submit button (starts a generation)
        ttk.Button(parameters_frame, name="generate_button", text="Generate", command=self.__try_generate).place(width=70, relx=0.465, rely=0.75)



    def __build_entries(self, master : ttk.Frame):
        """Creates the entries (parameters), places them, sets the callbacks."""

        # Register the valid value callback, "%W" to pass the widget implied in error as an argument
        validcommand = ( self.register(self.__valid_value_callback), "%W" )

        # Register the error callback, "%W" to pass the widget implied in error as an argument
        invalidcommand = ( self.register(self.__invalid_value_callback), "%W" )

        # Register the needed validity-test callback(s) (validation callbacks), if it returns False, the error callback is called
        is_nonzero_real = ( self.register(self.__is_positive_real), "%P", "%W" )
        match_value = ( self.register(self.__match_value), "%P", "%W" )


        # Creation of inputs widgets, each have their own frame
        # SCHEMA : {
        #               "<title>" : [ <widget : ttk.Widget>, <error_string : str = ""> ],
        #               //                          
        #          }
        self.ttk_inputs : Dict[ str, List[Union[ttk.Widget, str]] ] = {

            "title" : [ttk.Entry(ttk.Frame(master), validate="focus", validatecommand=validcommand), ""],
            "inhabitant per km²" : [ ttk.Entry(ttk.Frame(master), validate="focus", validatecommand=is_nonzero_real, invalidcommand=invalidcommand), "Value must be a strictly positive real number"],
            "width" : [ttk.Entry(ttk.Frame(master), validate="focus",validatecommand=is_nonzero_real, invalidcommand=invalidcommand ), "Not a valid width"],
            "height" : [ttk.Entry(ttk.Frame(master), validate="focus",validatecommand=is_nonzero_real, invalidcommand=invalidcommand ), "Not a valid height"],
            "biome" : [ttk.Combobox(ttk.Frame(master), values=["desert"], validate="focus", validatecommand=match_value, invalidcommand=invalidcommand), "Choose a biome"]
        }

        # Operations for each input : creation of an individual frame, placement, creation of 2 labels (title and eventual error)
        column = 0
        row = 0

        for key, ttk_input in self.ttk_inputs.items() :
            w : ttk.Widget = ttk_input[0]
            err : str = ttk_input[1]

            # x size of the cell
            master.columnconfigure(column, minsize = self.size[0]//4, weight=1)

            # y size of the cell
            master.rowconfigure(row, minsize = (self.size[1] - 100) // (len(self.ttk_inputs)//3 + 2), pad=10)

            # placement of the frame in the grid
            w.master.grid(column=column, row=row)

            # Set a default validity state : "invalid"
            w.state(["invalid"])

            # Creation of 2 labels for the frame : 
            # - the title
            # - the eventual error string (text placed by the error callback and removed by the validation callback if it returns True)
            ttk.Label(w.master, text=key, name="title").pack(side="top")
            ttk.Label(w.master, text=err, name="error_string", foreground=self.theme_color).pack(side="bottom")

            # Display the widget
            w.pack()
            
            column += 1
            if column > 3:
                column = 0
                row += 1



    def __are_inputs_valid(self) -> bool :
        """ The function returns True if all the inputs are valid, False if not."""

        is_valid = True

        for key in self.ttk_inputs :
            state : tuple = self.ttk_inputs[key][0].state()
            if len(state) != 0 :
                if state[0] == "invalid" :
                    is_valid = False
                    break

        return is_valid



    def get_inputs(self) -> Union[dict, bool] :
        """If the inputs are valid, the function returns a dict of parameters and their associated value.
           If not, it returns False."""

        result = False

        if self.__are_inputs_valid() :
            result = {}

            for key in self.ttk_inputs:
                result[key] = self.ttk_inputs[key][0].get()

        return result



    def __set_inputs_access(self, are_available : bool):
        """Sets the access state of the ttk inputs AND the buttons (usefull when a generation starts for example)
           True : availables, False : disabled."""

        state = "!readonly" if are_available else "readonly"
        buttons_state = "!disabled" if are_available else "disabled"

        # Update the generate button state
        self.nametowidget(".container.note_book.first_frame.parameters.generate_button").state([buttons_state]) 
        # Update the state of each input
        for key in self.ttk_inputs :
            self.ttk_inputs[key][0].state([state])



    # BUTTONS AND INPUTS CALLBACKS



    def __invalid_value_callback(self, widget_name) -> None :
        """This callback is called when the validation callback of an input has returned False."""

        # Make the error string visible (in red)
        self.nametowidget(widget_name).master.children["error_string"].configure(foreground="#F00")

        # Set the parameter's title color white
        self.nametowidget(widget_name).master.children["title"].configure(foreground="#FFF")



    def __valid_value_callback(self, widget_name) -> None :
        """This callback is called before the validation callback of an input returns True, or directly as a validation callback if the widget doesn't need any verification."""

        err_label = self.nametowidget(widget_name).master.children["error_string"]
        title_label = self.nametowidget(widget_name).master.children["title"]

        # Make the error string invisble (foreground color same as background color)
        err_label.configure(foreground = self.theme_color)

        # Set the parameter's title green
        title_label.configure(foreground="#0F0")



    def __is_positive_real(self, input : str, widget_name : str) -> bool :
        """An input validation callback. Test if the given value is a strictly positive real."""

        result = False
        try:
            value = float(input)
            if value > 0 :
                result = True
                self.__valid_value_callback(widget_name)

            return result

        except:
            return result
    


    def __match_value(self, input : str, widget_name) -> bool :
        """An input validation callback. Must be used only to check widgets having a 'values' instance attribute."""
        w : ttk.Combobox = self.nametowidget(widget_name)
        test = False
        if  input in w["values"] :
            self.__valid_value_callback(widget_name)
            test = True
        return test



    def __try_generate(self) -> bool :
        """Tries to start a generation in a new notebook tab with the given parameters. Returns True if it succeeds, False if not.
           The function is blocking until the generation has finished."""

        params = self.get_inputs()
        print(params)

        # If the inputs are valid and if there are less than 5 five generations
        if params and Generation.instances_total_number < 6 :
            
            # Disable the inputs
            self.__set_inputs_access(False)

            # Create a generation
            generation = Generation(self.__note_book, params)

            # New notebook tab
            self.__note_book.add(generation.frame, text=params["title"])
            
            
            # Start the generation : blocking
            generation.start()

            # Reactivate the inputs
            self.__set_inputs_access(True)

            return True

        else :
            print("Error : bad parameters or too many generations in memory.")
            return False



