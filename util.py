import calc
import datetime
import numpy as np
import pandas as pd
import matplotlib as plt


def get_column(df, column_name, start_date=None, end_date=None):
    start_date_name = start_date.strftime("%-m/%-d/%-Y") if start_date is not None else None
    end_date_name = start_date.strftime("%-m/%-d/%-Y") if start_date is not None else None
    start_index = df[df['Date']==start_date_name].index.values[0] if start_date is not None else 0
    end_index = df[df['Date']==end_date_name].index.values[0] if end_date is not None else len(df.loc[:, 'Delta'])
    col = df.loc[:,column_name].iloc[start_index:end_index+1]
    return col

"""
gets first row like something
"""
def get_row(df, row_trait, row_name, additional_columns=[]):
    #return list(df.loc[df[row_trait] == row_name].iloc[0])
    return df.loc[df[row_trait] == row_name].iloc[0] 

"""
gets all rows like something
"""
def get_rows(df, row_trait, row_name):
    # TODO untested
    return df.loc[df[row_trait] == row_name].values.T.tolist()


def get_parameter(df, name, start_date=None, end_date=None):
    if name in df.columns:
        return get_column(df, name, start_date, end_date)
    elif name == 'Total':
        return calc.get_total(df)
    else:
        raise Exception(f'Do not know how to handle name: {name}')

def filter_dataframe(df, trait='Delta', start_date=None, end_date=None):
    if 'day' not in df.columns:
        df = add_parameter(df, 'day')
    start_date = start_date if start_date is not None else min(df['day'])
    end_date = end_date if end_date is not None else max(df['day'])
    df = df[df.apply(lambda v: v['day'] >= start_date and v['day'] <= end_date, axis=1)]
    df = df[df.apply(lambda v: not np.isnan(v[trait]), axis=1)]
    return df

def add_parameter(df, trait):
    if trait in df.columns:
        print('Trait is already in df, no need to add it')
    elif trait == 'Total':
        col = calc.get_total(df)
        df['Total'] = col
    elif trait == 'day':
        df = calc.get_day(df)
    elif trait == 'weekday':
        df = calc.get_weekday(df)
    else:
        raise Exception(f'Do not know how to handle trait: {trait}')
    return df


def add_parameters(df, traits):
    for trait in traits: df = add_parameter(trait)
    return df

def add_parameter_to_weekdays(df, trait):
    if trait in df[0][0][1]:
        print('Trait is already in df, no need to add it')
    elif trait == 'total_weekday':
        all_deltas = [list(map(lambda v: v[1]['Delta'], df[d])) for d in df]
        for i in range(0, len(df)):
            deltas = list(map(lambda v: v[1]['Delta'], df))
            dA = 0
        [calc.get_total(deltas=0) for i in range(0, len(df))]
        dA = 0
    else:
        raise Exception(f'Do not know how to handle trait: {trait}')

def add_parameters_to_weekdays(df, traits):
    for trait in traits: df = add_parameter_to_weekdays(df, trait)
    return df


def get_df_from_csv(filename : str):
    df = pd.read_csv(filename)
    df = filter_dataframe(df)
    df = add_parameter(df, trait='day')
    return df


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)
    
