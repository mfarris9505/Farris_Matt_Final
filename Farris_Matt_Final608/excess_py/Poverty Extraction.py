# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 18:14:52 2016

@author: Matts42
"""
from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,

)
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure

from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment

import pandas as pd

palette.reverse()


ny_data = pd.read_csv("NYData.csv", sep = ",",float_precision = "high")
ny_data = ny_data.dropna(axis = 0)
hosp_lat = ny_data['Lat'].tolist()
hosp_long = ny_data['Long'].tolist()
hosp_name = ny_data['Provider.Name'].tolist()
hosp_payment= ny_data['Average.Medicare.Payments'].tolist()


counties = {
    code: county for code, county in counties.items() if county["state"] == "ny"
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]
color_mapper = LogColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
    hosp_lt = hosp_lat,
    hosp_lg = hosp_long))

source_hosp = ColumnDataSource(data=dict(
    x=hosp_long,
    y=hosp_lat,
    name=hosp_name,
    rate=hosp_payment))


TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

p = figure(
    title="New York Unemployment, 2009", tools=TOOLS,
    x_axis_location=None, y_axis_location=None
)
p.grid.grid_line_color = None

p.patches('x', 'y', source=source,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)
 
      
p.scatter('x','y', source=source_hosp,
          fill_alpha=0.6,
          line_color=None)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Unemployment rate)", "@rate%"),
    ("(Long, Lat)", "($x, $y)"),
]

show(p)

