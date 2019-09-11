from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure, output_file, save, show
from bokeh.models.widgets import Select, TableColumn, Div
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, HoverTool, CustomJS
from CIMPLO_KLM_data_handler import getData
import numpy as np
import pandas as pd


# // Retrieve data //
a, b = getData()
cols = list(b.columns)
cols.remove('Ground_Speed')
cols.remove('Flight_Phase')

b['y1'] = b.EGT
b['y2'] = b.Altitude
b['y3'] = b.Fuel_Flow

source = ColumnDataSource(b)

# // setting up the visualization/plots etc. //
TOOLS = 'crosshair, save, pan, box_zoom, reset, wheel_zoom'

div1 = Div(text="""Sensor Visualizations""", width=500, height=14)
div2 = Div(text=""" """, width=500, height=50)
div3 = Div(text="""Sensor Distribution""", width=500, height=14)

# source1 = ColumnDataSource(data=dict(x=b.index, y0=b.EGT_probe1, y1=b.Altitude, y6=b.Flight_Phase, y8=b.EGT))
p = figure(plot_width=900, plot_height=250, x_axis_type="datetime", y_axis_type='linear', tools=TOOLS)
p.line('time', 'y1', source=source, color='blue', alpha=0.5)

try:
    hist_1, edges_1 = np.histogram(b['y1'], density=True, bins=int(np.sqrt(len(b['y1']))))
except ValueError:
    temp_1 = b[~b['y1'].isna()]['y1']
    hist_1, edges_1 = np.histogram(temp_1, density=True, bins=int(np.sqrt(len(temp_1))))

source_hist_1 = ColumnDataSource(data=dict(x=hist_1, y=edges_1[:-1], z=edges_1[1:]))
p_hist = figure(plot_width=700, plot_height=250)
p_hist.quad(top='x', bottom=0, left='y', right='z', source=source_hist_1, color='purple', alpha=0.5)


# source2 = ColumnDataSource(data=dict(x=b.index, y0=b.Altitude, y6=b.Flight_Phase, y8=b.EGT))
p2 = figure(plot_width=900, plot_height=250, x_axis_type="datetime", y_axis_type='linear', tools=TOOLS)
p2.line('time', 'y2',  source=source, color='blue', alpha=0.5,)

try:
    hist_2, edges_2 = np.histogram(b['y2'], density=True, bins=int(np.sqrt(len(b['y2']))))
except ValueError:
    temp_2 = b[~b['y2'].isna()]['y2']
    hist_2, edges_2 = np.histogram(temp_2, density=True, bins=int(np.sqrt(len(temp_2))))
source_hist_2 = ColumnDataSource(data=dict(x=hist_2, y=edges_2[:-1], z=edges_2[1:]))
p2_hist = figure(plot_width=700, plot_height=250)
p2_hist.quad(top='x', bottom=0, left='y', right='z', source=source_hist_2, color='purple', alpha=0.5)


p3 = figure(plot_width=900, plot_height=250, x_axis_type="datetime", y_axis_type='linear', tools=TOOLS)
p3.line('time', 'y3',  source=source, color='blue', alpha=0.5)

try:
    hist_3, edges_3 = np.histogram(b['y3'], density=True, bins=int(np.sqrt(len(b['y3']))))
except ValueError:
    temp_3 = b[~b['y3'].isna()]['y3']
    hist_3, edges_3 = np.histogram(temp_3, density=True, bins=int(np.sqrt(len(temp_3))))
source_hist_3 = ColumnDataSource(data=dict(x=hist_3, y=edges_3[:-1], z=edges_3[1:]))
p3_hist = figure(plot_width=700, plot_height=250)
p3_hist.quad(top='x', bottom=0, left='y', right='z', source=source_hist_3, color='purple', alpha=0.5)


# // Set up widgets //
select1 = Select(title="           Sensor 1:", value="EGT", options=cols, sizing_mode='scale_both')
select2 = Select(title="           Sensor 2:", value="Altitude", options=cols, sizing_mode='scale_both')
select3 = Select(title="           Sensor 3:", value="Fuel_Flow", options=cols, sizing_mode='scale_both')


callback1 = CustomJS(args={'source': source}, code="""
        // print the selected value of the select widget - 
        // this is printed in the browser console.
        // cb_obj is the callback object, in this case the select 
        // widget. cb_obj.value is the selected value.
        console.log(' changed selected option', cb_obj.value);
     
        // create a new variable for the data of the column data source
        // this is linked to the plot
        var data = source.data;
               
        // allocate the selected column to the field for the y values
        data['y1'] = data[cb_obj.value];
       
        // register the change - this is required to process the change in 
        // the y values
        source.change.emit();
""")

callback2 = CustomJS(args={'source': source}, code="""
        // print the selected value of the select widget - 
        // this is printed in the browser console.
        // cb_obj is the callback object, in this case the select 
        // widget. cb_obj.value is the selected value.
        console.log(' changed selected option', cb_obj.value);
        
        // create a new variable for the data of the column data source
        // this is linked to the plot
        var data = source.data;

        // allocate the selected column to the field for the y values
        data['y2'] = data[cb_obj.value];
        
        // register the change - this is required to process the change in 
        // the y values
        source.change.emit();
""")

callback3 = CustomJS(args={'source': source}, code="""
        // print the selected value of the select widget - 
        // this is printed in the browser console.
        // cb_obj is the callback object, in this case the select 
        // widget. cb_obj.value is the selected value.
        console.log(' changed selected option', cb_obj.value);

        // create a new variable for the data of the column data source
        // this is linked to the plot
        var data = source.data;

        // allocate the selected column to the field for the y values
        data['y3'] = data[cb_obj.value];

        // register the change - this is required to process the change in 
        // the y values
        source.change.emit();
""")


def update_data1(attrname, old, new):

    sensor1 = select1.value
    try:
        hist_1, edges_1 = np.histogram(b[sensor1], density=True, bins=int(np.sqrt(len(b[sensor1]))))
    except ValueError:
        temp_1 = b[~b[sensor1].isna()][sensor1]
        hist_1, edges_1 = np.histogram(temp_1, density=True, bins=int(np.sqrt(len(temp_1))))
    source_hist_1.data = dict(x=hist_1, y=edges_1[:-1], z=edges_1[1:])


def update_data2(attrname, old, new):

    sensor2 = select2.value
    try:
        hist_2, edges_2 = np.histogram(b[sensor2], density=True, bins=int(np.sqrt(len(b[sensor2]))))
    except ValueError:
        temp_2 = b[~b[sensor2].isna()][sensor2]
        hist_2, edges_2 = np.histogram(temp_2, density=True, bins=int(np.sqrt(len(temp_2))))
    source_hist_2.data = dict(x=hist_2, y=edges_2[:-1], z=edges_2[1:])


def update_data3(attrname, old, new):

    sensor3 = select3.value
    try:
        hist_3, edges_3 = np.histogram(b[sensor3], density=True, bins=int(np.sqrt(len(b[sensor3]))))
    except ValueError:
        temp_3 = b[~b[sensor3].isna()][sensor3]
        hist_3, edges_3 = np.histogram(temp_3, density=True, bins=int(np.sqrt(len(temp_3))))
    source_hist_3.data = dict(x=hist_3, y=edges_3[:-1], z=edges_3[1:])


select1.callback = callback1
select1.on_change('value', update_data1)

select2.callback = callback2
select2.on_change('value', update_data2)

select3.callback = callback3
select3.on_change('value', update_data3)


#  // formats and tools //
p.xaxis.formatter = DatetimeTickFormatter(
    days=["%d %B %y %T"],
    months=["%d %B %y %T"],
    years=["%d %B %y %T"],
    hours=["%d %B %y %T"]
)

p.add_tools(HoverTool(
    tooltips=[
        ('Time of flight', '@time{%F %T}'),
        ('Value', '@y1'),
        ('Mean Value', '@EGT'),
        ('Altitude', '@Altitude'),
        ('phase', '@Flight_Phase')],
    formatters={
        'time': 'datetime'}, mode='vline'))

p.xaxis.axis_label = 'Time of flight'
# # p.yaxis.axis_label = 'EGT value'

p.legend.orientation = "horizontal"
p.legend.click_policy = "hide"

p2.xaxis.formatter = DatetimeTickFormatter(
        days=["%d %B %y %T"],
        months=["%d %B %y %T"],
        years=["%d %B %y %T"],
        hours=["%d %B %y %T"]
    )

p2.add_tools(HoverTool(
    tooltips=[
        ('Time of flight', '@time{%F %T}'),
        ('Value', '@y2'),
        ('phase', '@Flight_Phase')],
    formatters={
        'time': 'datetime'}, mode='vline'))

p2.xaxis.axis_label = 'Time of flight'
# p2.yaxis.axis_label = 'Altitude'

p2.x_range = p.x_range

p3.xaxis.formatter = DatetimeTickFormatter(
    days=["%d %B %y %T"],
    months=["%d %B %y %T"],
    years=["%d %B %y %T"],
    hours=["%d %B %y %T"]
)

p3.add_tools(HoverTool(
    tooltips=[
        ('Time of flight', '@time{%F %T}'),
        ('Value', '@y3'),
        ('Altitude', '@Altitude'),
        ('phase', '@Flight_Phase')],
    formatters={
        'time': 'datetime'}, mode='vline'))

p3.x_range = p.x_range

# // set up layout //
widgets = row(select1, select2, select3)
viz1 = column(div1, p, p2, p3)
first_col = column(widgets, viz1)
second_col = column(div2, div3, p_hist, p2_hist, p3_hist)
layout = row(first_col, second_col)

# // App or static (comment/uncomment the following) //
curdoc().add_root(layout)
curdoc().title = "CEOD"
# output_file("KLM_visualize.html")
# show(layout)



# ======================================================================================================
#
# def stats(b):
#
#     # cols = ['EGT_probe1', 'EGT_probe2', 'EGT_probe3', 'EGT_probe4', 'EGT_probe5', 'EGT_probe6', 'EGT_probe7',
#     #         'EGT_probe8', 'egt', 'FF', 'FF_demand', 'FF_selected', 'Vibration', 'fuel_to_air']
#     #
#     # df = b.iloc[:, cols]
#     # table = df.describe().transpose()
#     # cols = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
#     # descrpt_data = DataTable(source=table, columns=cols, editable=False)
#     #
#     # curdoc().add_root(column(descrpt_data))
#
#     #
#     #     # find the quartiles and IQR for each category
#     #     groups = df.groupby('group')
#     #     q1 = groups.quantile(q=0.25)
#     #     q2 = groups.quantile(q=0.5)
#     #     q3 = groups.quantile(q=0.75)
#     #     iqr = q3 - q1
#     #     upper = q3 + 1.5 * iqr
#     #     lower = q1 - 1.5 * iqr
#     #
#     #     # find the outliers for each category
#     #     def outliers(group):
#     #         cat = group.name
#     #         return group[(group.score > upper.loc[cat]['score']) | (group.score < lower.loc[cat]['score'])]['score']
#     #
#     #     out = groups.apply(outliers).dropna()
#     #
#     #     # prepare outlier data for plotting, we need coordinates for every outlier.
#     #     if not out.empty:
#     #         outx = []
#     #         outy = []
#     #         for keys in out.index:
#     #             outx.append(keys[0])
#     #             outy.append(out.loc[keys[0]].loc[keys[1]])
#     #
#     #     p = figure(tools="", background_fill_color="#efefef", x_range=cats, toolbar_location=None)
#     #
#     #     # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
#     #     qmin = groups.quantile(q=0.00)
#     #     qmax = groups.quantile(q=1.00)
#     #     upper.score = [min([x, y]) for (x, y) in zip(list(qmax.loc[:, 'score']), upper.score)]
#     #     lower.score = [max([x, y]) for (x, y) in zip(list(qmin.loc[:, 'score']), lower.score)]
#     #
#     #     # stems
#     #     p.segment(cats, upper.score, cats, q3.score, line_color="black")
#     #     p.segment(cats, lower.score, cats, q1.score, line_color="black")
#     #
#     #     # boxes
#     #     p.vbar(cats, 0.7, q2.score, q3.score, fill_color="#E08E79", line_color="black")
#     #     p.vbar(cats, 0.7, q1.score, q2.score, fill_color="#3B8686", line_color="black")
#     #
#     #     # whiskers (almost-0 height rects simpler than segments)
#     #     p.rect(cats, lower.score, 0.2, 0.01, line_color="black")
#     #     p.rect(cats, upper.score, 0.2, 0.01, line_color="black")
#     #
#     #     # outliers
#     #     if not out.empty:
#     #         p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
#     #
#     #     p.xgrid.grid_line_color = None
#     #     p.ygrid.grid_line_color = "white"
#     #     p.grid.grid_line_width = 2
#     #     p.xaxis.major_label_text_font_size = "12pt"


