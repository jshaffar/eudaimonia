import util
import pandas as pd
import numpy as np
import datetime

def get_total(df=None, deltas=None, start_date=None, end_date=None):
    if df is None and deltas is None:
        print('Error: either df or deltas needs to be specified in get_total()')
    if deltas is None:
        deltas = list(filter(lambda v: not np.isnan(v), list(util.get_parameter(df, 'delta', start_date=start_date, end_date=end_date))))
    sum = 0
    totals = np.zeros(len(deltas))
    for i in range(0, len(deltas)):
        totals[i] = sum + deltas[i]
        sum += deltas[i]
    return totals


def get_frequencies(df, name=None, start_date=None, end_date=None):
    col = util.get_parameter(df, name, start_date=start_date, end_date=end_date)
    values = {}
    for value in col:
        values[value] = values[value] + 1 if value in values else 1
    return values

def get_weekdays_dataframe(df, start_date=None, end_date=None, additional_columns=[]):
    col = util.get_parameter(df, 'date', start_date=start_date, end_date=end_date)
    days = list(map(lambda v: (v, datetime.datetime(month=int(v.split('/')[0]), day=int(v.split('/')[1]), year=int(v.split('/')[2]))), col))
    #days_of_week = list(map(lambda v: (v[0], v[1], v[1].weekday(), df.loc(lambda df: df['date'] == v[0])), days))
    days_of_week = list(map(lambda v: (v[0], v[1], v[1].weekday()), days))
    #print(list(map(lambda v: np.empty(0), list(range(0, 7)))))
    #print(pd.DataFrame(rows=list(map(lambda v: np.empty(0), list(range(0, 7))))))
    #map(lambda v: init_data[v] = np.empty(0), list(range(0, 7)))
    data = {}
    for i in range(0, 7):
        data[i] = np.empty(0)
    
    new_df = pd.DataFrame(data)

    dict_to_convert = {}
    index = 0
    for day in days_of_week:
        row = int(index / 7)
        day_index = index % 7
        if row >= len(dict_to_convert):
            dict_to_convert[row] = [()] * 7
        if row >= 0 and day != 0:
            dict_to_convert[row][day_index] = (day[0], day[1], day[2], util.get_row(df, 'date', day[0]))
        index += 1
    list_to_convert = list(map(lambda v: dict_to_convert[v],list(dict_to_convert)))

    new_df = pd.DataFrame(list_to_convert)
    return new_df
