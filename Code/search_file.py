def search_output_file(file_name, direct):
    """
    Function that searches through for final single-point energy in Orca output text file
    """
    #Opens Orca output text file - read-only
    file = open(direct +  "\\" + file_name, 'r')
    #Assumes there is no final single-point energy within text file
    found = False
    #For loops reads through each line in text file one at a time
    for line in file.readlines():
        #Splits line
        line = line.split()
        #Checks length of line as length of line with final single-point energy on is know
        #Avoids looping checking line that's to short, or unnecessary
        if len(line) == 5:
            #Checks lines contents
            if line[0] == "FINAL" and line[1] == "SINGLE" and line[2] == "POINT" and line[3] == "ENERGY":
                #Stores final sinlge-point energy in variable
                #Changes 'found' to True
                final_energy = float(line[4])
                found = True
                break #Stops loop
    file.close() #Closes text file
    #Checks to see if found is false, if so prints error message and set final_energy to 0.00
    if not found:
            print("Error: Final Single-Point Energy not found")
            final_energy = 0.00
    return found, final_energy
