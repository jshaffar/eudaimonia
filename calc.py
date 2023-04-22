import util
import pandas as pd
import numpy as np
import datetime
import argparse
import math

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


def get_condition(condition_name):
    def positive_function(num, params):
        return num > 0
    def negative_function(num, params):
        return num < 0
    def non_negative_function(num, params):
        return num >= 0
    def non_positive_function(num, params):
        return num <= 0
    def consecutive_function(num, params):
        if 'target' not in params:
            raise Exception('consecutive numbers function must have target num')
        target = params['target']
        if isinstance(num[0], int) or isinstance(num[0], float):
            target = int(target)
        return num == target
    def exists(num, params):
        # nan is not equal to nan so this trick works https://stackoverflow.com/a/19322739
        return num == num
        #return num.equals(math.nan)
    def not_exists(num, params):
        return num != num

    function_map = {
        'positive':positive_function,
        'negative':negative_function,
        'non_negative':non_negative_function,
        'non_positive':non_positive_function,
        'consecutive':consecutive_function,
        'exists':exists,
        'not_exists':not_exists
    }
    return function_map[condition_name]


def calc_streak(df, attribute='Delta', start_date=None, end_date=None, condition='positive', params={}):
    df = util.filter_dataframe(df, start_date=start_date, end_date=end_date)
    function = get_condition(condition)
    positive = function(df[attribute], params)
    cum_sum = positive.cumsum()
    # https://stackoverflow.com/a/44104130
    streaks_df = cum_sum - cum_sum.mask(positive).ffill().fillna(0).astype(int)
    max_streak_idx = streaks_df.idxmax()
    max_streak_value = streaks_df[max_streak_idx]
    max_streak_start = df.iloc[max_streak_idx - max_streak_value + 1]['Date']
    max_streak_end = df.iloc[max_streak_idx]['Date']
    result = f'The most consecutive rows with the condition {condition} is {max_streak_value}. This was from {max_streak_start} to {max_streak_end}'
    print(result)

    # we want 673-687

if __name__ == "__main__":
    default_action = 'streak'
    default_condition = 'positive'
    default_attribute = 'Delta'
    filename = 'pursuit.csv'
    df = util.get_df_from_csv(filename)
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date', '-sd')
    parser.add_argument('--end_date', '-ed', default=None)
    parser.add_argument('--action', '-a', default=default_action)
    parser.add_argument('--attribute', '-at', default=default_attribute)
    parser.add_argument('--condition', '-c', default=default_condition)
    parser.add_argument('--target', '-t', default=None)
    parser.add_argument('--on_weekday', '-ow', default="False")
    args = parser.parse_args()
    def parse_date(date_str):
        date_split = list(map(lambda v: int(v), date_str.split('/')))
        date = datetime.datetime(year=date_split[2], month=date_split[0], day=date_split[1])
        return date
    start_date = parse_date(args.start_date) if args.start_date is not None else None
    end_date = parse_date(args.end_date) if args.end_date is not None else None
    action = args.action
    condition = args.condition
    attribute = args.attribute
    params = {}
    if args.target is not None:
        params['target'] = args.target
    on_weekday = args.on_weekday.lower() in ["t", "true"]
    if action is not None and action in ["streak"]:
        calc_streak(df, start_date=start_date, end_date=end_date, condition=condition, params=params, attribute=attribute)
    else:
        raise Exception(f'Error: action {action} not currently supported')
    