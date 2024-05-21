#Imports another python files needed
import gui_v2
import render_and_generate_file_v2
import search_file
import graph_results_v2

#Creates varible for the final single-point energy. 
#Variable made global so can be updated from function
global final_energy
final_energy = 0.00
#Creates all atoms that are used in molecules
all_atoms = render_and_generate_file_v2.create_atom_types()

def run_(atom1, atom2, atom3, bond_angle, orca_function, render_canvas, graph_canvas, plot_colour, energy_label):
    """
    Function that combines all sections of code, running functions in correct order 
    """
    #Create object in 'molcule' class dependant on atom1, atom2, atom3
    #Creates mol_type from atoms choosen
    work_mol = render_and_generate_file_v2.molecule([atom1+'_1',atom2+'_2',atom3+'_3'],[-1,-1,-1])
    mol_type = str(work_mol.symbol_comp[0]+work_mol.symbol_comp[1]+work_mol.symbol_comp[2])
    #Calls function to calculate the placement of atoms in molecule, dependant on angle entered and molecule selected
    work_mol.calculate_co_ords(bond_angle, 100)
    #Call function to create an orca input file based on coordinates previously calculated 
    input_file_name, direct_name = render_and_generate_file_v2.build_orca_file(mol_type, work_mol.symbol_comp, work_mol.co_ords, orca_function)
    #Call function to run orca input file through Orca in CMD
    output_file_name = render_and_generate_file_v2.run_orca(input_file_name, direct_name)
    
    #Searched through Orca output file for the final single-point energy
    found_status, final_energy = search_file.search_output_file(output_file_name, direct_name)
    
    #Creates graph on current and prevous results
    pic_filename = graph_results_v2.cont_plot([bond_angle, final_energy], plot_colour, mol_type, direct_name)
    
    #Updates canvas with saved graph of results
    #Rendered simple molecule graphic into separate canvas
    gui_v2.graph_final_energy_config(energy_label, final_energy, graph_canvas, pic_filename)
    work_mol.render(bond_angle, render_canvas, mol_type)
    return