import util
import pandas as pd
import numpy as np
import datetime

def get_total(df=None, deltas=None, start_date=None, end_date=None):
    if df is None and deltas is None:
        print('Error: either df or deltas needs to be specified in get_total()')
    if deltas is None:
        deltas = list(filter(lambda v: not np.isnan(v), list(util.get_parameter(df, 'Delta', start_date=start_date, end_date=end_date))))
    sum = 0
    totals = np.zeros(len(deltas))
    for i in range(0, len(deltas)):
        totals[i] = sum + deltas[i]
        sum += deltas[i]
    return totals

def get_weekday(df, start_date=None, end_date=None):
    def get_day_of_week(n):
        day_mapping = {0:'Monday',1:'Tuesday',2:'Wednesday',3: 'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
        return day_mapping[n]
    df = df.assign(weekday=lambda df: df['day'].apply(datetime.datetime.weekday).apply(get_day_of_week))
    return df

def get_day_from_text(date_text):
    parsed_date_text = list(map(int, date_text.split('-')))
    return datetime.datetime(year=parsed_date_text[0], month=parsed_date_text[1], day=parsed_date_text[2])


def get_day(df, start_date=None, end_date=None):
    df = df.assign(day=lambda v: v['Date'].apply(get_day_from_text))
    return df


def get_frequencies(df, name=None, start_date=None, end_date=None):
    col = util.get_parameter(df, name, start_date=start_date, end_date=end_date)
    values = {}
    for value in col:
        values[value] = values[value] + 1 if value in values else 1
    return values

def get_weekdays_dataframe(df, start_date=None, end_date=None):
    col = util.get_parameter(df, 'Date', start_date=start_date, end_date=end_date)
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
    index = row = 0
    for day in days_of_week:
        row = int(index / 7)
        day_index = index % 7
        if row >= len(dict_to_convert):
            dict_to_convert[row] = [None] * 7
        if row >= 0 and day != 0:
            dict_to_convert[row][day_index] = (day[1], util.get_row(df, 'Date', day[0]))
        index += 1
    dict_to_convert[row] = list(filter(lambda v: v is not None, dict_to_convert[row]))
    list_to_convert = list(map(lambda v: dict_to_convert[v],list(dict_to_convert)))
    new_df = pd.DataFrame(list_to_convert)
    return new_df

