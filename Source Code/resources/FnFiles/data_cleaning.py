# python 3!
# =========================================================================================
# Global Imports
# =========================================================================================
import pandas as pd
# ============================================================================================
# FUNCTIONS
# ============================================================================================


def clean_ura(data):
    """
    :param: URA file
    Used to check URA file. It will first check against a preset values for the coloumns in the dataset. Then it will
    check row by row, if any data in any cell is in the incorrect format or value, the entire row will be dropped.
    :return: correct URA dataset with no errors when used by other functions.
    """
    uracolumns = {'date_of_launch', 'date_of_tender_closing', 'date_of_award', 'location', 'type_of_devt_allowed',
                  'lease',
                  'type_of_devt_code', 'site_area', 'gross_plot_ratio', 'gross_floor_area', 'no_of_bids',
                  'successful_tenderer_name',
                  'psm_per_gpr_or_gfa', 'planning_area'}
    data1 = pd.DataFrame(data)

    if uracolumns.issubset(data1.columns):
        try:
            data1['date_of_launch'].str.match("[\d]{1,2}/[\d]{1,2}/[\d]{4}")

            data1['date_of_tender_closing'].str.match("[\d]{1,2}/[\d]{1,2}/[\d]{4}")

            data1['date_of_award'].str.match("[\d]{1,2}/[\d]{1,2}/[\d]{4}")

            if data1.lease.dtype or data1.no_of_bids.dtype or data1.successful_tender_price.dtype is not int:
                data1.dropna(inplace=True)

            if data1.site_area.dtype or data1.psm_per_gpr_or_gfa.dtype is not float:
                data1.dropna(inplace=True)

            data1['type_of_devt_allowed'].str.match(
                "^(\w*(Hotel)\w*)|(\w*(Commercial)\w*)|(\w*(Industrial)\w*)|(\w*(Residential)\w*)|(\w*(Business)\w*)|(\w*(Condominium)\w*)|(\w*(Restoration)\w*)|(\w*(Food)\w*)|(\w*(White)\w*)|(\w*(Office)\w*)|(\w*(Housing)\w*)|(\w*(Flats)\w*)|(\w*(Hospital)\w*)|(\w*(Recreation)\w*)|(\w*(Development)\w*)|(\w*(Light)\w*)|(\w*(Apartment)\w*)|(\w*(General)\w*)|(\w*(Civic)\w*)|(\w*(Christian)\w*)|(\w*(Buddist)\w*)|(\w*(Farm)\w*)|(\w*(Medical)\w*)|(\w*(Holiday)\w*)|(\w*(Car)\w*)|(\w*(Boatel)\w*)")

            data1['type_of_devt_code'].str.match(
                "^(\w*(Hotel)\w*)|(\w*(Commercial)\w*)|(\w*(Industrial)\w*)|(\w*(Residential)\w*)|(\w*(Business)\w*)|(\w*(Condominium)\w*)|(\w*(Restoration)\w*)|(\w*(Food)\w*)|(\w*(White)\w*)|(\w*(Office)\w*)|(\w*(Housing)\w*)|(\w*(Flats)\w*)|(\w*(Hospital)\w*)|(\w*(Recreation)\w*)|(\w*(Development)\w*)|(\w*(Light)\w*)|(\w*(Apartment)\w*)|(\w*(General)\w*)|(\w*(Civic)\w*)|(\w*(Christian)\w*)|(\w*(Buddist)\w*)|(\w*(Farm)\w*)|(\w*(Medical)\w*)|(\w*(Holiday)\w*)|(\w*(Car)\w*)|(\w*(Boatel)\w*)")

            if data1.location.dtype or data1.successful_tenderer_name.dtype or data1.planning_area.dtype is not str:
                data1.dropna(inplace=True)

            data1['gross_plot_ratio'].str.match("(^na$)|(\d*\.\d+)|([1-3]{1})")

            data1['gross_floor_area'].str.match("(^na$)|(\d*\.\d+)|([0-9]{1,6})")

            # Replace 'na' to a value of 0
            data1 = data1.replace('na', 0)

            return data1
        except:
            print('Error')
            return data
    else:
        return pd.DataFrame()


def clean_acra(data):
    """
    :param: ACRA file
    Used to check ACRA file. It will first check against a preset values for the coloumns in the dataset. Then it will
    check row by row, if any data in any cell is in the incorrect format or value, the entire row will be dropped.
    :return: correct ACRA dataset with no errors when used by other functions.
    """
    acracolumns = {'uen', 'issuance_agency_id', 'uen_status', 'entity_name', 'entity_type', 'uen_issue_date',
                   'reg_street_name', 'reg_postal_code'}

    data1 = pd.DataFrame(data)

    if acracolumns.issubset(data1.columns):
        try:
            data1['uen_issue_date'].str.match("[\d]{1,2}/[\d]{1,2}/[\d]{4}")

            data1.drop(data1[data1.issuance_agency_id != 'ACRA'].index, inplace=True)

            data1['entity_type'].str.match("(^BN$)|(^LC$)")

            data1['uen_status'].str.match("(^D$)|(^R$)")

            data1['uen'].str.match("(^[0-9]{8,9})([A-Z]$)")

            data1['entity_name'].str.match("[A-Z]{1,}")

            data1['reg_street_name'].str.match("([A-Z]{1,})|(^na$)")

            data1['reg_postal_code'].str.match("(^na$)|([0-9]{6})")
            return data1
        except ValueError:
            print('Error')
            return data
    else:
        return pd.DataFrame()
