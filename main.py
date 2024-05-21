#Imports another python files needed
import gui
import render_and_generate_file
import search_file
import graph_results

#Creates varible for the final single-point energy. 
#Variable made global so can be updated from function
global final_energy
final_energy = 0.00
#Creates all atoms that are used in molecules
render_and_generate_file.create_atom_types()

def run_(mol_type, bond_angle, render_canvas, graph_canvas, energy_label):
    """
    Function that combines all sections of code, running functions in correct order 
    """
    #Create object in 'molcule' class dependant on variable mol_type
    #Uses if statements to compare against 'mol_type'
    if mol_type == "H2O":
        work_mol = render_and_generate_file.molecule(['H_1','O_1','H_2'],[-1,-1,-1])
    elif mol_type == "H3":
        work_mol = render_and_generate_file.molecule(['H_1','H_2','H_3'],[-1,-1,-1])
    elif mol_type == "BeH2":
        work_mol = render_and_generate_file.molecule(['H_1', 'Be_1', 'H_2'],[-1,-1,-1])
    elif mol_type == "CO2":
        work_mol = render_and_generate_file.molecule(['O_1', 'C_1', 'O_2'],[-1,-1,-1])
    else:
        print("No molecule") #Error handling
        return
    #Calls function to calculate the placement of atoms in molecule, dependant on angle entered and molecule selected
    work_mol.calculate_co_ords(bond_angle, 100)
    #Call function to create an orca input file based on coordinates previously calculated 
    input_file_name = render_and_generate_file.build_orca_file(mol_type, work_mol.symbol_comp, work_mol.co_ords)
    #Call function to run orca input file through Orca in CMD
    output_file_name = render_and_generate_file.run_orca(input_file_name)
    
    #Searched through Orca output file for the final single-point energy
    found_status, final_energy = search_file.search_output_file(output_file_name, input_file_name)
    
    #Creates graph on current and prevous results
    pic_filename = graph_results.cont_plot([bond_angle, final_energy], work_mol.get_colour(1),input_file_name)
    
    #Updates canvas with saved graph of results
    #Rendered simple molecule graphic into separate canvas
    gui.graph_final_energy_config(energy_label, final_energy, graph_canvas, pic_filename)
    work_mol.render(bond_angle, render_canvas, mol_type)
    return