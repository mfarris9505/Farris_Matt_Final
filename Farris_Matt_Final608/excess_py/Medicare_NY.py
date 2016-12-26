# -*- coding: utf-8 -*-
"""
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve --show Medicare_NY.py

@author: Matts42
"""
import pandas as pd
import math

from bokeh.io import show
from bokeh.layouts import row

from bokeh.models import (
    Select,
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    Widgets)

from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment



# 
palette.reverse()

TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

counties = {
    code: county for code, county in counties.items() if county["state"] == "ny"}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]
color_mapper = LogColorMapper(palette=palette)

# data prep 
ny_data = pd.read_csv("NYData.csv", sep = ",",float_precision = "high")
ny_data = ny_data.dropna(axis = 0) # FOR DISCUSSION AS TO WHY I REMOVED NA


#GROUPING FOR DISCUSSION
g_comb = ny_data.groupby('Comb.DRG').get_group("HF")
#g_prov = g_comb.groupby('Provider.Id').get_group("HF")

hosp_lat = g_comb['Lat'].tolist()
hosp_long = g_comb['Long'].tolist()
hosp_name = g_comb['Provider.Name'].tolist()
hosp_mort = g_comb['READMN'].tolist()
hosp_mort= [math.log1p(x)/10 for x in hosp_mort]

source = ColumnDataSource(data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates))
    
source_hosp = ColumnDataSource(data=dict(
    x=hosp_long,
    y=hosp_lat,
    name=hosp_name,
    radii = hosp_mort))

#Plot to show
p = figure(
    title="New York Unemployment, 2014", tools=TOOLS,
    x_axis_location=None, y_axis_location=None)

p.grid.grid_line_color = None
    
p.patches('x', 'y', source=source,
    fill_color={'field': 'rate', 'transform': color_mapper},
    fill_alpha=0.7, line_color="white", line_width=0.5)
    
    
p.scatter('x','y', radius = 'radii',
          source=source_hosp,
          fill_alpha=0.6,
          line_color=None)
          
hover = p.select_one(HoverTool)    
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Unemployment rate)", "@rate%"),
    ("(Long, Lat)", "($x, $y)")]
 
#Inputs 

#USING show to see the results  
show(p)

#Below Code to run the Server
""" 
#Layout 
layout = row(p)

curdoc().add_root(layout)
curdoc().title = "MedicareNY"
"""