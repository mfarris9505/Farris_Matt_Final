# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:41:06 2016

@author: Matts42
"""


import pandas as pd 
# data cleanup
ny_data = pd.read_csv("NYData.csv", sep = ",",float_precision = "high")
ny_data = ny_data.dropna(axis = 0)
hosp_lat = ny_data['Lat'].tolist()
hosp_long = ny_data['Long'].tolist()
hosp_name = ny_data['Provider.Name'].tolist()
hosp_payment= ny_data['Average.Medicare.Payments'].tolist()

g_comb = ny_data.groupby('Comb.DRG').get_group("HF")
#drg_select = g_comb.groups.keys()


# Grouping Data: 
ny_data.groupby('Comb.DRG').get_group("HF")