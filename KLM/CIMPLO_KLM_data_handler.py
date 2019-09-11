import pandas as pd
import datetime
import numpy as np
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool
from bokeh.layouts import column


def getData():
    """
    Takes in a path where the data is and returns a visualization of the most important parameters
    :return: Visualization, raw dataframe and processed dataframe
    """

    # put data path
    data = pd.read_csv('cimplo_platform_toy.csv', parse_dates=False, delimiter=",", decimal=".", header=0)

    # rename columns
    cols = ['offset', 'start_date', 'start_time', 'hour', 'Altitude', 'EGT_probe1', 'EGT_probe2',
            'EGT_probe3', 'EGT_probe4', 'EGT_probe5', 'EGT_probe6', 'EGT_probe7', 'EGT_probe8', 'ESN', 'FL', 'EGT',
            'Fuel_Flow', 'FF_selected', 'Flight_Phase', 'Ground_Speed', 'Fuel_to_Air']
    data.columns = cols
    # t = int(data.start_time.unique()[0])
    # d = int(data.start_date.unique()[0])
    # cuml = actual_time(t, d, data.offset)
    # data['time'] = cuml
    # data = data.set_index(data.time)
    # data = data.drop(['time'], axis=1)
    #
    # return data

    # extract the necessary data based on the sampling rate of the EGT probes
    times = data.offset[~pd.isnull(data.EGT_probe1)]
    esn = int(data.ESN.unique()[0])
    fl = data.FL.unique()[0]
    y1 = data.EGT_probe1[~pd.isnull(data.EGT_probe1)]
    y2 = data.EGT_probe2[~pd.isnull(data.EGT_probe2)]
    y3 = data.EGT_probe3[~pd.isnull(data.EGT_probe3)]
    y4 = data.EGT_probe4[~pd.isnull(data.EGT_probe4)]
    y5 = data.EGT_probe5[~pd.isnull(data.EGT_probe5)]
    y6 = data.EGT_probe6[~pd.isnull(data.EGT_probe6)]
    y7 = data.EGT_probe7[~pd.isnull(data.EGT_probe7)]
    y8 = data.EGT_probe8[~pd.isnull(data.EGT_probe8)]
    y9 = data.EGT.iloc[times.index]
    y10 = data.Fuel_Flow.iloc[times.index]
    y11 = data.FF_selected.iloc[times.index]
    y12 = data.Flight_Phase.iloc[times.index]
    y13 = data.Ground_Speed.iloc[times.index]
    y14 = data.Fuel_to_Air.iloc[times.index]

    # because the sampling rate of the altitude was smaller than the EGT probes I linearly interpolate
    altitude = data.Altitude.iloc[times.index]
    altitude = altitude.interpolate(classmethod='linear')

    # create the timeline of the flight based on the startup time, departure data and offset
    t = 133029# int(data.start_time.unique()[0]) // Inserting fake data for security
    d = 920227# int(data.start_date.unique()[0])  // Inserting fake data for security
    cuml = actual_time(t, d, times)


    # creating the dataframe and plotting it
    data3 = pd.DataFrame(
        {'offset': times, 'EGT_probe1': y1, 'EGT_probe2': y2, 'EGT_probe3': y3, 'EGT_probe4': y4, 'EGT_probe5': y5,
         'EGT_probe6': y6, 'EGT_probe7': y7, 'EGT_probe8': y8, 'Altitude': altitude, 'EGT': y9, 'Fuel_Flow': y10,
         'FF_selected': y11,  'Flight_Phase': y12, 'Ground_Speed': y13, 'Fuel_to_Air': y14})
    data3['time'] = cuml
    data3.iloc[:4].Flight_Phase.fillna(method='bfill', inplace=True)
    data3.Flight_Phase.fillna(method='ffill', inplace=True)
    # bokeh_plot(data3)

    data3 = data3.set_index(data3.time)
    cols = ['EGT_probe1', 'EGT_probe2', 'EGT_probe3', 'EGT_probe4', 'EGT_probe5', 'EGT_probe6', 'EGT_probe7',
            'EGT_probe8', 'EGT', 'Fuel_Flow', 'FF_selected', 'Ground_Speed', 'Fuel_to_Air', 'Altitude', 'Flight_Phase']
    data3 = data3.loc[:, cols]
    # data3 = data3.iloc[3:]
    # data3 = data3.asfreq('960L')

    return data, data3


def date_time(t, d):
    """
    Returning year, month, day, hour, minute, second of start time
    :param t: start time of flight
    :param d: start day of flight
    :return:
    """
    s = t % 100
    temp = np.int(np.floor(t/100))
    mnt = temp % 100
    h = np.int(np.floor(temp/100))

    day = d % 100
    temp = np.int(np.floor(d / 100))
    m = temp % 100
    year = np.int(np.floor(temp / 100))
    year = 1900+year
    ms = s - int(s)
    return year, m, day, h, mnt, int(s)


def actual_time(t, d, ints):
    """
    Creating the time axis based on the KLM data
    :param t: start time of flight
    :param d: date of departure
    :param ints: offset of time
    :return: timeline fo flight
    """
    dt = date_time(t, d)

    t = pd.Timestamp(year=dt[0], month=dt[1], day=dt[2], hour=dt[3], minute=dt[4], second=dt[5])
    # or datetime.datetime

    cum = []
    for i in ints.values:
        w = pd.Timedelta(i, unit='s') # milliseconds
        cum.append(t+w) #(datetime.datetime.combine(datetime.date(1, 1, 1), t) + w).time())

    return cum


def bokeh_plot(b):
    """
    Creating the bokeh plot for the KLM CEOD
    :param b: data frame
    :return: plot
    """

    TOOLS = 'crosshair,save,pan,box_zoom,reset,wheel_zoom'
    probes = ['EGT_probe1', 'EGT_probe2', 'EGT_probe3', 'EGT_probe4', 'EGT_probe5', 'EGT_probe6', 'EGT_probe7',
              'EGT_probe8']
    colors = ['navy', 'cadetblue', 'orange', 'brown', 'green', 'purple', 'cyan', 'black']
    p = figure(plot_width=1600, plot_height=500, x_axis_type="datetime", y_axis_type='linear', tools=TOOLS)
    for probe, color in zip(probes, colors):
        source = ColumnDataSource(data=dict(x=b.time, y0=b[probe], y1=b.altitude, y2=b.FF, y3=b.FF_demand,
                                            y4=b.FF_selected, y5=b.Vibration, y6=b.fph, y7=b.ground_speed, y8=b.EGT,
                                            y9=b.fuel_to_air))
        p.line('x', 'y0', source=source, legend=probe, color=color, alpha=0.5)

    p.line('x', 'y8', source=source, legend='Mean EGT', color='fuchsia', alpha=0.5)
    p2 = figure(plot_width=1600, plot_height=200, x_axis_type="datetime", y_axis_type='linear', tools=TOOLS)
    p2.line('x', 'y1',  source=source, legend='Altitude', color='black', alpha=0.5)
    p3 = figure(plot_width=1600, plot_height=200, x_axis_type="datetime", y_axis_type='linear', tools=TOOLS)
    p3.line('x', 'y5',  source=source, legend='Vibration', color='black', alpha=0.5)
    # p3.line('x', 'y3',  source=source, legend='Fuel Flow demand', color='red', alpha=0.5)
    # p3.line('x', 'y4',  source=source, legend='Fuel Flow selected', color='yellow', alpha=0.5)

    p.xaxis.formatter = DatetimeTickFormatter(
        days=["%d %B %y %T"],
        months=["%d %B %y %T"],
        years=["%d %B %y %T"],
        hours=["%d %B %y %T"]
    )

    p2.xaxis.formatter = DatetimeTickFormatter(
        days=["%d %B %y %T"],
        months=["%d %B %y %T"],
        years=["%d %B %y %T"],
        hours=["%d %B %y %T"]
    )

    p3.xaxis.formatter = DatetimeTickFormatter(
        days=["%d %B %y %T"],
        months=["%d %B %y %T"],
        years=["%d %B %y %T"],
        hours=["%d %B %y %T"]
    )

    p.add_tools(HoverTool(
        tooltips=[
            ('Time of flight', '@x{%F %T}'),
            ('Value', '@y0'),
            ('Mean Value', '@y8'),
            ('Altitude', '@y1'),
            ('phase', '@y6')],
        formatters={
            'x': 'datetime'}, mode='vline'))

    p2.add_tools(HoverTool(
        tooltips=[
            ('Time of flight', '@x{%F %T}'),
            ('Value', '@y1'),
            ('phase', '@y6')],
        formatters={
            'x': 'datetime'}, mode='vline'))

    p3.add_tools(HoverTool(
        tooltips=[
            ('Time of flight', '@x{%F %T}'),
            ('Value', '@y5'),
            ('Altitude', '@y1')],
        formatters={
            'x': 'datetime'}, mode='vline'))

    p.xaxis.axis_label = 'Time of flight'
    p.yaxis.axis_label = 'EGT value'
    p2.xaxis.axis_label = 'Time of flight'
    p2.yaxis.axis_label = 'Altitude'
    p3.xaxis.axis_label = 'Time of flight'
    p3.yaxis.axis_label = 'Vibration'
    p.legend.location = "bottom_center"
    p3.legend.location = "top_center"
    p.legend.orientation = "horizontal"
    p.legend.click_policy = "hide"
    p3.legend.click_policy = "hide"
    p2.x_range = p.x_range = p3.x_range
    output_file("KLM.html")
    show(column(p, p3, p2))
