# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 15:53:03 2016

@author: Matthew
"""

def process_data(tot_data,tot_counties):
    
    current = tot_data.groupby('Provider.State').get_group(state.value)
    current = current.groupby('Comb.DRG').get_group(drg.value)
    group = ['Provider.Name','Provider.Id','ZIP','Lat','Long','ST_FIPS','CT_FIPS','Comb.DRG']
    current = current.groupby(group, as_index=False).agg({'Average.Medicare.Payments':'mean','READM':'mean','MORT':'mean'})
    hosp_name = current['Provider.Name'].tolist()
    payment = current['Average.Medicare.Payments'].tolist()
    payment = [i/1000 for i in payment]
    mort = current['MORT'].tolist()
    readm = current['READM'].tolist()

    source_table.data = {
        'Hospital': hosp_name,
        'Payment':payment,
        'Mortality':mort,
        'Readmission':readm}
    
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
                         