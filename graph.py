import pandas as pd
from matplotlib import pyplot as plt
import datetime

import calc
import util

def trad_graph(x, y, name, dpi=1200, animate=False):
    plt.plot(x, y)
    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')

# specifically designed for days of week initially but may need to expand
def multi_graph(x_data, y_data, data_labels, name, dpi=1200, animate=False, colors=None, alpha=.7):
    plt.xticks(rotation=90)
    for i in range(0, len(x_data)):
        plt.plot(x_data[i], y_data[i], label=data_labels[i], color=colors[i] if colors is not None else None, alpha=alpha)
    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')


def graph_delta_by_time(df, start_date=None, end_date=None, animate=False):
    dates = list(util.get_column(df, 'date', start_date=start_date, end_date=end_date))
    deltas = list(util.get_column(df, 'delta', start_date=start_date, end_date=end_date))
    trad_graph(dates, deltas, 'deltas', animate=False)

def graph_total_by_time(df, start_date=None, end_date=None, animate=False):
    totals = list(calc.get_total(df))
    dates = list(util.get_column(df, 'date', start_date=start_date, end_date=end_date))[:len(totals)]
    trad_graph(dates, totals, 'totals', animate=False)

def graph_frequency_by_time(df, name, start_date=None, end_date=None, animate=False):

    freq = calc.get_frequencies(df, name=name, start_date=start_date, end_date=end_date)
    sorted_freqs = sorted(freq.items())
    x, y = zip(*sorted_freqs)
    trad_graph(x, y, f'freq_{name}', animate=False)


def graph_value_of_each_value(df, start_date=None, end_date=None, animate=False):
    freq = calc.get_frequencies(df, name='delta', start_date=start_date, end_date=end_date)
    sorted_freqs = sorted(freq.items())
    sorted_values = list(map(lambda v: (v[0], v[0] * v[1]), sorted_freqs))
    x, y = zip(*sorted_values)
    trad_graph(x, y, 'value_by_value', animate=False)

def graph_weekdays(df, trait, start_date=None, end_date=None, colors=['black', 'green', 'brown', 'purple', 'red', 'orange', 'blue']):
    df = util.filter_dataframe(df)
    dates = list(util.get_parameter(df, 'date', start_date=start_date, end_date=end_date))
    additional_columns = [trait] if trait not in df.columns else []
    if len(additional_columns) > 0:
        for trait in additional_columns: util.add_parameter(df, trait='total')
    new_df = calc.get_weekdays_dataframe(df, start_date=start_date, end_date=end_date, additional_columns=additional_columns)
    x_data = [list(map(lambda v: v[1], list(new_df[i].loc[new_df[i] != ()]))) for i in range(0, 7)]
    y_data = [list(map(lambda v: v[3][trait], list(new_df[i].loc[new_df[i] != ()]))) for i in range(0, 7)]

    data_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    multi_graph(x_data=x_data, y_data=y_data, data_labels=data_labels, name=f'days_of_week_{trait}', colors=colors)

filename = 'pursuit.csv'
df = pd.read_csv(filename)
graph_weekdays(df, 'total')
#graph_weekdays(df, 'total')
#graph_total_by_time(df)
#graph_delta_by_time(df, start_date=datetime.datetime(year=2021, month=2, day=3), end_date=datetime.datetime(year=2021, month=3, day=3))
#graph_frequency_by_time(df, 'delta')
#graph_frequency_by_time(df, 'total')
#graph_value_of_each_value(df)

