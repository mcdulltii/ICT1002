# ==========================================================================================
# Custom Function Imports
# ==========================================================================================
from resources.FnFiles import process_inputs                                # check import.txt and make sure entries are valid
from resources.FnFiles import identify_csv_file                             # check whether the headers are found in 1 or 2 different csv files
from resources.FnFiles import data_cleaning                                 # To clean up the csv files (only for the 2 chosen one)
from resources.FnFiles import main_process                                  # GroupBy and Sort function (+ decending rows and sum/avg)
from resources.FnFiles import compare_csv                                   # Special function: Compare 2 csv files.
from resources.FnFiles import unique_value                                  # Special function: Return interesting results from the successful tenderers
from resources.FnFiles import makegraph                                     # To create, save and show graph
# =========================================================================================
# Global Imports
# =========================================================================================
import datetime
import os
import pandas as pd
from tkinter import messagebox
import sys
import tkinter
# ==========================================================================================
# Global Variables and settings
# ==========================================================================================
time_now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")              # Get the time_now to make unique timestamp folder
filepath = os.getcwd()                                                      # get the current working directory of the function.py (and server.py) files. Used as base for file referencing


# ============================================================================================
# FUNCTIONS
# ============================================================================================


def takein_files(function_filepaths):
    """
    File includes both filepath and encoding type that is to be separated
    Take each filepath and load the dataframes accordingly

    :param function_filepaths: The current working filepath of function.py
    :return: 2 dataframes
    """
    csv_filepath_list = []                                                  # Store the path in which the .csv files are held
    encoding_list = []                                                      # Store the file's corresponding encoding type

    # Open dir.txt and read the data inside
    with open(function_filepaths + '/resources/dir.txt', 'r') as f:
        data = f.readlines()

        # Process each line, remove "\n" if any (only at end of each line)
        for line in data:
            line = line.split(',')
            if "\n" in line[1]:
                line[1] = line[1][:-1]
            # append the 2 parts into the lists csv_filepath and encoding
            csv_filepath_list.append(line[0])
            encoding_list.append(line[1])

    # Generate the 2 sets of dataframe that is to be processed
    dataframe_1 = pd.read_csv(csv_filepath_list[0], dayfirst=True, delimiter=",", encoding=encoding_list[0], parse_dates=True)
    dataframe_2 = pd.read_csv(csv_filepath_list[1], dayfirst=True, delimiter=",", encoding=encoding_list[1], parse_dates=True)
    return dataframe_1, dataframe_2


def make_directory(path, time):
    """
    Making the directory to store the results of the program

    :param path: The current working filepath of function.py as a reference point
    :param time: The current time
    :return: <created folders to contain .txt, .csv or .png files>
    """
    try:
        os.mkdir(path + "/results")
    except FileExistsError:
        pass
    try:
        os.mkdir(path + "/results/" + time)
    except FileExistsError:
        pass


def save_as_csv_txt(paths, time, dataframe, filename):
    """
    :param paths: The current working filepath of function.py
    :param time: The current time
    :param dataframe: Dataframe that is processed
    :param filename: The name to give the resulting file that is to be saved
    :return: .txt and .csv files under the results folder
    """
    # Saving the dataframe into a .csv file
    out_file = open(paths + "/results/" + time + "/{}.csv".format(filename), "w+")
    dataframe.to_csv(out_file, sep=",", index=False, line_terminator="\n")

    # Saving the dataframe into a .txt file
    out_file = open(paths + "/results/" + time + "/{}.txt".format(filename), "w+")
    dataframe.to_csv(out_file, sep="\t", index=False)


def use_this_dataframe(user_inputs, path, first_chosen_dataframe, second_chosen_dataframe):
    """
    :param user_inputs:  Dictionary containing the user's option and their corresponding value
    :param path: The current working filepath of function.py
    :param first_chosen_dataframe: The first dataframe that was read
    :param second_chosen_dataframe: The second dataframe that was read
    :return: dataframe corresponding to the (group) of chosen header(s)
    """

    # Check whether the headers belong to which dataframe
    csv_number = identify_csv_file.verify_headers(user_inputs["select"], path)
    print(csv_number)
    if csv_number == 1:                                                             # Headers are present in the first dataframe
        print(1)
        return first_chosen_dataframe
    elif csv_number == 2:                                                           # Headers are present in the second dataframe
        print(2)
        return second_chosen_dataframe


def output_html(integratable_message):
    """
    Inside this HTML file, there will be a Click Here hyperlink that allows the user to process different stuff using the same sets of CSV
    There is also a reset button, which will allow users to choose 2 other sets of csv file (a generic option)

    :param integratable_message: The string or HTML code (as string) that is to be included into the skeleton
    :return: The integrated message containing both the skeleton and the added message
    """

    output_html_body = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="icon" href="data:;base64,iVBORw0KGgo=">
        <link rel="stylesheet" href="style.css">
        <title>Processed Results </title>
    </head>
    <body>
        <div style="color:black; margin: 10px auto 15px auto; text-align:center; ">
        <button class = "button_output" onclick= "location.href='http://localhost:8000/'" style="display:inline-block;"> Back </button>
        <form target="dummyframe" action="" method="post" style="display:inline-block; margin-top:10px;">
        <button class = "button_output" name="reset" value="reset" onclick="setTimeout(function(){},1000);">Choose other CSV files</button>
        </form>
        <iframe width="0" height="0" border="0" name="dummyframe" id="dummyframe" style="display:none;"></iframe>
        </div>
        {}
    </body>
    </html>""".format("window.location.href='http://localhost:8000/python.html';", integratable_message)
    return output_html_body


def save_dataframe_as_html(path, processed_dataframe):
    """
    :param path:  The current working filepath of function.py
    :param processed_dataframe: Processed dataframe
    :return: An overwritten python.html file which server.py will redirct to
    """
    # Gives the HTML code from the dataframe, string type
    table_output = processed_dataframe.to_html(justify="left")
    # Output as HTML file as table format
    final_html_code = output_html(table_output)
    with open(path + "/resources/python.html", "w+") as f:
        f.write(final_html_code)
        f.close()


def save_string_as_html(path, string):
    """
    :param path:  The current working filepath of function.py
    :param string: String or HTML code (as string)
    :return: An overwritten python.html file which server.py will redirct to
    """
    # Output as HTML file
    final_html_code = output_html(string)
    with open(path + "/resources/python.html", "w+") as f:
        f.write(final_html_code)
        f.close()


def success_message():
    """
    :return: Message box indicating that the process has completed successfully.
    """
    return messagebox.showinfo("Success", "Function successfully completed.\nResults can be found in 'results' folder")


# ================================================================================================
#
# Main Integration File / MAIN FUNCTION
#
# ================================================================================================


def main():
    """
    This assumes that the user has started the server.py which will result in the creation of certain .txt files needed for this program to work
    The process will be as follows:
    1. The file will read the import.txt file which contains user input from the web UI. It will check and validate the form
    2. A message will show to alert the user that it has receive the input and is starting to process
    3. The program will then load the 2 dataframes from the chosen csv file
    4. Make the necessary directories to hold the results
    5.1. If the user chooses the group or select function, run the function in main_process.py and then output the results
    5.2. If the user chooses the compare function, run the functions in compare_csv.py and unique_value.py.
        Note that this selection is very specific to the 2 datasets that we have chosen; using any other csv files will result in an error.
    5.3. If the user chooses the graph function, run the function in makegraph.py and outpt the results.
        This is a generic function that works with any csv file. But it does not guarantee clean and presentable results.
    6. HTML version of the result is saved in python.html, which is called by server.py at the end of the execution

    More details can be found in the individual function files.
    """

    # Reads import.txt file. Checks for any incomplete portions. End execution if form incomplete. Otherwise return dictionary
    user_input_dict, user_input_list = process_inputs.process_input(filepath)

    # To remove the Tkinter window box
    messagebox.showinfo("Form posted", "Entry captured. Dismiss this message to start the processing.")

    # Get the file path the 2 csv files and open them, returns 2 dataframes corresponding to the 2 chosen csv files
    df1, df2 = takein_files(filepath)

    # Making the directory which will hold the results
    make_directory(filepath, time_now)

    # ---- If the user chooses GroupBy ------ #
    if "group" in user_input_dict['checkbox']:
        try:
            # identify which csv file this header is from and choose its corresponding dataframe. Also check validity of chosen headers. Terminate if conditions not met.
            chosen_dataframe = use_this_dataframe(user_input_dict, filepath, df1, df2)

            # Returns result, which is a series of dataframes (usually >1 dataframes)
            results = main_process.selection(chosen_dataframe, user_input_list)
            if isinstance(results,tuple):
                counter = 1
                table_output = ''
                # Try to save returned dataframe from the results above, if that dataframe is empty, continue iteration.
                for every in results:
                    try:
                        save_as_csv_txt(filepath, time_now, every, "{}_{}".format(user_input_dict['select'], counter))  # Save as csv and txt file
                        # Adding HTML lines and pad it
                        table_output += every.to_html(justify="left")
                        table_output += "<br><br><br><br><br><br>"
                        counter += 1
                    except:
                        continue
                # After the csv and txt files are saved, the combined HTML code gets written to python.html
                final_html_code = output_html(table_output)
            else:
                save_as_csv_txt(filepath, time_now, results, "{}".format(user_input_dict['select']))  # Save as csv and txt file
                something = results.to_html(justify="left")
                final_html_code = output_html(something)

            with open(filepath+"/resources/python.html", "w+") as f:
                f.write(final_html_code)
                f.close()
            success_message()
        except ValueError:
            sys.exit(messagebox.showerror("Error", "ValueError exception occurred"))

    # ----- If the user chooses Selection ------ #
    elif "selection" in user_input_dict['checkbox']:
        try:
            # identify which csv file this header is from and choose its corresponding dataframe. Also check validity of chosen headers. Terminate if conditions not met.
            chosen_dataframe = use_this_dataframe(user_input_dict, filepath, df1, df2)
            print(chosen_dataframe)
            results = main_process.selection(chosen_dataframe, user_input_list)

            # save the resulting dataframe as .csv, .txt and show up in html
            save_as_csv_txt(filepath, time_now, results, "sorted_by_{}".format(user_input_dict['select'].split(',')[0], ))
            save_dataframe_as_html(filepath, results)
            success_message()
        except ValueError:
            sys.exit(messagebox.showerror("Error", "ValueError exception occurred"))

    # ------ If the user chooses Compare ----- #
    # #### Function specific to only the 2 chosen datasets. Other datasets/csv will not work. ######
    elif "compare" in user_input_dict['checkbox']:
        # essentially trial and error, if 1st dataframe is not ura, and if 2nd dataframe is not ura, throw error
        try:
            company_collab = unique_value.company_collab(df1)
        except:
            try:
                company_collab = unique_value.company_collab(df2)
            except:
                sys.exit(messagebox.showerror("Error", "The selection 'compare' does not apply to custom csv files.\nPlease use the original 2 csv files.\nProgram terminating..."))

        try:
            not_company = unique_value.not_company(df1)
        except:
            try:
                not_company = unique_value.not_company(df2)
            except:
                sys.exit(messagebox.showerror("Error", "The selection 'compare' does not apply to custom csv files.\nPlease use the original 2 csv files.\nProgram terminating..."))

        compare_result = compare_csv.compare_csv(df1, df2)  # already has self-checking function inside

        # Save each result in .csv and .txt
        save_as_csv_txt(filepath, time_now, company_collab, "Successful_tenderer_company_collab")
        html_code_1 = company_collab.to_html(justify="left")

        save_as_csv_txt(filepath, time_now, not_company, "Successful_tenderer_not_company")
        html_code_2 = not_company.to_html(justify="left")

        save_as_csv_txt(filepath, time_now, compare_result, "combined_data")
        html_code_3 = compare_result.to_html(justify="left")

        # combines the HTML code from each of the individual functions and combine them as 1 HTML output.
        combined_html_code = html_code_1 + "<br><br><br><br><br><br>" + html_code_2 + "<br><br><br><br><br><br>" + html_code_3

        save_string_as_html(filepath, combined_html_code)
        success_message()

    # ------If the user chooses Graph------ #
    elif "graph" in user_input_dict['checkbox']:
        # Chooses which dataframe to use
        if 'first' in user_input_dict['csv']:
            chosen_df = df1
        elif 'second' in user_input_dict['csv']:
            chosen_df = df2

        # Cleaning the dataframe (only works for the 2 chosen dataframes, if other csv files, dataframe will not be processed at this stage)
        try:
            cleaned_dataframe = data_cleaning.clean_ura(chosen_df)
        except:
            try:
                cleaned_dataframe = data_cleaning.clean_acra(chosen_df)
            except:
                cleaned_dataframe = chosen_df

        # identify the x and y axis from the headers
        x_input = user_input_dict['x']
        y_input = user_input_dict['y']

        # Output accordingly to the type of graphs
        if 'bar' in user_input_dict['type']:
            html_code = makegraph.make_barchart(filepath, time_now, x_input, y_input, cleaned_dataframe)
            save_string_as_html(filepath, html_code)

        elif 'line' in user_input_dict['type']:
            html_code = makegraph.make_linechart(filepath, time_now, x_input, y_input, cleaned_dataframe)
            save_string_as_html(filepath, html_code)

        elif 'pie' in user_input_dict['type']:
            html_code = makegraph.make_piechart(filepath, time_now, x_input, y_input, cleaned_dataframe)
            save_string_as_html(filepath, html_code)
        success_message()



# main()
