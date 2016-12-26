# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:49:33 2016

bokeh serve --show main.py

@author: Matthew
"""

import pandas as pd
import numpy as np
import math

from bokeh.io import show
from bokeh.layouts import row, widgetbox

from bokeh.models import (
    Select,
    ColumnDataSource,
    HoverTool,
    LinearColorMapper)

from bokeh.models.widgets import (DataTable, 
    TableColumn, 
    Tabs, 
    Panel, 
    NumberFormatter)

from bokeh.palettes import OrRd9 as palette
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.us_counties import data as tot_counties
from bokeh.sampledata.unemployment import data as unemployment

#Setup
palette.reverse()
TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

#Data Initialization
states = pd.read_csv('data/states.csv', sep = ",")
states.columns = ['State', 'ABB']
states['abb'] = states['ABB'].str.lower()

state_dict= dict(zip(states['ABB'].tolist(),states['abb'].tolist()))

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

max_readm = tot_data['READM'].max(axis=0)
min_readm = tot_data['READM'].min(axis=0)
max_mort = tot_data['MORT'].max(axis=0)
min_mort = tot_data['MORT'].min(axis=0)


mort_color_mapper = LinearColorMapper(palette=palette, high=max_mort, low=min_mort)
readm_color_mapper = LinearColorMapper(palette=palette, high=max_readm, low=min_readm)

color_mapper ={"READM":readm_color_mapper,"MORT":mort_color_mapper}

copd_drg = [190,191,192]
pn_drg = [193,194,195]
hf_drg = [291,292,293]
ami_drg = [280,281,282,283,284,285]

drgs = {
         'HF': copd_drg,
         'PN': pn_drg,
         'COPD': copd_drg,
         'AMI': ami_drg
         }          
#Change state options because it didnt work for some states (NAN???)
#state_opt = states['ABB'].tolist()
state_opt = ['TX','OH','NC','NJ','WA','VA']
drg_opt = ['AMI','COPD', 'HF','PN']
ind_opt = ['READM', 'MORT']


current = tot_data.groupby('Provider.State').get_group("TX")
current = current.groupby('Comb.DRG').get_group("HF")
group = ['Provider.Name','Provider.Id','ZIP','Lat','Long','ST_FIPS','CT_FIPS','Comb.DRG']
current = current.groupby(group, as_index=False).agg({'Average.Medicare.Payments':'mean','READM':'mean','MORT':'mean'})
hosp_name = current['Provider.Name'].tolist()
payment = current['Average.Medicare.Payments'].tolist()
payment = [i/1000 for i in payment]
mort = current['MORT'].tolist()
readm = current['READM'].tolist()

source_table = ColumnDataSource(dict(
                                Hospital = hosp_name,
                                Payment=payment,
                                MORT=mort,
                                READM=readm))
    
counties = {code: county for code, county in tot_counties.items() if county["state"] == "tx"}

county_xs = [county["lons"] for county in counties.values()]
county_xs = [[x for x in item if x is not None] for item in county_xs]
county_ys = [county["lats"] for county in counties.values()]
county_ys = [[x for x in item if x is not None] for item in county_ys]  

county_names = [county['name'] for county in counties.values()]

#Finding Average Payment data in                 
county_rates = [county_id for county_id in counties]
county_rates = pd.DataFrame(county_rates)
county_rates.columns = ['ST_FIPS','CT_FIPS']
county_pay = current.groupby(['ST_FIPS','CT_FIPS'], as_index=False).agg({'READM':'mean'})
county_rates = pd.merge(county_rates, county_pay, how='left', on=['ST_FIPS', 'CT_FIPS'])
county_rates = county_rates.fillna(0)
county_rates = county_rates['READM'].tolist()
county_rates = [int(i) for i in county_rates]
                
hosp_lat = current['Lat'].tolist()
hosp_long = current['Long'].tolist()
    
source_hosp= ColumnDataSource(dict( 
    x=hosp_long,
    y=hosp_lat,
    radii=payment,
    name=hosp_name))

source_county = ColumnDataSource(dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates))

def update():
    
    current = tot_data.groupby('Provider.State').get_group(state.value)
    current = current.groupby('Comb.DRG').get_group(drg.value)
    group = ['Provider.Name','Provider.Id','ZIP','Lat','Long','ST_FIPS','CT_FIPS','Comb.DRG']
    current = current.groupby(group, as_index=False).agg({'Average.Medicare.Payments':'mean','READM':'mean','MORT':'mean'})
    hosp_name = current['Provider.Name'].tolist()
    payment = current['Average.Medicare.Payments'].tolist()
    payment = [i/1000 for i in payment]
    hosp_id = current['Provider.Id'].tolist()
    mort = current['MORT'].tolist()
    readm = current['READM'].tolist()

    source_table.data = {
        'Hospital': hosp_name,
        'Provider ID':hosp_id
        'Payment':payment,
        'Rate':mort}
    
    counties = {code: county for code, county in tot_counties.items() if county["state"] == state_dict[state.value] }

    #Necessary to remove NAN is the Counties Dataset... Not the best.
    county_xs = [county["lons"] for county in counties.values()]
    county_xs = [[x for x in item if x is not None] for item in county_xs]
    county_ys = [county["lats"] for county in counties.values()]
    county_ys = [[x for x in item if x is not None] for item in county_ys]             

    county_names = [county['name'] for county in counties.values()]
    county_rates = [county_id for county_id in counties]
    county_rates = pd.DataFrame(county_rates)
    county_rates.columns = ['ST_FIPS','CT_FIPS']
    county_pay = current.groupby(['ST_FIPS','CT_FIPS'], as_index=False).agg({ind.value:'mean'})
    county_rates = pd.merge(county_rates, county_pay, how='left', on=['ST_FIPS', 'CT_FIPS'])
    county_rates = county_rates.fillna(0)
    county_rates = county_rates[ind.value].tolist()
    county_rates = [int(i) for i in county_rates]
    
    hosp_lat = current['Lat'].tolist()
    hosp_long = current['Long'].tolist()
    
    source_hosp.data = {'x':hosp_long,
                        'y':hosp_lat,
                        'radii':payment,
                        'name':hosp_name}
    source_county.data ={
                         'x':county_xs,
                         'y':county_ys,
                         'name':county_names,
                         'rate':county_rates}


    
columns = [
    TableColumn(field="Hospital", title="Provider"),
    TableColumn(field="Payment", 
                title="Payments(in Thousands)",
                formatter=NumberFormatter(format="0,0.00")),
    TableColumn(field="MORT", title="Mortality",
                formatter=NumberFormatter(format="0.00")),
    TableColumn(field="READM", title="Readmission",
                formatter=NumberFormatter(format="0.00"))]

data_table = DataTable(source=source_table, columns=columns, width=800)

state = Select(title='State', value='TX', options=state_opt)
state.on_change('value', lambda attr, old, new: update())

drg = Select(title='DRG Code', value='HF', options=drg_opt)
drg.on_change('value', lambda attr, old, new: update())

ind = Select(title='Indicator', value='READM', options=ind_opt)
ind.on_change('value', lambda attr, old, new: update())
    
#Map 
p1 = figure(
    tools=TOOLS,
    title = "Indicator Rates of Counties Vs. Hospital Payments",
    x_axis_location=None, 
    y_axis_location=None)

p1.grid.grid_line_color = None
    
p1.patches('x', 'y', source=source_county,
    fill_color={'field': 'rate', 'transform': color_mapper[ind.value]},
    fill_alpha=0.7, line_color="white", line_width=0.5)
    
    
p1.circle('x','y', size='radii',
          source=source_hosp,
          fill_alpha=0.6,
          line_color=None)
#Graph 

p2 = figure(
    tools=TOOLS,
    title = "Hospital Payments Vs. Indicator",
    x_axis_label = "Indicator",
    y_axis_label = "Hosptial Payment")

p2.circle('Payment','Rate', size=5,
          source=source_table,
          fill_alpha=0.6)

table = widgetbox(data_table)

#Creating the 3 Tabs from the Graphs
tab1 = Panel(child=table, title="Table")
tab2 = Panel(child=p2, title ='Graph')
tab3 = Panel(child=p1, title="Map")
 

tabs = Tabs(tabs=[tab1, tab2, tab3])
controls = widgetbox([state,drg,ind], width=200)


#Layout 

curdoc().add_root(row(controls, tabs))
curdoc().title = "Medicare"
