#Imports all libraries needed
import turtle 
import numpy as np
from datetime import date
from datetime import datetime
import os

class atom:
    """
    Class of all elemental atoms within a molecule
    """
    def __init__(self, element, symbol, size, colour):
        #Assigns all attributes using value passed through function to object
        self.element = element
        self.symbol = symbol
        self.size = size
        self.colour = colour

class molecule:
    """
    Class with all attributes and function required to deal with a molecule
    """
    def __init__(self, composition, co_ords):
        self.composition = composition
        self.co_ords = co_ords
        self.symbol_comp = []
        
        #Fills attribute 'symbol_compostion' with compostion of elemental symbols
        for atom in composition: 
            atom = atom.split('_')
            self.symbol_comp.append(atom[0])
    
    def calculate_co_ords(self, bond_angle, bond_length): 
        """
        Calcuales the co-ords of atoms (with the the 3 atom molecule) 
        """
        #Sets central atoms coordinates to origin
        self.co_ords[1] = [0,0]
        #Calculates angle between: north, central molecule, and termianl atoms
        angle = np.radians(180-bond_angle)/2
        #Calculates the vector values that can be translated into coordinates
        i = bond_length*np.cos(angle) 
        j = bond_length*np.sin(angle)
        #Sets coordinates of remain atoms using vectors
        self.co_ords[0] = [-i,j]
        self.co_ords[2] = [i,j]
        return
    
    def type_2_render(self, index):
        """
        Retreives all visual attributes (colour. size) of an atom with the molcule
        """
        if self.symbol_comp[index] == hydro.symbol:
            return hydro.size, hydro.colour
        elif self.symbol_comp[index] == oxy.symbol:
            return oxy.size, oxy.colour
        elif self.symbol_comp[index] == beryl.symbol:
            return beryl.size, beryl.colour
        elif self.symbol_comp[index] == carbon.symbol:
            return carbon.size, carbon.colour
        return 12, 'blue'

    def render(self, bond_angle, canvas, mol_type):
        """
        Render image of molecule selected by the user
        """
        #Sets up canvas to be drawn on
        canvas_ = turtle.TurtleScreen(canvas)
        #Clears canvas for new rendering
        canvas_.clearscreen()
        
        _canvas = turtle.RawTurtle(canvas)
        canvas_.bgcolor("silver") #changes colour of canvas backgroud
        _canvas.hideturtle() #Hides turtle so no arrow visible
        _canvas.width(2) #Sett line width
        #If molecule is CO2 line width is thicked to show double bond between atoms
        if mol_type == "OCO":
            _canvas.width(10)
        #for loop creates lines (bonds) between each atom - from origin/central atom to terminal atoms
        for index in range(0,len(self.co_ords),2):
            _canvas.home()
            _canvas.down()
            _canvas.goto(self.co_ords[index][0],self.co_ords[index][1])
            _canvas.up()
        
        _canvas.home() #Draws central atom - central atom always at origin
        radius, colour = self.type_2_render(1)
        _canvas.dot(radius, colour)
        
        #Draws left termianl atom
        _canvas.goto(self.co_ords[0][0],self.co_ords[0][1])
        #Collects the correct visible attributes for the atom being drawn
        radius, colour = self.type_2_render(0)
        _canvas.dot(radius, colour)
        
        #Draws right termainl atom
        _canvas.goto(self.co_ords[2][0],self.co_ords[2][1])
        radius, colour = self.type_2_render(2)
        _canvas.dot(radius, colour)
        
        return

def create_atom_types():
    """
    Creates selection of atoms to be used within molecules, stating all attributes
    """
    global hydro, oxy, beryl, carbon
    hydro = atom("Hydrogen","H", 30, 'grey')
    oxy = atom("Oxygen","O",60, 'red')
    beryl = atom("Berylllium", "Be", 49, "orange")
    carbon = atom("Carbon","C", 40, "black")
    return [hydro.symbol, oxy.symbol, beryl.symbol, carbon.symbol]

def file_name_gen(mol_type): 
    """
    Creates file name including the molecule type, current date and time
    """
    name = (mol_type + '_' + str(date.today()) + '_' + str(datetime.now().strftime("%H-%M-%S")))
    return name+".txt", name

def build_orca_file(mol_type, mol_comp, mol_co_ords, orca_function): 
    """
    Fucntion generates the Orca input file
    """
    #Create filename for Orca input file
    work_file_name, direct_name = file_name_gen(mol_type)
    #Creates new directory and the text file using the filename generated
    os.mkdir(direct_name)
    file_script = open(direct_name+ "\\"+ str(work_file_name),"a")
    #If moleucle is H£ the positive cahrge must be specified in the Orca input file
    if mol_comp[1 == "h"]:
        #Writes contains into text file
        file_script.write("#Input generated by program\n" + str(orca_function) + "\n\n* xyz +1 1 \n")
    else:
        file_script.write("#Input generated by program\n" + str(orca_function) + "\n\n* xyz 0 1 \n")
    #Writes atom symbol and coordinates within text file
    for atom_index in range(len(mol_comp)):
        file_script.write("   " + str(mol_comp[atom_index]) +"        "+ str(mol_co_ords[atom_index][0]) +"        "+ "0.0" +"        "+ str(mol_co_ords[atom_index][1]) + "\n")
    file_script.write("*\n")
    file_script.close() #Closes test file
    return work_file_name, direct_name #Returns filename

def run_orca(file_name, direct_name):
    """
    Runs input file through Orca in CMD and return output filename
    """
    #file_name = file_name
    #Gets path for current directory within documents
    current_dir = os.getcwd()
    #Moves CMD to correct/current working direcetory
    os.chdir(current_dir + "\\"+ direct_name)
    #Wriets command line
    #Runs command line created in CMD
    orca_command_line = str("orca "+ str(file_name)+ " > "+ str( "output_"+file_name))
    os.system(orca_command_line)
    #print(orca_command_line)
    #Moves back of diectory, to directory containing code
    os.chdir(current_dir)
    return str("output_"+file_name)