# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:04:21 2016

@author: Matts42
"""



import pandas as pd
import numpy as np
import shapefile
from shpDict import getDict


dat = shapefile.Reader("HSA_Bdry.SHP")
states = set([i[2] for i in dat.iterRecords()])

from bokeh.io import show
from bokeh.plotting import figure

TOOLS="pan,wheel_zoom,box_zoom,reset,previewsave"
p = figure(title="Map of India", tools=TOOLS, plot_width=900, plot_height=800)




