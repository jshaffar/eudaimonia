import pandas as pd
from matplotlib import pyplot as plt
import datetime
import numpy as np
import calc
import util
import json
import argparse

def annot_max(x,y, num_annotations, ax=None):
    ymaxes = list(reversed(list((sorted(y))[-1*num_annotations:])))
    for ymax in ymaxes:
        xmax = x[list(y).index(ymax)]
        text= "x={:.3f}, y={:.3f}".format(xmax, ymax)
        if not ax:
            ax=plt.gca()
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
        kw = dict(xycoords='data',textcoords="data",
                arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")
        ax.annotate(text, xy=(xmax, ymax), xytext=(xmax+.5,ymax+5), **kw)


def trad_graph_provided_xy(x, y, name, dpi=1200, animate=False, num_annotations=0):
    plt.plot(x, y)
    if num_annotations > 0:
        annot_max(x, y, num_annotations)

    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')
    plt.clf()

# specifically designed for days of week initially but may need to expand
def multi_graph_provided_xy(x_data, y_data, data_labels, name, dpi=1200, animate=False, colors=None, alpha=.7, graph_minmax=True):
    plt.xticks(rotation=90)
    for i in range(0, len(x_data)):
        try:
            plt.plot(x_data[0], y_data[i], label=data_labels[i], color=colors[i] if colors is not None else None, alpha=alpha)
        except:
            plt.plot(x_data[6], y_data[i], label=data_labels[i], color=colors[i] if colors is not None else None, alpha=alpha)


    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')

def split_graph(df, trait, trait_to_split, name, date=0, dpi=1200, animate=False, colors_file=None, alpha=.7, graph_minmax=False):
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
        color=colors_dict[label.lower()] if label.lower() in colors_dict else None
        plt.plot(data_section['day'], data_section[trait],label=label, alpha=alpha, color=color)
        if graph_minmax:
            plt.axhline(min(list(data_section[trait])), color=color, linestyle='dashed', alpha=.2)
            plt.axhline(max(list(data_section[trait])), color=color, linestyle='dashed', alpha=.2)


    plt.legend()
    graph_name = f'Graphs/{name}'
    plt.savefig(graph_name, dpi=dpi, bbox_inches='tight')
    print(f'Printed to {graph_name}')
    plt.clf()

def get_name(attribute, params, start_date, end_date):
    name = attribute
    if start_date is not None:
        name += f'-from_{start_date}'
    if end_date is not None:
        name += f'-to_{end_date}'
    for param in params:
        if params[param] is not None:
            name += f'-{param}_{params[param]}'
    return name

def graph_attribute_by_time(df, attribute, params={}, start_date=None, end_date=None, animate=False):
    if "on_weekday" in params and params["on_weekday"]:
        return graph_weekday_attribute_by_time(df, attribute=attribute, params=params, start_date=start_date, end_date=end_date, animate=animate)
    dates = list(util.get_column(df, 'day', start_date=start_date, end_date=end_date))
    y_var = list(util.get_column(df, attribute, start_date=start_date, end_date=end_date))
    name = get_name(attribute=attribute, params=params, start_date=start_date, end_date=end_date)
    trad_graph_provided_xy(dates, y_var, name, animate=False)

def graph_weekday_attribute_by_time(df, attribute, params={}, start_date=None, end_date=None, colors_file='Config/default.json', animate=False):
    df = util.add_parameter(df, 'weekday')
    frames = util.split_frame(df, param_to_split='weekday')
    labels = []
    x_data = []
    y_data = []
    for frame in frames:
        frames[frame] = util.add_parameter(frames[frame], attribute, need_custom_method=True)
        dates = list(util.get_column(frames[frame], column_name='day', start_date=start_date, end_date=end_date))
        y_var = list(util.get_column(frames[frame], column_name=attribute, start_date=start_date, end_date=end_date))
        x_data.append(dates)
        y_data.append(y_var)
        labels.append(frame)
    params['weekday'] = True
    name = get_name(attribute=attribute, params=params, start_date=start_date, end_date=end_date)
    multi_graph_provided_xy(x_data=x_data, y_data=y_data, data_labels=labels, name=name)



def graph_frequency_by_time(df, name, start_date=None, end_date=None, animate=False, num_annotations=0):
    freq = calc.get_frequencies(df, name=name, start_date=start_date, end_date=end_date)
    sorted_freqs = sorted(freq.items())
    x, y = zip(*sorted_freqs)
    graph_name = get_name(attribute=f'frequency-{name}', params={}, start_date=start_date, end_date=end_date)
    trad_graph_provided_xy(x, y, graph_name, animate=False, num_annotations=num_annotations)


def graph_value_of_each_value(df, start_date=None, end_date=None, animate=False):
    freq = calc.get_frequencies(df, name='Delta', start_date=start_date, end_date=end_date)
    sorted_freqs = sorted(freq.items())
    sorted_values = list(map(lambda v: (v[0], v[0] * v[1]), sorted_freqs))
    x, y = zip(*sorted_values)
    trad_graph_provided_xy(x, y, 'value_by_value', animate=False)

def graph_weekdays(df, trait, start_date=None, end_date=None, colors_file='Config/default.json', graph_minmax=False):
    #df2 = calc.get_weekdays_dataframe(df)
    df = util.filter_dataframe(df, start_date=start_date, end_date=end_date)
    df = util.add_parameter(df, trait)
    name = f'days_of_week_{trait}_from_{df["Date"].iloc[0].replace("/", "-")}_to_{df["Date"].iloc[-1].replace("/", "-")}'
    split_graph(df=df, trait=trait, trait_to_split='weekday', name=name, colors_file=colors_file, graph_minmax=graph_minmax)



if __name__ == "__main__":
    default_attribute = 'Total'
    filename = 'pursuit.csv'
    df = util.get_df_from_csv(filename)
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date', '-sd')
    parser.add_argument('--end_date', '-ed', default=None)
    parser.add_argument('--attribute', '-a', default=default_attribute)
    parser.add_argument('--name', '-n', default=None)
    parser.add_argument('--on_weekday', '-ow', default="False")
    args = parser.parse_args()
    def parse_date(date_str):
        date_split = list(map(lambda v: int(v), date_str.split('/')))
        date = datetime.datetime(year=date_split[2], month=date_split[0], day=date_split[1])
        print(date)
        return date
    start_date = parse_date(args.start_date) if args.start_date is not None else None
    end_date = parse_date(args.end_date) if args.end_date is not None else None
    attribute = args.attribute
    on_weekday = args.on_weekday.lower() in ["t", "true"]

    if attribute is not None and attribute in ['Total', 'Delta']:
        params = {"name":args.name}
        graph_attribute_by_time(df=df, params=params, attribute=attribute, start_date=start_date, end_date=end_date)
    elif attribute == 'Frequency':
        graph_frequency_by_time(df=df, start_date=start_date, end_date=end_date, name=args.name)
    elif attribute == 'Value':
        graph_value_of_each_value(df=df, start_date=start_date, end_date=end_date)
    else:
        raise Exception(f'currently unsupported option: {attribute}')



#graph_weekdays(df, 'total', start_date=datetime.datetime(year=2022, month=1, day=1))
#graph_weekdays(df, 'Total', start_date=datetime.datetime(year=2023, month=1, day=1), graph_minmax=True)

#graph_total_by_time(df)
#graph_delta_by_time(df, start_date=datetime.datetime(year=2021, month=2, day=3), end_date=datetime.datetime(year=2021, month=3, day=3))
#graph_frequency_by_time(df, 'Delta', num_annotations=1)
#graph_frequency_by_time(df, 'Total')
#graph_value_of_each_value(df)

