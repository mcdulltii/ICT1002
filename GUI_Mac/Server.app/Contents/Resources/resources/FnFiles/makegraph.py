# =========================================================================================
# Global Imports
# =========================================================================================
import matplotlib.pyplot as pyplot
import numpy as np
import io
import base64
from tkinter import messagebox
import sys
# ============================================================================================
# FUNCTIONS
# ============================================================================================


def save_as_png(path, time_now, string):
    """
    :param path: filepath of function.py
    :param time_now: time of execution of function.py (used to save in result folder)
    :param string: the name to give the file
    :return: .png file which contains the respective figure
    """
    return pyplot.savefig(path+"/results/"+time_now+"/{}.png".format(string), bbox_inches="tight")


def get_html_string():
    """
    Get the graph data, convert to base 64 formatting so that the figure can be 'represented' using a string, which is then decoded.

    :return: HTML code as string type in html format
    """
    # Get Base64 encoded value (string type)
    encoding_img = io.BytesIO()
    pyplot.savefig(encoding_img, format="png", bbox_inches="tight")
    encoded = base64.b64encode(encoding_img.getvalue())

    # HTML code taking in encoded data
    html_code = "<img src='data:image/png;base64, {}'>".format(encoded.decode('utf-8'))
    return html_code


def read_header_for_graph(x, y, processed_dataframe):
    """
    Takes in the dataframe, get the x and y axis and process its relevant data
    return the parameters necessary to make the graphs.

    :param x: header corresponding to the x-axis label
    :param y: header corresponding to the y-axis label
    :param processed_dataframe: Processed dataframe
    :return: a set of variables containing the x,y axis names, x,y data and the "length" of x-axis (so that each value on the x axis is unique later on)
    """
    # Headers, Strings
    x_axis = x
    y_axis = y

    # Datatype: Series
    x_axis_data = processed_dataframe[x_axis]
    y_axis_data = processed_dataframe[y_axis]

    # Find how many sets of data there are
    x_axis_length = np.arange(len(x_axis_data))
    return x_axis, y_axis, x_axis_data, y_axis_data, x_axis_length  # 5 output variables


def make_piechart(path, time_now, x, y, processed_dataframe):
    """
    Make and save a piechart
    :param path: filepath of function.py
    :param time_now: time of execution of function.py (used to save in result folder)
    :param x: header corresponding to the x-axis label
    :param y: header corresponding to the y-axis label
    :param processed_dataframe: processed dataframe
    :return: piechart in .png and shows in HTML
    """
    try:
        # Takes in the parameters
        x_axis, y_axis, x_axis_data, y_axis_data, x_axis_length = read_header_for_graph(x, y, processed_dataframe)
        # Plots piechart
        pyplot.title("{} by {}".format(y_axis, x_axis), pad=120)
        pyplot.pie(x=y_axis_data, labels=x_axis_data, rotatelabels=True, radius=1.4, labeldistance=1.0, autopct='%1.1f%%', pctdistance=0.8)
        # Output
        save_as_png(path, time_now, "piechart")
        return get_html_string()
    except:
        sys.exit(messagebox.showerror("Error", "Non-numerical value on y-axis. Please use a numerical value"))


def make_barchart(path, time_now, x, y, processed_dataframe):
    """
    Make and save a barchart
    :param path: filepath of function.py
    :param time_now: time of execution of function.py (used to save in result folder)
    :param x: header corresponding to the x-axis label
    :param y: header corresponding to the y-axis label
    :param processed_dataframe: processed dataframe
    :return: barchart in .png and shows in HTML
    """
    try:
        # Taking in parameters
        x_axis, y_axis, x_axis_data, y_axis_data, x_axis_length = read_header_for_graph(x, y, processed_dataframe)
        fig, ax = pyplot.subplots()
        # Plots the barchart
        ax.bar(x_axis_length, y_axis_data)
        # Set chart settings
        xysize = pyplot.gcf()
        xysize.set_size_inches(50, 10.5)
        ax.ticklabel_format(style="plain")
        ax.set_ylabel(y_axis)
        ax.set_title("{} by {}".format(y_axis, x_axis), pad=20)
        ax.set_xticks(x_axis_length)
        pyplot.xticks(rotation=90)
        ax.set_xticklabels(x_axis_data)
        # Output
        save_as_png(path, time_now, "barchart")
        return get_html_string()
    except:
        sys.exit(messagebox.showerror("Error", "Non-numerical value on y-axis.Please use a numerical value"))


def make_linechart(path, time_now, x, y, processed_dataframe):
    """
    Make and save a line-based graph
    :param path: filepath of function.py
    :param time_now: time of execution of function.py (used to save in result folder)
    :param x: header corresponding to the x-axis label
    :param y: header corresponding to the y-axis label
    :param processed_dataframe: processed dataframe
    :return: line-based graaph in .png and shows in HTML
    """
    try:
        # Take in parameters
        x_axis, y_axis, x_axis_data, y_axis_data, x_axis_length = read_header_for_graph(x, y, processed_dataframe)
        fig, ax = pyplot.subplots()
        # Plot line chart
        pyplot.plot(x_axis_length, y_axis_data)
        # Set relevant settings
        xysize = pyplot.gcf()
        xysize.set_size_inches(50, 10.5)
        ax.ticklabel_format(style="plain")
        ax.set_ylabel(y_axis)
        ax.set_title("{} by {}".format(y_axis, x_axis), pad=20)
        ax.set_xticks(x_axis_length)
        pyplot.xticks(rotation=90)
        ax.set_xticklabels(x_axis_data)
        # Output
        save_as_png(path, time_now, "linechart")
        return get_html_string()
    except:
        sys.exit(messagebox.showerror("Error", "Non-numerical value on y-axis. Please use a numerical value"))
