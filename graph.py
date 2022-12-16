import pandas as pd
from matplotlib import pyplot as plt

import calc
import util

def trad_graph(x, y, name, dpi=1200, animate=False):
    plt.plot(x, y)
    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi)
    print(f'Printed to {graph_name}', False)

def graph_delta_by_time(df, start_date=None, end_date=None, animate=False):
    dates = list(util.get_column(df, 'date'))
    deltas = list(util.get_column(df, 'delta'))
    trad_graph(dates, deltas, 'deltas', False)

def graph_total_by_time(df, start_date=None, end_date=None, animate=False):
    totals = list(calc.get_total(df))
    dates = list(util.get_column(df, 'date'))[:len(totals)]
    trad_graph(dates, totals, 'totals', False)

def graph_frequency_by_time(df, name, start_date=None, end_date=None, animate=False):

    freq = calc.get_frequencies(df, name=name)

    sorted_freqs = sorted(freq.items())
    x, y = zip(*sorted_freqs)
    trad_graph(x, y, f'freq_{name}', False)




def graph_value_of_each_value(df, start_date=None, end_date=None, animate=False):
    freq = calc.get_frequencies(df, name='delta')
    sorted_freqs = sorted(freq.items())
    sorted_values = list(map(lambda v: (v[0], v[0] * v[1]), sorted_freqs))
    x, y = zip(*sorted_values)
    trad_graph(x, y, 'value_by_value', False)

def graph_weekdays(df, start_date=None, end_date=None, colors=['blue', 'black', 'green', 'brown', 'purple', 'red', 'orange']):
    raise NotImplementedError








filename = 'pursuit.csv'
df = pd.read_csv(filename)
#graph_total_by_time(df)
graph_value_of_each_value(df)

#graph_frequency_by_time(df, 'delta')
#graph_frequency_by_time(df, 'total')