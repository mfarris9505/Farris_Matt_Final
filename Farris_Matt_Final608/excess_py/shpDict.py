# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 22:30:10 2016

@author: Matthew
"""
# Boorrowed Code from : http://www.abisen.com/blog/bokeh-maps/
# Given a shapeObject return a list of list for latitude and longitudes values
#       - Handle scenarios where there are multiple parts to a shapeObj

def getParts ( shapeObj ):

    points = []

    num_parts = len( shapeObj.parts )
    end = len( shapeObj.points ) - 1
    segments = list( shapeObj.parts ) + [ end ]

    for i in range( num_parts ):
        points.append( shapeObj.points[ segments[i]:segments[i+1] ] )
    
        
        return points

# Return a dict with three elements
#        - state_name
#        - total_area
#        - list of list representing latitudes
#        - list of list representing longitudes
#
#  Input: State Name & ShapeFile Object

def getDict ( state_name, shapefile ):

    stateDict = {state_name: {} }

    rec = []
    shp = []
    points = []


    # Select only the records representing the
    # "state_name" and discard all other
    for i in shapefile.shapeRecords( ):

        if i.record[2] == state_name:
            rec.append(i.record)
            shp.append(i.shape)

    # In a multi record state for calculating total area
	  # sum up the area of all the individual records
	  #        - first record element represents area in cms^2
        total_area = sum( [float(i[0]) for i in rec] ) / (1000*1000)


	  # For each selected shape object get
	  # list of points while considering the cases where there may be
	  # multiple parts  in a single record
        for j in shp:
	      for i in getParts(j):
	          points.append(i)

	  # Prepare the dictionary
	  # Seperate the points into two separate lists of lists (easier for bokeh to consume)
	  #      - one representing latitudes
	  #      - second representing longitudes

        lat = []
        lng = []
        for i in points:
	      lat.append( [j[0] for j in i] )
	      lng.append( [j[1] for j in i] )

        stateDict[state_name]['lat_list'] = lat
        stateDict[state_name]['lng_list'] = lng
        stateDict[state_name]['total_area'] = total_area

        return stateDict
