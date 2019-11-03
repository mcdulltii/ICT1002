# =========================================================================================
# Global Imports
# =========================================================================================
import sys
from tkinter import messagebox
# ============================================================================================
# FUNCTIONS
# ============================================================================================


def process_input(function_filepath):
    """
    Reads the file, if form is null or incomplete, end the execution of the file
    1. Reads import.txt for the user inputs from GUI
    2. Check each line of input for any invalid entries or empty form
    3. Return some sort of trigger to stop execution of main file if invalid entries are found
    Otherwise return a dictionary with relevant values.

    :param function_filepath: filepath of main: function.py
    :return: List and dictionary version of the user inputs.
    """
    file = open(function_filepath+"/resources/import.txt", "r")
    # Creating a list to store the lines
    input_list = file.readlines()
    file.close()

    # Check for empty form
    if input_list == []:
        return sys.exit(messagebox.showerror("Error", "Function fail to run \nReason: Empty form"))

    # Throw the values of file into a dictionary
    output_dict = {}
    count = 0
    for x in input_list:
        temp = [str(z).lower() for z in input_list[count].split(", ")]
        # check for any empty inputs
        if temp[0] == "rows":
            pass
        else:
            if temp[1] == "\n":
                return sys.exit(messagebox.showerror("Error", "Function fail to run \nReason: Incomplete form"))

        # Move on to add to dictionary if this line passes inspection
        try:
            output_dict[temp[0]] += ','+(temp[1].strip("\n"))
        except:
            output_dict[temp[0]] = (temp[1].strip("\n"))
        count += 1
    # return this result only if all lines pass inspection
    return output_dict, input_list
