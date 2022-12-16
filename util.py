import calc

def get_column(df, column_name, start_date=None, end_date=None):
    return df.loc[:,column_name]

def get_parameter(df, name, start_date=None, end_date=None):
    if name in df.columns:
        return get_column(df, name, start_date, end_date)
    elif name == 'total':
        return calc.get_total(df)
    else:
        raise Exception(f'Do not know how to handle name = {name}')
