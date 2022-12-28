import pandas as pd
from matplotlib import pyplot as plt
import datetime
import numpy as np
import calc
import util
import json

def trad_graph_provided_xy(x, y, name, dpi=1200, animate=False):
    plt.plot(x, y)
    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')

# specifically designed for days of week initially but may need to expand
def multi_graph_provided_xy(x_data, y_data, data_labels, name, dpi=1200, animate=False, colors=None, alpha=.7):
    plt.xticks(rotation=90)
    for i in range(0, len(x_data)):
        plt.plot(x_data[i], y_data[i], label=data_labels[i], color=colors[i] if colors is not None else None, alpha=alpha)
    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')

def split_graph(df, trait, trait_to_split, name, date=0, dpi=1200, animate=False, colors_file=None, alpha=.7):
    values = sorted(list(set(df[trait_to_split])))
    data = [df.loc[df[trait_to_split] == value] for value in values]

    for i in range(0, len(data)):
        if trait not in data[i]:
            data[i] = util.add_parameter(data[i], trait=trait)
    
    colors_dict = json.load(open(colors_file)) if colors_file is not None else {}

    plt.xticks(rotation=90)
    for i in range(0, len(data)):
        label = values[i]
        data_section = data[i]
        #TODO implement random color
        plt.plot(data_section['day'], data_section[trait],label=label, alpha=alpha, color=colors_dict[label.lower()] if label.lower() in colors_dict else None)
    plt.legend()
    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')



def graph_delta_by_time(df, start_date=None, end_date=None, animate=False):
    dates = list(util.get_column(df, 'date', start_date=start_date, end_date=end_date))
    deltas = list(util.get_column(df, 'delta', start_date=start_date, end_date=end_date))
    trad_graph_provided_xy(dates, deltas, 'deltas', animate=False)

def graph_total_by_time(df, start_date=None, end_date=None, animate=False):
    totals = list(calc.get_total(df))
    dates = list(util.get_column(df, 'date', start_date=start_date, end_date=end_date))[:len(totals)]
    trad_graph_provided_xy(dates, totals, 'totals', animate=False)

def graph_frequency_by_time(df, name, start_date=None, end_date=None, animate=False):

    freq = calc.get_frequencies(df, name=name, start_date=start_date, end_date=end_date)
    sorted_freqs = sorted(freq.items())
    x, y = zip(*sorted_freqs)
    trad_graph_provided_xy(x, y, f'freq_{name}', animate=False)


def graph_value_of_each_value(df, start_date=None, end_date=None, animate=False):
    freq = calc.get_frequencies(df, name='delta', start_date=start_date, end_date=end_date)
    sorted_freqs = sorted(freq.items())
    sorted_values = list(map(lambda v: (v[0], v[0] * v[1]), sorted_freqs))
    x, y = zip(*sorted_values)
    trad_graph_provided_xy(x, y, 'value_by_value', animate=False)

def graph_weekdays(df, trait, start_date=None, end_date=None, colors_file='Config/default.json'):
    df = util.filter_dataframe(df, start_date=start_date, end_date=end_date)
    df = util.add_parameter(df, 'weekday')
    split_graph(df=df, trait=trait, trait_to_split='weekday', name=f'days_of_week_{trait}', colors_file=colors_file)

filename = 'pursuit.csv'
df = util.get_df_from_csv(filename)
graph_weekdays(df, 'total', start_date=datetime.datetime(year=2022, month=1, day=1))
#graph_weekdays(df, 'total')
#graph_total_by_time(df)
#graph_delta_by_time(df, start_date=datetime.datetime(year=2021, month=2, day=3), end_date=datetime.datetime(year=2021, month=3, day=3))
#graph_frequency_by_time(df, 'delta')
#graph_frequency_by_time(df, 'total')
#graph_value_of_each_value(df)

