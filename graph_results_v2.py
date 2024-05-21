#Imports library to be used within script
import numpy as np
from matplotlib import pyplot as plt

#Creates empty list to hold previous results
results = []
colours = []
mol_types = []

def cont_plot(result, colour, mol_type, file_name):
    """
    Creates plot of current and previous results ofOca calculations
    """
    #Adds new reuslts and colour to respective lists
    results.append(result)
    colours.append(colour)
    mol_types.append(mol_type)
    #Changes formatted so that x co-ords are are grouped in 1 array, and all y co-ords in another array
    formatted = np.transpose(results)
    #Plots all reuslts individual so the colour of plot can be different
    for i in range(len(results)):
        plt.scatter(formatted[0][i], formatted[1][i], color = colours[i], label = mol_types[i])
    
    #Formats graph
    #Limits x-axis values
    #Creates labels
    #Adds grid to graph
    plt.xlim(0,360)
    plt.title("Historic Single-Point Energies")
    plt.xlabel("Angle (Degrees)")
    plt.ylabel("Final Single-Point Energy (Eh)")
    plt.grid()
    plt.legend()
    
    #Save graph as .png in found with Orca files for molecule
    plt.savefig(file_name+"\\Graph.png", dpi = 75)
    #Shows graph into shell
    plt.show()
    #Returns graph loaction and name
    return file_name+"\\Graph.png"