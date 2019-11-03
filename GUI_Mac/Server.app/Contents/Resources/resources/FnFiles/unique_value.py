# python 3!
# =========================================================================================
# Global Imports
# =========================================================================================
import pandas as pd
# ============================================================================================
# FUNCTIONS
# ============================================================================================


def company_collab(data):
    """
    :param data: URA file
    :return: Companies collaborating on a project
    """
    data = pd.DataFrame(data)
    # cleaning of data - limitation (have to manually do this cause of some tenderer naming
    data1 = data[~data['successful_tenderer_name'].str.contains("(.*(\s(& Co).*))|(.*(\s(& Resorts).*))")][
        ['location', 'type_of_devt_allowed', 'type_of_devt_code', 'successful_tenderer_name', 'planning_area']]

    # filter for tenderers who are companies
    data2 = data1[data1['successful_tenderer_name'].str.contains(
        "(.*Pte.*(|\s)Ltd.*)|(.*Ltd)|(.*Limited)|(.*Bhd)|(.*Properties)")][
        ['location', 'type_of_devt_allowed', 'type_of_devt_code', 'successful_tenderer_name', 'planning_area']]

    # find for companies collaborating
    data3 = data2[data2['successful_tenderer_name'].str.contains("(.*&.*)|(.*(\s(and).*))|(.*(\s(And).*))")][
        ['location', 'type_of_devt_allowed', 'type_of_devt_code', 'successful_tenderer_name', 'planning_area']]
    return data3


def not_company(data):
    """
    :param data: URA file
    :return: Tenderes who are not companies
    """
    data = pd.DataFrame(data)
    # find tenderers who are not companies
    data1 = data[~data['successful_tenderer_name'].str.contains(
        "(.*Pte.*(|\s)Ltd.*)|(.*Ltd)|(.*Limited)|(.*Bhd)|(.*Properties)")][
        ['location', 'type_of_devt_allowed', 'type_of_devt_code', 'successful_tenderer_name', 'planning_area']]
    return data1
