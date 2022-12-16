import util
import pandas as pd
import numpy as np

def get_total(df):
    dA = list(util.get_parameter(df, 'delta'))
    deltas = list(filter(lambda v: not np.isnan(v), list(util.get_parameter(df, 'delta'))))
    sum = 0
    totals = np.zeros(len(deltas))
    for i in range(0, len(deltas)):
        totals[i] = sum + deltas[i]
        #totals.append(sum + col[i])
        sum += deltas[i]
    return totals


def get_frequencies(df, name=None):
    col = util.get_parameter(df, name)
    values = {}
    for value in col:
        values[value] = values[value] + 1 if value in values else 1
    return values
    