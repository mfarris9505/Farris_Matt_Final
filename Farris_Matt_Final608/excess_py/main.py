# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:49:33 2016

@author: Matthew
"""
from os.path import dirname, join
import pandas as pd
import math

from bokeh.io import show
from bokeh.layouts import row

from bokeh.models import (
    Select,
    ColumnDataSource,
    HoverTool, 
    LogColorMapper)

from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.us_counties import data as counties

#Data Collection 
ny_data = pd.read_csv("states.csv", sep = ",")



