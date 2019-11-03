# python 3!
# =========================================================================================
# Global Imports
# =========================================================================================
import pandas as pd
import numpy as np
from itertools import chain
from tkinter import messagebox
import sys
# ============================================================================================
# FUNCTIONS
# ============================================================================================


# return list from series of separated string
def chainer(x):
    """
    :param x: Series of successful_tenderer_name column in dataframe of vacant sites by URA
    :return: List of all split successful tenderers in the dataframe
    """
    return list(chain.from_iterable(x.str.split(r', | & | \band\b')))


# Split multiple companies in successful_tenderer_name to form new rows per company
def split_name(tenderer):
    """
    :param tenderer: Dataframe of vacant sites by URA
    :return: List of each successful tenderer name after splitting
    """
    # Split multiple company names separated by ',' or '&'
    tenderer_split = tenderer['successful_tenderer_name'].str.split(r', | & | \band\b')
    return tenderer_split


def processing_function(tenderer, entity):
    """
    :param tenderer: Dataframe of vacant sites by URA
    :param entity: Dataframe of entities registered under URA
    :return: Merged dataframe of dataframe1 and dataframe2
    :description: Create new dataframe after splitting successful_tenderer_name that has multiple names.
    Afterwards, merge the newly created dataframe with the entities registered under ACRA dataframe.  
    """
    # calculate lengths of splits
    split_len = split_name(tenderer).map(len)

    # Store result into new data frame
    new_tenderer = pd.DataFrame({'successful_tenderer_name': chainer(tenderer['successful_tenderer_name']),
                                 'date_of_launch': np.repeat(tenderer['date_of_launch'], split_len),
                                 'date_of_tender_closing': np.repeat(tenderer['date_of_tender_closing'], split_len),
                                 'date_of_award': np.repeat(tenderer['date_of_award'], split_len),
                                 'location': np.repeat(tenderer['location'], split_len),
                                 'type_of_devt_allowed': np.repeat(tenderer['type_of_devt_allowed'], split_len),
                                 'lease': np.repeat(tenderer['lease'], split_len),
                                 'type_of_devt_code': np.repeat(tenderer['type_of_devt_code'], split_len),
                                 'site_area': np.repeat(tenderer['site_area'], split_len),
                                 'gross_plot_ratio': np.repeat(tenderer['gross_plot_ratio'], split_len),
                                 'no_of_bids': np.repeat(tenderer['no_of_bids'], split_len),
                                 'gross_floor_area': np.repeat(tenderer['gross_floor_area'], split_len),
                                 'successful_tender_price': np.repeat(tenderer['successful_tender_price'], split_len),
                                 'psm_per_gpr_or_gfa': np.repeat(tenderer['psm_per_gpr_or_gfa'], split_len),
                                 'planning_area': np.repeat(tenderer['planning_area'], split_len)})

    # Change successful_tenderer_name to upper case
    new_tenderer['successful_tenderer_name'] = new_tenderer['successful_tenderer_name'].str.upper()

    # Ensure entity_name is upper case
    entity['entity_name'] = entity['entity_name'].str.upper()

    # Merge both data frame based on successful_tenderer_name and entity_name
    # Returns only successful_tenderer_name that are found in entity_name
    merged_results = pd.merge(entity, new_tenderer, left_on=['entity_name'], right_on=['successful_tenderer_name'],
                              how='inner')
    # Remove unnecessary duplicate column entity_name
    merged_results = merged_results.drop('entity_name', 1)
    return merged_results


# START OF MAIN FUNCTION
def compare_csv(dataframe1, dataframe2):
    """
    :param dataframe1: Dataframe of vacant sites by URA
    :param dataframe2: Dataframe of entities registered under URA
    :return: Merged dataframe of dataframe1 and dataframe2
    :description: Main function to call processing_function that merges both dataframes and return a merged dataframe
    """
    try:
        # Get tenderer and entity data frame respectively
        tenderer = dataframe1
        entity = dataframe2
        merged_results = processing_function(tenderer, entity)
        return merged_results

    except KeyError:     # Except when suppose if the dataframe order is reversed
        try:
            # Get tenderer and entity data frame respectively, but the order is flipped
            tenderer = dataframe2
            entity = dataframe1
            merged_results = processing_function(tenderer, entity)
            return merged_results

        except KeyError:
            sys.exit(messagebox.showerror("Error", "The selection 'compare' does not apply to custom csv files.\nPlease use the original 2 csv files.\nProgram terminating..."))
    except:
        sys.exit(messagebox.showerror("Error", "The selection 'compare' does not apply to custom csv files.\nPlease use the original 2 csv files.\nProgram terminating..."))

