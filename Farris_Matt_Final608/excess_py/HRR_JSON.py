# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 23:53:10 2016

@author: Matthew
"""
import urllib2
import json

url = "https://raw.githubusercontent.com/jgoodall/us-maps/master/geojson/hrr.json"
response = urllib2.urlopen(url)
data = json.loads(response.read())


# Transform python object back into json
output_json = json.dumps(data)

from bokeh.io import output_file, show
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure


geo_source = GeoJSONDataSource(geojson=output_json)

p = figure()
p.patches(xs='xs', ys='ys', alpha=0.9, source=geo_source)
output_file("geojson.html")
show(p)
