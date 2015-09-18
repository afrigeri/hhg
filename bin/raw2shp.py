#!/usr/bin/env python

#Purpose:
#Convert raw results from the Holy Hand Grenade
#to a shapefile of crater circles (polygons)
#This is using the buffer option from OGR
#The first line has the center point location
#The second line has one point from the crater ring
#The buffer distance is thus the Euclidian distance from both points

####################
##Create a buffer from a known distance
##Distance should be calculated by Euclidean distance between center point and crater ring point, then run the code on the whole list of points pairs
####################
from osgeo import ogr
##Say we know x1, y1, x2, y2
wkt = "POINT (" + x1 +" " + y1 + ")"
pt = ogr.CreateGeometryFromWkt(wkt)
bufferDistance = 500 #sqrt(pow(x2-x1,2)+sqrt(pow(y2-y1,2))
poly = pt.Buffer(bufferDistance)
print "%s buffered by %d is %s" % (pt.ExportToWkt(), bufferDistance, poly.ExportToWkt())
##Now import it into a shapefile
 
