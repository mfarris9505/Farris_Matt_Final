# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 23:26:17 2016

@author: Matthew
"""
import pandas as pd
import numpy as np
from bokeh.sampledata.us_counties import data as tot_counties
from bokeh.sampledata.unemployment import data as unemployment

tot_data = pd.read_csv('data/Total_Data.csv',sep = ",",float_precision = "high")
tot_data = tot_data.replace('Not Available', np.nan)
tot_data = tot_data.dropna(axis=0)
tot_data = tot_data.apply(lambda x: pd.to_numeric(x, errors='ignore'))
tot_data['COUNTY'] = tot_data['COUNTY'].astype(int)
tot_data['COUNTY'] = tot_data['COUNTY'].astype(str)
tot_data['ST_FIPS'] = tot_data['COUNTY'].str[:-3]
tot_data['CT_FIPS'] = tot_data['COUNTY'].str[-3:]
tot_data['ST_FIPS'] = tot_data['ST_FIPS'].astype(int)
tot_data['CT_FIPS'] = tot_data['CT_FIPS'].astype(int)
tot_data['County'] = list(zip(tot_data['ST_FIPS'],tot_data['CT_FIPS']))
