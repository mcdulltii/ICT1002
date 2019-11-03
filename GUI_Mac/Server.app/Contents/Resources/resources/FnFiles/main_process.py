# =========================================================================================
# Global Imports
# =========================================================================================
import pandas as pd
import numpy as np
from resources.FnFiles import data_cleaning
import sys
from tkinter import messagebox
# ============================================================================================
# FUNCTIONS
# ============================================================================================


#--GENERAL GROUP BY--#
def generalGroupby(sepContent,data1):
    """

    :param sepContent:
    :param data1:
    :return:
    """
    # default 2 empty dataframe
    URAdata = pd.DataFrame()
    ACRAdata = pd.DataFrame()

    # only 1 data file#
    if data_cleaning.clean_ura(data1).empty == False:
        URAdata = data_cleaning.clean_ura(data1)
    elif data_cleaning.clean_acra(data1).empty == False:
        ACRAdata = data_cleaning.clean_acra(data1)
    if ACRAdata.empty == True and URAdata.empty == True:
        sys.exit(messagebox.showerror("Error", "Both files are neither URA nor ACRA"))

    # --Extract all columns headers and place them in their respective variables--#
    useracraHeaders, useruraHeaders = [], []
    URAHeader = list(URAdata.columns.values[0:])
    ACRAHeader = list(ACRAdata.columns.values[0:])

    # --GROUP VALIDATION--#
    def get_group(usergroup, labels, index):
        if labels in index:
            return usergroup.get_group(labels)
        else:
            return pd.DataFrame()

    # -- This check for import text, if a text in import.txt matches with a column header, it will append--#
    for i in sepContent:
        if i in URAHeader:
            useruraHeaders.append(i)
        elif i in ACRAHeader:
            useracraHeaders.append(i)

    if URAdata.empty == False:
        URAdata['date_of_award'] = pd.to_datetime(URAdata['date_of_award'], format='%Y-%m-%d')
        URAdata['date_of_tender_closing'] = pd.to_datetime(URAdata['date_of_tender_closing'], format='%Y-%m-%d')
        URAdata['date_of_launch'] = pd.to_datetime(URAdata['date_of_launch'], format='%Y-%m-%d')
        URAdata = URAdata.replace('na', 0)
        URAdata["gross_floor_area"] = URAdata["gross_floor_area"].astype('float64')
        URAdata["lease"] = URAdata["lease"].astype('int64')
        URAdata["site_area"] = URAdata["site_area"].astype('float64')
        URAdata["gross_plot_ratio"] = URAdata["gross_plot_ratio"].astype('float64')
        URAdata["no_of_bids"] = URAdata["no_of_bids"].astype('float64')
        URAdata["successful_tender_price"] = URAdata["successful_tender_price"].astype('float64')
        URAdata["psm_per_gpr_or_gfa"] = URAdata["psm_per_gpr_or_gfa"].astype('float64')
    if ACRAdata.empty== False:
        ACRAdata = ACRAdata.replace('na', 0)
        try:
            ACRAdata['uen_issue_date'] = pd.to_datetime(ACRAdata['uen_issue_date'], format='%d/%m/%Y')
        except ValueError:
            ACRAdata['uen_issue_date'] = pd.to_datetime(ACRAdata['uen_issue_date'], format='%Y-%m-%d')
        ACRAdata["reg_postal_code"] = ACRAdata["reg_postal_code"].astype('int64')
        ACRAdata['entity_name'] = ACRAdata['entity_name'].astype(str)

    # -- If the condition is more than 0, that means the user chose to group ACRA--#
    if len(useracraHeaders) > 0:
        # -- If user group by date--#
        if (useracraHeaders[0]) == 'uen_issue_date':
            # --Using pandas cut, the range will start from 1990 to 2020 with a frequency of 5 Years. Eg - 1990 to 1995--#
            bins_dt = pd.date_range(start='1/1/1990', end='1/1/2020', freq='5Ys')
            bins_str = bins_dt.astype(str).values
            labels = ['{} to {}'.format(bins_str[i - 1], bins_str[i]) for i in range(1, len(bins_str))]
            ACRAdata['group_year'] = pd.cut(ACRAdata[useracraHeaders[0]].astype(np.int64) // 10 ** 9,
                               bins=bins_dt.astype(np.int64) // 10 ** 9,
                               labels=labels)

            usergroup = ACRAdata.groupby('group_year')
            ACRAdata.set_index('group_year', inplace=True)

            dgp0 = get_group(usergroup, labels[0], ACRAdata.index)
            dgp1 = get_group(usergroup, labels[1], ACRAdata.index)
            dgp2 = get_group(usergroup, labels[2], ACRAdata.index)
            dgp3 = get_group(usergroup, labels[3], ACRAdata.index)
            dgp4 = get_group(usergroup, labels[4], ACRAdata.index)
            dgp5 = get_group(usergroup, labels[5], ACRAdata.index)

            return dgp0, dgp1, dgp2, dgp3, dgp4, dgp5

        elif (useracraHeaders[0]) == 'entity_name' or (useracraHeaders[0]) == 'reg_street_name':
            # -- Group by first character--#
            # -- Breakdown for such function, 1) Extract first character of all value and create a new column for it. 2) Group by the newly formed column. 3) Delete the column and store the value in a seperate dataframe #
            # -- Similiar method with slight twist can be found as you scroll further down--#
            # -- In this particular column, there are many combinations for this category(symbols such as !@# are also included). #
            # Therefore I have many predefined variables. However, it might not be enough. This will be reflected in the limitations reported accordingly.--#
            ACRAdata['alphabets'] = ACRAdata[useracraHeaders[0]].str[:1]
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
            zero, one, two, three, four, five, six, seven, eight, nine = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
            sym1, sym2, sym3, sym4, sym5, sym6, sym7, sym8, sym9, sym0 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
            for x in ACRAdata['alphabets']:
                if 'A' == x:
                    a = ACRAdata.groupby(['alphabets']).get_group('A')
                    a = a.drop(a.columns[-1], axis=1).reset_index(drop=True)
                elif 'B' == x:
                    b = ACRAdata.groupby(['alphabets']).get_group('B')
                    b = b.drop(b.columns[-1], axis=1).reset_index(drop=True)
                elif 'C' == x:
                    c = ACRAdata.groupby(['alphabets']).get_group('C')
                    c = c.drop(c.columns[-1], axis=1).reset_index(drop=True)
                elif 'D' == x:
                    d = ACRAdata.groupby(['alphabets']).get_group('D')
                    d = d.drop(d.columns[-1], axis=1).reset_index(drop=True)
                elif 'E' == x:
                    e = ACRAdata.groupby(['alphabets']).get_group('E')
                    e = e.drop(e.columns[-1], axis=1).reset_index(drop=True)
                elif 'F' == x:
                    f = ACRAdata.groupby(['alphabets']).get_group('F')
                    f = f.drop(f.columns[-1], axis=1).reset_index(drop=True)
                elif 'G' == x:
                    g = ACRAdata.groupby(['alphabets']).get_group('G')
                    g = g.drop(g.columns[-1], axis=1).reset_index(drop=True)
                elif 'H' == x:
                    h = ACRAdata.groupby(['alphabets']).get_group('H')
                    h = h.drop(h.columns[-1], axis=1).reset_index(drop=True)
                elif 'I' == x:
                    i = ACRAdata.groupby(['alphabets']).get_group('I')
                    i = i.drop(i.columns[-1], axis=1).reset_index(drop=True)
                elif 'J' == x:
                    j = ACRAdata.groupby(['alphabets']).get_group('J')
                    j = j.drop(j.columns[-1], axis=1).reset_index(drop=True)
                elif 'K' == x:
                    k = ACRAdata.groupby(['alphabets']).get_group('K')
                    k = k.drop(k.columns[-1], axis=1).reset_index(drop=True)
                elif 'L' == x:
                    l = ACRAdata.groupby(['alphabets']).get_group('L')
                    l = l.drop(l.columns[-1], axis=1).reset_index(drop=True)
                elif 'M' == x:
                    m = ACRAdata.groupby(['alphabets']).get_group('M')
                    m = m.drop(m.columns[-1], axis=1).reset_index(drop=True)
                elif 'N' == x:
                    n = ACRAdata.groupby(['alphabets']).get_group('N')
                    n = n.drop(n.columns[-1], axis=1).reset_index(drop=True)
                elif 'O' == x:
                    o = ACRAdata.groupby(['alphabets']).get_group('O')
                    o = o.drop(o.columns[-1], axis=1).reset_index(drop=True)
                elif 'P' == x:
                    p = ACRAdata.groupby(['alphabets']).get_group('P')
                    p = p.drop(p.columns[-1], axis=1).reset_index(drop=True)
                elif 'Q' == x:
                    q = ACRAdata.groupby(['alphabets']).get_group('Q')
                    q = q.drop(q.columns[-1], axis=1).reset_index(drop=True)
                elif 'R' == x:
                    r = ACRAdata.groupby(['alphabets']).get_group('R')
                    r = r.drop(r.columns[-1], axis=1).reset_index(drop=True)
                elif 'S' == x:
                    s = ACRAdata.groupby(['alphabets']).get_group('S')
                    s = s.drop(s.columns[-1], axis=1).reset_index(drop=True)
                elif 'T' == x:
                    t = ACRAdata.groupby(['alphabets']).get_group('T')
                    t = t.drop(t.columns[-1], axis=1).reset_index(drop=True)
                elif 'U' == x:
                    u = ACRAdata.groupby(['alphabets']).get_group('U')
                    u = u.drop(u.columns[-1], axis=1).reset_index(drop=True)
                elif 'V' == x:
                    v = ACRAdata.groupby(['alphabets']).get_group('V')
                    v = v.drop(v.columns[-1], axis=1).reset_index(drop=True)
                elif 'W' == x:
                    w = ACRAdata.groupby(['alphabets']).get_group('W')
                    w = w.drop(w.columns[-1], axis=1).reset_index(drop=True)
                elif 'X' == x:
                    x = ACRAdata.groupby(['alphabets']).get_group('X')
                    x = x.drop(x.columns[-1], axis=1).reset_index(drop=True)
                elif 'Y' == x:
                    y = ACRAdata.groupby(['alphabets']).get_group('Y')
                    y = y.drop(y.columns[-1], axis=1).reset_index(drop=True)
                elif 'Z' == x:
                    z = ACRAdata.groupby(['alphabets']).get_group('Z')
                    z = z.drop(z.columns[-1], axis=1).reset_index(drop=True)
                elif '0' == x:
                    zero = ACRAdata.groupby(['alphabets']).get_group('0')
                    zero = zero.drop(zero.columns[-1], axis=1).reset_index(drop=True)
                elif '1' == x:
                    one = ACRAdata.groupby(['alphabets']).get_group('1')
                    one = one.drop(one.columns[-1], axis=1).reset_index(drop=True)
                elif '2' == x:
                    two = ACRAdata.groupby(['alphabets']).get_group('2')
                    two = two.drop(two.columns[-1], axis=1).reset_index(drop=True)
                elif '3' == x:
                    three = ACRAdata.groupby(['alphabets']).get_group('3')
                    three = three.drop(three.columns[-1], axis=1).reset_index(drop=True)
                elif '4' == x:
                    four = ACRAdata.groupby(['alphabets']).get_group('4')
                    four = four.drop(four.columns[-1], axis=1).reset_index(drop=True)
                elif '5' == x:
                    five = ACRAdata.groupby(['alphabets']).get_group('5')
                    five = five.drop(five.columns[-1], axis=1).reset_index(drop=True)
                elif '6' == x:
                    six = ACRAdata.groupby(['alphabets']).get_group('6')
                    six = six.drop(six.columns[-1], axis=1).reset_index(drop=True)
                elif '7' == x:
                    seven = ACRAdata.groupby(['alphabets']).get_group('7')
                    seven = seven.drop(seven.columns[-1], axis=1).reset_index(drop=True)
                elif '8' == x:
                    eight = ACRAdata.groupby(['alphabets']).get_group('8')
                    eight = eight.drop(eight.columns[-1], axis=1).reset_index(drop=True)
                elif '9' == x:
                    nine = ACRAdata.groupby(['alphabets']).get_group('9')
                    nine = nine.drop(nine.columns[-1], axis=1).reset_index(drop=True)
                elif '!' == x:
                    sym1 = ACRAdata.groupby(['alphabets']).get_group('!')
                    sym1 = sym1.drop(sym1.columns[-1], axis=1).reset_index(drop=True)
                elif '@' == x:
                    sym2 = ACRAdata.groupby(['alphabets']).get_group('@')
                    sym2 = sym2.drop(sym2.columns[-1], axis=1).reset_index(drop=True)
                elif '#' == x:
                    sym3 = ACRAdata.groupby(['alphabets']).get_group('#')
                    sym3 = sym3.drop(sym3.columns[-1], axis=1).reset_index(drop=True)
                elif '$' == x:
                    sym4 = ACRAdata.groupby(['alphabets']).get_group('$')
                    sym4 = sym4.drop(sym4.columns[-1], axis=1).reset_index(drop=True)
                elif '%' == x:
                    sym5 = ACRAdata.groupby(['alphabets']).get_group('%')
                    sym5 = sym5.drop(sym5.columns[-1], axis=1).reset_index(drop=True)
                elif '^' == x:
                    sym6 = ACRAdata.groupby(['alphabets']).get_group('^')
                    sym6 = sym6.drop(sym6.columns[-1], axis=1).reset_index(drop=True)
                elif '&' == x:
                    sym7 = ACRAdata.groupby(['alphabets']).get_group('&')
                    sym7 = sym7.drop(sym7.columns[-1], axis=1).reset_index(drop=True)
                elif '*' == x:
                    sym8 = ACRAdata.groupby(['alphabets']).get_group('*')
                    sym8 = sym8.drop(sym8.columns[-1], axis=1).reset_index(drop=True)
                elif '(' == x:
                    sym9 = ACRAdata.groupby(['alphabets']).get_group('(')
                    sym9 = sym9.drop(sym9.columns[-1], axis=1).reset_index(drop=True)
                elif ')' == x:
                    sym0 = ACRAdata.groupby(['alphabets']).get_group(')')
                    sym0 = sym0.drop(sym0.columns[-1], axis=1).reset_index(drop=True)

            return a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, zero, one, two, three, four, five, six, seven, eight, nine, sym0, sym1, sym2, sym3, sym4, sym5, sym6, sym7, sym8, sym9

        elif (useracraHeaders[0]) == 'entity_type':
            uniqueID = ACRAdata.entity_type.unique()
            uniqueID.sort()

            BN = ACRAdata.groupby(['entity_type']).get_group(uniqueID[0]).reset_index(drop=True)
            FC = ACRAdata.groupby(['entity_type']).get_group(uniqueID[1]).reset_index(drop=True)
            LC = ACRAdata.groupby(['entity_type']).get_group(uniqueID[2]).reset_index(drop=True)
            LL = ACRAdata.groupby(['entity_type']).get_group(uniqueID[3]).reset_index(drop=True)
            LP = ACRAdata.groupby(['entity_type']).get_group(uniqueID[4]).reset_index(drop=True)
            PF = ACRAdata.groupby(['entity_type']).get_group(uniqueID[5]).reset_index(drop=True)
            UF = ACRAdata.groupby(['entity_type']).get_group(uniqueID[6]).reset_index(drop=True)
            return BN, FC, LC, LL, LP, PF, UF

        elif (useracraHeaders[0]) == 'uen_status':
            # -- Group by two category--#
            uniqueID = ACRAdata.uen_status.unique()
            uniqueID.sort()

            D = ACRAdata.groupby(['uen_status']).get_group(uniqueID[0]).reset_index(drop=True)
            R = ACRAdata.groupby(['uen_status']).get_group(uniqueID[1]).reset_index(drop=True)

            return D, R

        elif (useracraHeaders[0]) == 'reg_postal_code':
            # -- Group by a range from 0 to 1,000,000 with a frequency of 100,000. E.g - 0 to 99,999 --#
            labels = ["{} - {}".format(i, i + 99999) for i in range(0, 1000000, 100000)]
            ACRAdata['group_postal_code'] = pd.cut(ACRAdata.reg_postal_code, range(0, 1100000, 100000), right=False, labels=labels)
            ACRAdata.set_index('group_postal_code', inplace=True)
            usergroup = ACRAdata.groupby('group_postal_code')

            gpc0 = get_group(usergroup, labels[0], ACRAdata.index)
            gpc1 = get_group(usergroup, labels[1], ACRAdata.index)
            gpc2 = get_group(usergroup, labels[2], ACRAdata.index)
            gpc3 = get_group(usergroup, labels[3], ACRAdata.index)
            gpc4 = get_group(usergroup, labels[4], ACRAdata.index)
            gpc5 = get_group(usergroup, labels[5], ACRAdata.index)
            gpc6 = get_group(usergroup, labels[6], ACRAdata.index)
            gpc7 = get_group(usergroup, labels[7], ACRAdata.index)
            gpc8 = get_group(usergroup, labels[8], ACRAdata.index)
            gpc9 = get_group(usergroup, labels[9], ACRAdata.index)

            return gpc0, gpc1, gpc2, gpc3, gpc4, gpc5, gpc6, gpc7, gpc8, gpc9

        elif (useracraHeaders[0]) == 'issuance_agency_id':
            # -- Group by one category--#
            uniqueID = ACRAdata.issuance_agency_id.unique()
            iai = ACRAdata.groupby(['issuance_agency_id']).get_group(uniqueID[0]).reset_index(drop=True)
            return iai

        elif (useracraHeaders[0]) == 'uen':
            # -- Group by first character--#
            # -- Same method as mention previously, scroll up to line 115 to view --#
            ACRAdata['starter'] = ACRAdata[useracraHeaders[0]].str[:1]
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
            zero, one, two, three, four, five, six, seven, eight, nine = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

            for x in ACRAdata['starter']:
                if 'A' == x:
                    a = ACRAdata.groupby(['starter']).get_group('A')
                    a = a.drop(a.columns[-1], axis=1).reset_index(drop=True)
                elif 'B' == x:
                    b = ACRAdata.groupby(['starter']).get_group('B')
                    b = b.drop(b.columns[-1], axis=1).reset_index(drop=True)
                elif 'C' == x:
                    c = ACRAdata.groupby(['starter']).get_group('C')
                    c = c.drop(c.columns[-1], axis=1).reset_index(drop=True)
                elif 'D' == x:
                    d = ACRAdata.groupby(['starter']).get_group('D')
                    d = d.drop(d.columns[-1], axis=1).reset_index(drop=True)
                elif 'E' == x:
                    e = ACRAdata.groupby(['starter']).get_group('E')
                    e = e.drop(e.columns[-1], axis=1).reset_index(drop=True)
                elif 'F' == x:
                    f = ACRAdata.groupby(['starter']).get_group('F')
                    f = f.drop(f.columns[-1], axis=1).reset_index(drop=True)
                elif 'G' == x:
                    g = ACRAdata.groupby(['starter']).get_group('G')
                    g = g.drop(g.columns[-1], axis=1).reset_index(drop=True)
                elif 'H' == x:
                    h = ACRAdata.groupby(['starter']).get_group('H')
                    h = h.drop(h.columns[-1], axis=1).reset_index(drop=True)
                elif 'I' == x:
                    i = ACRAdata.groupby(['starter']).get_group('I')
                    i = i.drop(i.columns[-1], axis=1).reset_index(drop=True)
                elif 'J' == x:
                    j = ACRAdata.groupby(['starter']).get_group('J')
                    j = j.drop(j.columns[-1], axis=1).reset_index(drop=True)
                elif 'K' == x:
                    k = ACRAdata.groupby(['starter']).get_group('K')
                    k = k.drop(k.columns[-1], axis=1).reset_index(drop=True)
                elif 'L' == x:
                    l = ACRAdata.groupby(['starter']).get_group('L')
                    l = l.drop(l.columns[-1], axis=1).reset_index(drop=True)
                elif 'M' == x:
                    m = ACRAdata.groupby(['starter']).get_group('M')
                    m = m.drop(m.columns[-1], axis=1).reset_index(drop=True)
                elif 'N' == x:
                    n = ACRAdata.groupby(['starter']).get_group('N')
                    n = n.drop(n.columns[-1], axis=1).reset_index(drop=True)
                elif 'O' == x:
                    o = ACRAdata.groupby(['starter']).get_group('O')
                    o = o.drop(o.columns[-1], axis=1).reset_index(drop=True)
                elif 'P' == x:
                    p = ACRAdata.groupby(['starter']).get_group('P')
                    p = p.drop(p.columns[-1], axis=1).reset_index(drop=True)
                elif 'Q' == x:
                    q = ACRAdata.groupby(['starter']).get_group('Q')
                    q = q.drop(q.columns[-1], axis=1).reset_index(drop=True)
                elif 'R' == x:
                    r = ACRAdata.groupby(['starter']).get_group('R')
                    r = r.drop(r.columns[-1], axis=1).reset_index(drop=True)
                elif 'S' == x:
                    s = ACRAdata.groupby(['starter']).get_group('S')
                    s = s.drop(s.columns[-1], axis=1).reset_index(drop=True)
                elif 'T' == x:
                    t = ACRAdata.groupby(['starter']).get_group('T')
                    t = t.drop(t.columns[-1], axis=1).reset_index(drop=True)
                elif 'U' == x:
                    u = ACRAdata.groupby(['starter']).get_group('U')
                    u = u.drop(u.columns[-1], axis=1).reset_index(drop=True)
                elif 'V' == x:
                    v = ACRAdata.groupby(['starter']).get_group('V')
                    v = v.drop(v.columns[-1], axis=1).reset_index(drop=True)
                elif 'W' == x:
                    w = ACRAdata.groupby(['starter']).get_group('W')
                    w = w.drop(w.columns[-1], axis=1).reset_index(drop=True)
                elif 'X' == x:
                    x = ACRAdata.groupby(['starter']).get_group('X')
                    x = x.drop(x.columns[-1], axis=1).reset_index(drop=True)
                elif 'Y' == x:
                    y = ACRAdata.groupby(['starter']).get_group('Y')
                    y = y.drop(y.columns[-1], axis=1).reset_index(drop=True)
                elif 'Z' == x:
                    z = ACRAdata.groupby(['starter']).get_group('Z')
                    z = z.drop(z.columns[-1], axis=1).reset_index(drop=True)
                elif '0' == x:
                    zero = ACRAdata.groupby(['starter']).get_group('0')
                    zero = zero.drop(zero.columns[-1], axis=1).reset_index(drop=True)
                elif '1' == x:
                    one = ACRAdata.groupby(['starter']).get_group('1')
                    one = one.drop(one.columns[-1], axis=1).reset_index(drop=True)
                elif '2' == x:
                    two = ACRAdata.groupby(['starter']).get_group('2')
                    two = two.drop(two.columns[-1], axis=1).reset_index(drop=True)
                elif '3' == x:
                    three = ACRAdata.groupby(['starter']).get_group('3')
                    three = three.drop(three.columns[-1], axis=1).reset_index(drop=True)
                elif '4' == x:
                    four = ACRAdata.groupby(['starter']).get_group('4')
                    four = four.drop(four.columns[-1], axis=1).reset_index(drop=True)
                elif '5' == x:
                    five = ACRAdata.groupby(['starter']).get_group('5')
                    five = five.drop(five.columns[-1], axis=1).reset_index(drop=True)
                elif '6' == x:
                    six = ACRAdata.groupby(['starter']).get_group('6')
                    six = six.drop(six.columns[-1], axis=1).reset_index(drop=True)
                elif '7' == x:
                    seven = ACRAdata.groupby(['starter']).get_group('7')
                    seven = seven.drop(seven.columns[-1], axis=1).reset_index(drop=True)
                elif '8' == x:
                    eight = ACRAdata.groupby(['starter']).get_group('8')
                    eight = eight.drop(eight.columns[-1], axis=1).reset_index(drop=True)
                elif '9' == x:
                    nine = ACRAdata.groupby(['starter']).get_group('9')
                    nine = nine.drop(nine.columns[-1], axis=1).reset_index(drop=True)

            return a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, zero, one, two, three, four, five, six, seven, eight, nine

    elif len(useruraHeaders) > 0:
        if (useruraHeaders[0]) == 'date_of_launch' or (useruraHeaders[0]) == 'date_of_tender_closing' or (useruraHeaders[0]) == 'date_of_award':
            # --Using pandas cut, the range will start from 1990 to 2020 with a frequency of 5 Years. Eg - 1990 to 1995--#
            bins_dt = pd.date_range(start='1/1/1990', end='1/1/2020', freq='5Ys')
            bins_str = bins_dt.astype(str).values
            labels = ['{} to {}'.format(bins_str[i - 1], bins_str[i]) for i in range(1, len(bins_str))]
            URAdata['group_year'] = pd.cut(URAdata[useruraHeaders[0]].astype(np.int64) // 10 ** 9,
                               bins = bins_dt.astype(np.int64) // 10 ** 9,
                               labels = labels)

            URAdata.set_index('group_year', inplace=True)
            usergroup = URAdata.groupby('group_year')

            dgp0 = usergroup.get_group(labels[0])
            dgp1 = usergroup.get_group(labels[1])
            dgp2 = usergroup.get_group(labels[2])
            dgp3 = usergroup.get_group(labels[3])
            dgp4 = usergroup.get_group(labels[4])
            dgp5 = usergroup.get_group(labels[5])

            return dgp0,dgp1,dgp2,dgp3,dgp4,dgp5

        elif (useruraHeaders[0]) == 'location' or (useruraHeaders[0]) == 'type_of_devt_allowed' or (useruraHeaders[0]) == 'successful_tenderer_name':
            # -- Group by first character--#
            # -- Same method as mention previously, scroll up to line 115 to view --#
            URAdata['alphabets'] = URAdata[useruraHeaders[0]].str[:1]
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}
            for x in URAdata['alphabets']:
                if 'A' == x:
                    a = URAdata.groupby(['alphabets']).get_group('A')
                    a = a.drop(a.columns[-1], axis=1).reset_index(drop=True)
                elif 'B' == x:
                    b = URAdata.groupby(['alphabets']).get_group('B')
                    b = b.drop(b.columns[-1], axis=1).reset_index(drop=True)
                elif 'C' == x:
                    c = URAdata.groupby(['alphabets']).get_group('C')
                    c = c.drop(c.columns[-1], axis=1).reset_index(drop=True)
                elif 'D' == x:
                    d = URAdata.groupby(['alphabets']).get_group('D')
                    d = d.drop(d.columns[-1], axis=1).reset_index(drop=True)
                elif 'E' == x:
                    e = URAdata.groupby(['alphabets']).get_group('E')
                    e = e.drop(e.columns[-1], axis=1).reset_index(drop=True)
                elif 'F' == x:
                    f = URAdata.groupby(['alphabets']).get_group('F')
                    f = f.drop(f.columns[-1], axis=1).reset_index(drop=True)
                elif 'G' == x:
                    g = URAdata.groupby(['alphabets']).get_group('G')
                    g = g.drop(g.columns[-1], axis=1).reset_index(drop=True)
                elif 'H' == x:
                    h = URAdata.groupby(['alphabets']).get_group('H')
                    h = h.drop(h.columns[-1], axis=1).reset_index(drop=True)
                elif 'I' == x:
                    i = URAdata.groupby(['alphabets']).get_group('I')
                    i = i.drop(i.columns[-1], axis=1).reset_index(drop=True)
                elif 'J' == x:
                    j = URAdata.groupby(['alphabets']).get_group('J')
                    j = j.drop(j.columns[-1], axis=1).reset_index(drop=True)
                elif 'K' == x:
                    k = URAdata.groupby(['alphabets']).get_group('K')
                    k = k.drop(k.columns[-1], axis=1).reset_index(drop=True)
                elif 'L' == x:
                    l = URAdata.groupby(['alphabets']).get_group('L')
                    l = l.drop(l.columns[-1], axis=1).reset_index(drop=True)
                elif 'M' == x:
                    m = URAdata.groupby(['alphabets']).get_group('M')
                    m = m.drop(m.columns[-1], axis=1).reset_index(drop=True)
                elif 'N' == x:
                    n = URAdata.groupby(['alphabets']).get_group('N')
                    n = n.drop(n.columns[-1], axis=1).reset_index(drop=True)
                elif 'O' == x:
                    o = URAdata.groupby(['alphabets']).get_group('O')
                    o = o.drop(o.columns[-1], axis=1).reset_index(drop=True)
                elif 'P' == x:
                    p = URAdata.groupby(['alphabets']).get_group('P')
                    p = p.drop(p.columns[-1], axis=1).reset_index(drop=True)
                elif 'Q' == x:
                    q = URAdata.groupby(['alphabets']).get_group('Q')
                    q = q.drop(q.columns[-1], axis=1).reset_index(drop=True)
                elif 'R' == x:
                    r = URAdata.groupby(['alphabets']).get_group('R')
                    r = r.drop(r.columns[-1], axis=1).reset_index(drop=True)
                elif 'S' == x:
                    s = URAdata.groupby(['alphabets']).get_group('S')
                    s = s.drop(s.columns[-1], axis=1).reset_index(drop=True)
                elif 'T' == x:
                    t = URAdata.groupby(['alphabets']).get_group('T')
                    t = t.drop(t.columns[-1], axis=1).reset_index(drop=True)
                elif 'U' == x:
                    u = URAdata.groupby(['alphabets']).get_group('U')
                    u = u.drop(u.columns[-1], axis=1).reset_index(drop=True)
                elif 'V' == x:
                    v = URAdata.groupby(['alphabets']).get_group('V')
                    v = v.drop(v.columns[-1], axis=1).reset_index(drop=True)
                elif 'W' == x:
                    w = URAdata.groupby(['alphabets']).get_group('W')
                    w = w.drop(w.columns[-1], axis=1).reset_index(drop=True)
                elif 'X' == x:
                    x = URAdata.groupby(['alphabets']).get_group('X')
                    x = x.drop(x.columns[-1], axis=1).reset_index(drop=True)
                elif 'Y' == x:
                    y = URAdata.groupby(['alphabets']).get_group('Y')
                    y = y.drop(y.columns[-1], axis=1).reset_index(drop=True)
                elif 'Z' == x:
                    z = URAdata.groupby(['alphabets']).get_group('Z')
                    z = z.drop(z.columns[-1], axis=1).reset_index(drop=True)

            return a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

        elif (useruraHeaders[0]) == 'planning_area':
            # -- Group by category, there are 39 predefined categories here--#
            # -- Step by step, 1) Extract all unique value from the column (planning_area). 2) Sort accordingly (A at the top, Z at the bottom). 3) Group via unique ID#
            # -- If user add a new planning area that is not in the predefined list, the data will not be reflected. This will be reflected as limitation in the report#
            uniqueID = URAdata.planning_area.unique()
            uniqueID.sort()
            print(uniqueID)
            amk = URAdata.groupby(['planning_area']).get_group(uniqueID[0]).reset_index(drop=True)
            bdk = URAdata.groupby(['planning_area']).get_group(uniqueID[1]).reset_index(drop=True)
            bis = URAdata.groupby(['planning_area']).get_group(uniqueID[2]).reset_index(drop=True)
            bkb = URAdata.groupby(['planning_area']).get_group(uniqueID[3]).reset_index(drop=True)
            bkm = URAdata.groupby(['planning_area']).get_group(uniqueID[4]).reset_index(drop=True)
            bkp = URAdata.groupby(['planning_area']).get_group(uniqueID[5]).reset_index(drop=True)
            bkt = URAdata.groupby(['planning_area']).get_group(uniqueID[6]).reset_index(drop=True)
            chi = URAdata.groupby(['planning_area']).get_group(uniqueID[7]).reset_index(drop=True)
            cck = URAdata.groupby(['planning_area']).get_group(uniqueID[8]).reset_index(drop=True)
            cmt = URAdata.groupby(['planning_area']).get_group(uniqueID[9]).reset_index(drop=True)
            dtc = URAdata.groupby(['planning_area']).get_group(uniqueID[10]).reset_index(drop=True)
            gel = URAdata.groupby(['planning_area']).get_group(uniqueID[11]).reset_index(drop=True)
            hog = URAdata.groupby(['planning_area']).get_group(uniqueID[12]).reset_index(drop=True)
            jue = URAdata.groupby(['planning_area']).get_group(uniqueID[13]).reset_index(drop=True)
            juw = URAdata.groupby(['planning_area']).get_group(uniqueID[14]).reset_index(drop=True)
            kal = URAdata.groupby(['planning_area']).get_group(uniqueID[15]).reset_index(drop=True)
            mrp = URAdata.groupby(['planning_area']).get_group(uniqueID[16]).reset_index(drop=True)
            mus = URAdata.groupby(['planning_area']).get_group(uniqueID[17]).reset_index(drop=True)
            new = URAdata.groupby(['planning_area']).get_group(uniqueID[18]).reset_index(drop=True)
            nov = URAdata.groupby(['planning_area']).get_group(uniqueID[19]).reset_index(drop=True)
            orc = URAdata.groupby(['planning_area']).get_group(uniqueID[20]).reset_index(drop=True)
            otr = URAdata.groupby(['planning_area']).get_group(uniqueID[21]).reset_index(drop=True)
            psr = URAdata.groupby(['planning_area']).get_group(uniqueID[22]).reset_index(drop=True)
            pyl = URAdata.groupby(['planning_area']).get_group(uniqueID[23]).reset_index(drop=True)
            pgg = URAdata.groupby(['planning_area']).get_group(uniqueID[24]).reset_index(drop=True)
            rvv = URAdata.groupby(['planning_area']).get_group(uniqueID[25]).reset_index(drop=True)
            roc = URAdata.groupby(['planning_area']).get_group(uniqueID[26]).reset_index(drop=True)
            sbw = URAdata.groupby(['planning_area']).get_group(uniqueID[27]).reset_index(drop=True)
            sgk = URAdata.groupby(['planning_area']).get_group(uniqueID[28]).reset_index(drop=True)
            srg = URAdata.groupby(['planning_area']).get_group(uniqueID[29]).reset_index(drop=True)
            sgr = URAdata.groupby(['planning_area']).get_group(uniqueID[30]).reset_index(drop=True)
            sti = URAdata.groupby(['planning_area']).get_group(uniqueID[31]).reset_index(drop=True)
            tpi = URAdata.groupby(['planning_area']).get_group(uniqueID[32]).reset_index(drop=True)
            tgl = URAdata.groupby(['planning_area']).get_group(uniqueID[33]).reset_index(drop=True)
            tpy = URAdata.groupby(['planning_area']).get_group(uniqueID[34]).reset_index(drop=True)
            tua = URAdata.groupby(['planning_area']).get_group(uniqueID[35]).reset_index(drop=True)
            wwc = URAdata.groupby(['planning_area']).get_group(uniqueID[36]).reset_index(drop=True)
            wdl = URAdata.groupby(['planning_area']).get_group(uniqueID[37]).reset_index(drop=True)
            yis = URAdata.groupby(['planning_area']).get_group(uniqueID[38]).reset_index(drop=True)

            return amk, bdk, bis, bkb, bkm, bkp, bkt, chi, cck, cmt, dtc, gel, hog, jue, juw, kal, mrp, mus, new, nov, orc, otr, psr, pyl, pgg, rvv, roc, sbw, sgk, srg, sgr, sti, tpi, tgl, tpy, tua, wwc, wdl, yis

        elif (useruraHeaders[0]) == 'type_of_devt_code':
            # -- Group by category, there are 13 predefined categories here--#
            # -- Refer to line 542 for details --#
            uniqueID = URAdata.type_of_devt_code.unique()
            uniqueID.sort()
            commerical = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[0]).reset_index(drop=True)
            commercial_and_residential = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[1]).reset_index(drop=True)
            driving_centre = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[2]).reset_index(drop=True)
            entertainment = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[3]).reset_index(drop=True)
            hospital = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[4]).reset_index(drop=True)
            hotel = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[5]).reset_index(drop=True)
            industrial = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[6]).reset_index(drop=True)
            industrial_white = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[7]).reset_index(drop=True)
            office = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[8]).reset_index(drop=True)
            others = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[9]).reset_index(drop=True)
            recreation = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[10]).reset_index(drop=True)
            residential_non_landed = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[11]).reset_index(drop=True)
            white_site = URAdata.groupby(['type_of_devt_code']).get_group(uniqueID[12]).reset_index(drop=True)

            return commerical, commercial_and_residential, driving_centre, entertainment, hospital, hotel, industrial, industrial_white, office, others, recreation, residential_non_landed, white_site

        elif (useruraHeaders[0]) == 'no_of_bids':
            # -- A range from 0 to 20 with a frequency of 5. E.g - 0 to 5--#
            labels = ["{} - {}".format(i, i + 5) for i in range(0, 20, 5)]
            URAdata['group_bids'] = pd.cut(URAdata.no_of_bids, range(0, 25, 5), right=False, labels=labels)
            URAdata.set_index('group_bids', inplace=True)
            usergroup = URAdata.groupby('group_bids')
            gb0 = get_group(usergroup, labels[0], URAdata.index)
            gb1 = get_group(usergroup, labels[1], URAdata.index)
            gb2 = get_group(usergroup, labels[2], URAdata.index)
            gb3 = get_group(usergroup, labels[3], URAdata.index)

            print(gb0, gb1, gb3)

            return gb0, gb1, gb2, gb3

        elif (useruraHeaders[0]) == 'lease':
            # -- A range from 0 to 120 with a frequency of 30. E.g - 0 to 29--#
            labels = ["{0} - {1}".format(i, i + 29) for i in range(0, 120, 30)]
            URAdata['group_lease'] = pd.cut(URAdata.lease, range(0, 150, 30), right=False, labels=labels)
            URAdata.set_index('group_lease', inplace=True)
            usergroup = URAdata.groupby('group_lease')

            gl0 = get_group(usergroup, labels[0], URAdata.index)
            gl1 = get_group(usergroup, labels[1], URAdata.index)
            gl2 = get_group(usergroup, labels[2], URAdata.index)
            gl3 = get_group(usergroup, labels[3], URAdata.index)
            print(gl1, gl2, gl3)
            return gl0, gl1, gl2, gl3

        elif (useruraHeaders[0]) == 'gross_plot_ratio':
            # -- A range from 0 to 5 with a frequency of 1. E.g - 0 < x < 1--#
            labels = ["{0} < X < {1}".format(i, i+1) for i in range(0, 5, 1)]
            URAdata['group_gross_plot_ratio'] = pd.cut(URAdata.gross_plot_ratio, range(0, 6, 1), right=False, labels=labels)
            URAdata.set_index('group_gross_plot_ratio', inplace=True)
            usergroup = URAdata.groupby('group_gross_plot_ratio')

            ggpr0 = get_group(usergroup, labels[0], URAdata.index)
            ggpr1 = get_group(usergroup, labels[1], URAdata.index)
            ggpr2 = get_group(usergroup, labels[2], URAdata.index)
            ggpr3 = get_group(usergroup, labels[3], URAdata.index)
            return ggpr0, ggpr1, ggpr2, ggpr3

        elif (useruraHeaders[0]) == 'site_area':
            # -- A range from 0 to 200,000 with a frequency of 40,000. E.g - 0 to 39,999--#
            labels = ["{0} - {1}".format(i, i + 39999) for i in range(0, 200000, 40000)]
            URAdata['group_site_area'] = pd.cut(URAdata.site_area, range(0, 220000, 40000), right=False, labels=labels)
            usergroup = URAdata.groupby('group_site_area')
            URAdata.set_index('group_site_area', inplace=True)

            gsa0 = get_group(usergroup, labels[0], URAdata.index)
            gsa1 = get_group(usergroup, labels[1], URAdata.index)
            gsa2 = get_group(usergroup, labels[2], URAdata.index)
            gsa3 = get_group(usergroup, labels[3], URAdata.index)
            gsa4 = get_group(usergroup, labels[4], URAdata.index)

            return gsa0, gsa1, gsa2, gsa3, gsa4

        elif (useruraHeaders[0]) == 'gross_floor_area':
            # -- A range from 0 to 500,000 with a frequency of 100,000. E.g - 0 to 99,999--#
            labels = ["{0} - {1}".format(i, i + 99999) for i in range(0, 500000, 100000)]
            URAdata['group_gross_floor_area'] = pd.cut(URAdata.gross_floor_area, range(0, 600000, 100000), right=False, labels=labels)
            usergroup = URAdata.groupby('group_gross_floor_area')
            URAdata.set_index('group_gross_floor_area', inplace=True)

            gfa0 = get_group(usergroup, labels[0], URAdata.index)
            gfa1 = get_group(usergroup, labels[1], URAdata.index)
            gfa2 = get_group(usergroup, labels[2], URAdata.index)
            gfa3 = get_group(usergroup, labels[3], URAdata.index)
            gfa4 = get_group(usergroup, labels[4], URAdata.index)

            return gfa0, gfa1, gfa2, gfa3, gfa4

        elif (useruraHeaders[0]) == 'successful_tender_price':
            # -- A range from 0 to 2,500,000,000 with a frequency of 500,000,000. E.g - 0 to 499,999,999--#
            labels = ["{0} - {1}".format(i, i + 499999999) for i in range(0, 2500000000, 500000000)]
            URAdata['group_successful_tender_price'] = pd.cut(URAdata.successful_tender_price, range(0, 3000000000, 500000000), right=False, labels=labels)
            usergroup = URAdata.groupby('group_successful_tender_price')
            URAdata.set_index('group_successful_tender_price', inplace=True)
            gst0 = get_group(usergroup, labels[0], URAdata.index)
            gst1 = get_group(usergroup, labels[1], URAdata.index)
            gst2 = get_group(usergroup, labels[2], URAdata.index)
            gst3 = get_group(usergroup, labels[3], URAdata.index)
            gst4 = get_group(usergroup, labels[4], URAdata.index)

            return gst0, gst1, gst2, gst3, gst4

        elif (useruraHeaders[0]) == 'psm_per_gpr_or_gfa':
            # -- A range from 0 to 18,000 with a frequency of 3,000. E.g - 0 to 18,000--#
            labels = ["{0} - {1}".format(i, i + 2999) for i in range(0, 18000, 3000)]
            URAdata['group_psm_per_gpr_or_gfa'] = pd.cut(URAdata.psm_per_gpr_or_gfa, range(0, 21000, 3000), right=False, labels=labels)
            usergroup = URAdata.groupby('group_psm_per_gpr_or_gfa')
            URAdata.set_index('group_psm_per_gpr_or_gfa', inplace=True)

            gps0 = get_group(usergroup, labels[0], URAdata.index)
            gps1 = get_group(usergroup, labels[1], URAdata.index)
            gps2 = get_group(usergroup, labels[2], URAdata.index)
            gps3 = get_group(usergroup, labels[3], URAdata.index)
            gps4 = get_group(usergroup, labels[4], URAdata.index)
            gps5 = get_group(usergroup, labels[5], URAdata.index)

            return gps0, gps1, gps2, gps3, gps4, gps5


# --SELECT AND SORT--#
def generalSelectsort(sepContent,data1):
    """

    :param sepContent:
    :param data1:
    :return:
    """
    # default 2 empty dataframe
    URAdata = pd.DataFrame()
    ACRAdata = pd.DataFrame()

    # only 1 data file#
    if data_cleaning.clean_ura(data1).empty == False:
        URAdata = data_cleaning.clean_ura(data1)
    elif data_cleaning.clean_acra(data1).empty == False:
        ACRAdata = data_cleaning.clean_acra(data1)
    if ACRAdata.empty == True and URAdata.empty == True:
        sys.exit(messagebox.showerror("Error", "Both files are neither URA nor ACRA"))

    if URAdata.empty == False:
        URAdata['date_of_award'] = pd.to_datetime(URAdata['date_of_award'], format='%Y-%m-%d')
        URAdata['date_of_tender_closing'] = pd.to_datetime(URAdata['date_of_tender_closing'], format='%Y-%m-%d')
        URAdata['date_of_launch'] = pd.to_datetime(URAdata['date_of_launch'], format='%Y-%m-%d')
        URAdata = URAdata.replace('na', 0)
        URAdata["gross_floor_area"] = URAdata["gross_floor_area"].astype('float64')
        URAdata["lease"] = URAdata["lease"].astype('int64')
        URAdata["site_area"] = URAdata["site_area"].astype('float64')
        URAdata["gross_plot_ratio"] = URAdata["gross_plot_ratio"].astype('float64')
        URAdata["no_of_bids"] = URAdata["no_of_bids"].astype('float64')
        URAdata["successful_tender_price"] = URAdata["successful_tender_price"].astype('float64')
        URAdata["psm_per_gpr_or_gfa"] = URAdata["psm_per_gpr_or_gfa"].astype('float64')
    if ACRAdata.empty == False:
        ACRAdata = ACRAdata.replace('na', 0)
        ACRAdata['uen_issue_date'] = pd.to_datetime(ACRAdata['uen_issue_date'], format='%d/%m/%Y')
        ACRAdata["reg_postal_code"] = ACRAdata["reg_postal_code"].astype('int64')
        ACRAdata['entity_name'] = ACRAdata['entity_name'].astype(str)

    # --Extract all columns headers and place them in their respective variables--#
    useracraHeaders, useruraHeaders = [], []
    URAHeader = list(URAdata.columns.values[0:])
    ACRAHeader = list(ACRAdata.columns.values[0:])

    # -- This check for import text, if a text in import.txt matches with a column header, it will append--#
    for i in sepContent:
        if i in URAHeader:
            useruraHeaders.append(i)
        elif i in ACRAHeader:
            useracraHeaders.append(i)

    # -- This if/else method will extract the headers accordingly--#
    if len(useruraHeaders) > 0 and URAdata.empty == False:
        if len(useruraHeaders) == 1:
            newSorted = URAdata.reindex([useruraHeaders[0]], axis='columns')
        elif len(useruraHeaders) == 2:
            newSorted = URAdata.reindex([useruraHeaders[0], useruraHeaders[1]], axis='columns')
        elif len(useruraHeaders) == 3:
            newSorted = URAdata.reindex([useruraHeaders[0], useruraHeaders[1], useruraHeaders[2]], axis='columns')
        elif len(useruraHeaders) == 4:
            newSorted = URAdata.reindex([useruraHeaders[0], useruraHeaders[1], useruraHeaders[2], useruraHeaders[3]], axis='columns')
        else:
            sys.exit(messagebox.showerror("Error", "Headers selected must be less than 5"))
    if len(useracraHeaders) > 0 and ACRAdata.empty == False:
        if len(useracraHeaders) == 1:
            newSorted = ACRAdata.reindex([useracraHeaders[0]], axis='columns')
        elif len(useracraHeaders) == 2:
            newSorted = ACRAdata.reindex([useracraHeaders[0], useracraHeaders[1]], axis='columns')
        elif len(useracraHeaders) == 3:
            newSorted = ACRAdata.reindex([useracraHeaders[0], useracraHeaders[1], useracraHeaders[2]], axis='columns')
        elif len(useracraHeaders) == 4:
            newSorted = ACRAdata.reindex([useracraHeaders[0], useracraHeaders[1], useracraHeaders[2], useracraHeaders[3]], axis='columns')
        else:
            sys.exit(messagebox.showerror("Error", "Headers selected must be less than 5"))

    # -- If normal sorting is deteced, this will run --#
    for i in sepContent:
        if i == 'sort' and len(useruraHeaders)>0:
            newSorted = newSorted.sort_values(by=useruraHeaders[0], ascending=True).reset_index(drop=True)

        elif i == 'sort' and len(useracraHeaders)>0:
            newSorted = newSorted.sort_values(by=useracraHeaders[0], ascending=True).reset_index(drop=True)


    # -- If descending is deteced, this will run --#
    for i in sepContent:
        if i == 'descending' and len(useruraHeaders)>0:
            newSorted = newSorted.sort_values(by=useruraHeaders[0], ascending=False).reset_index(drop=True)

        elif i == 'descending' and len(useracraHeaders)>0:
            newSorted = newSorted.sort_values(by=useracraHeaders[0], ascending=False).reset_index(drop=True)

    #-- Sort accordingly to the number of rows with the last row of arithmetic --#
    for i in sepContent:
        if i.isnumeric() == True and len(useruraHeaders)>0:
            i = int(i)
            newSorted = (newSorted.head(n=i))
        elif i.isnumeric() == True and len(useracraHeaders) > 0:
            i = int(i)
            newSorted = (newSorted.head(n=i))

    #-- If an arithmetic is detected in the import.txt, this function wil run--#
    for i in sepContent:
        if i == 'sum':
            newSorted.loc['Total Sum'] = pd.Series(newSorted.sum(numeric_only=True))
            return newSorted
        if i =='average':
            newSorted.loc['Total Average'] = pd.Series(newSorted.mean(numeric_only=True))
            return newSorted

    return newSorted


def parsecsv():
    """
    :return:
    """
    data1 = pd.read_csv("ACRA.csv", dayfirst=True, encoding="iso-8859-1", parse_dates=True)
    return data1


# --TAKE THE IMPORT TEXT AND SPLIT--#
def selection(data1, user_input_list):
    """
    :param data1:
    :param user_input_list:
    :return:
    """
    sepContent=[]
    content = user_input_list
    content = [x.strip() for x in content]
    for element in content:
        sepContent += element.split(', ')

    for i in sepContent:
        if i == 'group':
            return generalGroupby(sepContent, data1)
        if i == 'selection':
            return generalSelectsort(sepContent, data1)

    sys.exit(messagebox.showerror("Error", "Both files are neither URA nor ACRA"))




"""Please decide whether to keep these comments."""
# #Song xuan csv will become data 1
# data1=parsecsv()
#
# #After data 1 parses into this function, it will be sorted out if its group by or select&Sort. If its neither, there will be an error message
# fml=selection(data1)
# print(fml)


#-- Order of function --#
# 1) parsecsv()
# 2) selection(data1) - if data is neither group or select&sort, show error
#   if selection(data1) = groupby, go 3.1)
#   if selection(data1) = selected&sort, go 3.2)
# 3.1) generalGroupby(sepContent,data1) - return dataframe based on predefined group
# 3.2) generalSelectsort(sepContent,data1) - return dataframe based on requirement

#NOTE
#After groupby function, some dataframe will return empty because some data does no exist in the predefined range.