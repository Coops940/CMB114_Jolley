#Imports tkinter to use to create and build GUI
from tkinter import *
from main import run_

#Sets up defualt values for variables 'mol_type' and 'bond_angle'
#Makes variables global so that they could be updated anywhere in script
global mol_type, bond_angle
mol_type = "H2O" 
bond_angle = 120 

def graph_final_energy_config(energy_label, final_energy, graphic_canvas, pic_file):
    """
    Configures all widegts, in output window, necasssary with results from Orca calucaltions
    """
    energy_label.config(text = f"Final Single Point Energy: {final_energy:>4.2f}") #Reconfigure final single-point enrgy label
    #Handling the image file of graphed results
    #Opens image in a format that Tkinter can handle
    img = PhotoImage(file = pic_file)
    #Updated canvas with results graph
    graphic_canvas.create_image(50,0, image = img, anchor= "nw")
    graphic_canvas.image=img
    
#|~~~BUTTON FUNCTIONS~~~|
def change_mol_type(new_mol, mol_label):
    """
    Changes the molecule stored in 'mol_type'. Updates label on the input window.
    """
    global mol_type
    print(f"Molecule type: {mol_type}", end= ".")
    mol_type = new_mol
    print(f" Updated to: {mol_type}.")
    mol_label.config(text = f"MOLECULE TYPE: {new_mol:>5s}")
    return mol_type

def collect_angle(entry_box, angle_label): 
    """
    Changes the bond angle stored in 'bond_angle'. Updates label on the input window.
    """
    global bond_angle
    #Retreieves anything typed within entry box and stores in variable
    angle = entry_box.get()
    #Try...Except...Used for error handling, dealing with nummerical vs strings.
    try:
        angle = float(angle) #Converts variable into a float (decimal) type.
        print(f"Bond angle:{bond_angle:.2f}", end = ".")
        bond_angle = angle
        print(f" Updated to: {bond_angle:.2f}.")
        angle_label.config(text = f"BOND ANGLE: {bond_angle:>5.2f}")
    except:
        #Prints an error message to shell
        print("Error: Number not entered")
    return bond_angle

class elements_: 
    """
    General class with all attributes and functions for any widget in tkinter
    """   
    def __init__(self, window, geo, colour, co_ords):
        #Asigning all variables passd into function as attributies of object
        self.height = geo[1]
        self.width = geo[0]
        self.colour = colour
        self.window = window
        self.co_ords = co_ords
        self.font = "Trebuchet MS"
        self.fontsize = 14
    
    def build_entrybox(self):
        """
        Builds entry box from general attributes belonging to object
        """
        _entry = Entry(self.window, relief = "sunken", bd = 4, width = self.width, font = (self.font , str(self.fontsize)))
        _entry.pack()
        _entry.place(y = self.co_ords[1], x = self.co_ords[0])
        return _entry
    
    def build_canvas(self): 
        """
        Builds canvas from general attributes belonging to the object
        """
        _canvas = Canvas(self.window, bg = self.colour, width = self.width, height = self.height)
        _canvas.grid(padx = 2, pady = 2, row=0, column=0, rowspan=10, columnspan = 10)
        _canvas.pack()
        _canvas.place(y = self.co_ords[1], x = self.co_ords[0])
        return _canvas
        
class label_(elements_):
    """
    Daughter class of elements - extra attributes (text) and functions specifc to label widgets
    """
    def __init__(self, window, geo, colour, co_ords, text):
        #Asigns all attribuites under elements and addition attributes 
        elements_.__init__(self, window, geo, colour, co_ords)
        self.text = text
    
    def build(self):
        """
        Builds label from general and specific attributes belonging to object
        """
        _label = Label(self.window, text = self.text, width = self.width, height = self.height, bg = self.colour, font = (self.font , str(self.fontsize)))
        _label.pack()
        #Places widget in specific place from object attributes
        _label.place(y = self.co_ords[1], x = self.co_ords[0])
        return _label
    
class button_(elements_): 
    """
    Daughter class for elements - extra attributes (text and function) and functions specifc to button widget
    """
    def __init__(self, window, geo, colour, co_ords, text, function):
        elements_.__init__(self, window, geo, colour, co_ords)
        self.text = text
        self.function = function
    
    def build(self): 
        """
        Builds button from general and specific attributes belonging to object
        """
        _button = Button(self.window, text = self.text,bg= self.colour, width = self.width, height = self.height, font = (self.font , str(self.fontsize-4)), command= self.function)
        _button.pack()
        _button.place(y = self.co_ords[1], x = self.co_ords[0])

#|~~~DEFINES WIGDETS FOR OUTPUT WINDOW~~~|
#Creates output window GUI
output_window = Tk()
output_window.geometry("650x710")
output_window.title("OUTPUT WINDOW")
output_window.configure(bg = 'LightSteelBlue4')

#Creates all wdigets for the Output GUI window
graph_box = elements_(output_window, [550,300], 'gray64', [50,390])
mol_model = elements_(output_window, [550,300], 'gray64', [50,10])
final_point_label = label_(output_window, [40,2], 'LightSteelBlue4', [10,325], "Final Single Point Energy:  0.00")

#|~~~BUILDS WIDGETS~~~|
render_canvas = mol_model.build_canvas()
graph_canvas = graph_box.build_canvas()
final_energy_label = final_point_label.build()

#|~~~CREATES INPUT WINDOW AND DEFINES WIGDETS~~~|
#Creates input window GUIs
input_window = Tk()
input_window.geometry("560x450")
input_window.title("INPUT WINDOW")
input_window.configure(bg = 'LightSteelBlue3')

#Creates all widgets for the Input GUI window
mol_type_label = label_(input_window, [30,2] , 'LightSteelBlue3', [0,10], f"MOLECULE TYPE: {mol_type:>5s}")
bond_angle_label = label_(input_window, [30,2] , 'LightSteelBlue3', [0,150], f"BOND ANGLE: {bond_angle:>5.2f}")

mol_label = mol_type_label.build()
angle_label =  bond_angle_label.build()

angle_entry = elements_(input_window, [30,5], 'grey82', [10,215])

H2O_button = button_(input_window, [15,2] , 'slate grey', [10,75], "Water", lambda: change_mol_type("H2O", mol_label))
H3_button = button_(input_window, [15,2] , 'slate grey', [150,75], "Trihydrogen", lambda: change_mol_type("H3", mol_label))
BeH2_button = button_(input_window, [15,2] , 'slate grey', [290,75], "Beryllium Hydride", lambda: change_mol_type("BeH2", mol_label))
CO2_button = button_(input_window, [15,2] , 'slate grey', [430,75], "Carbon Dioxide", lambda: change_mol_type("CO2", mol_label))
enter_button = button_(input_window, [20,3], 'slate grey', [15,275], "Enter", lambda: collect_angle(_entry, angle_label))
generate_button = button_(input_window, [20,3], 'slate grey', [15, 350], "GENERATE", lambda: run_(mol_type, bond_angle, render_canvas, graph_canvas, final_energy_label)) 
#"Generate" button added to start calculation of results
#Generate button function links to main python script

#|~~~BUILDS WIDGETS~~~|

_entry = angle_entry.build_entrybox()

H2O_button.build()
H3_button.build()
BeH2_button.build()
CO2_button.build()
enter_button.build()
generate_button.build()

#Opens windows and loops to check for activity
input_window.mainloop()
output_window.mainloop()

