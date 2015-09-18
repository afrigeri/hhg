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

import numpy as np
b = np.genfromtxt(r'results.txt', delimiter=',', names=True, dtype=None)
print( b[0][3].split('=')[-1], b[0][4].split('=')[-1])
print( b.shape[0] )

#Final stage: Create a new shapefile directly
import os, osgeo.ogr, osgeo.osr
sr = osgeo.osr.SpatialReference()
#Assumes Geo lat/long wgs84
sr.ImportFromEPSG(3148)
#Export to Shapefile called craters.shp
driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
if os.path.exists('craters.shp'):
        driver.DeleteDataSource('craters.shp')
shpData = driver.CreateDataSource('craters.shp')
if shpData is None:
        print ' Could not create file'
        sys.exit(1)
lyr = shpData.CreateLayer('layer1', sr, osgeo.ogr.wkbPolygon)
lyrDef = lyr.GetLayerDefn()
idField = osgeo.ogr.FieldDefn("ID_0", osgeo.ogr.OFTReal)
lyr.CreateField(idField)
fidx = 0

i = 0
while (i+1 < b.shape[0]):
	##Say we know x1, y1, x2, y2
	x1 = float(b[i][3].split('=')[-1])
	y1 = float(b[i][4].split('=')[-1])
	x2 = float(b[i+1][3].split('=')[-1])
	y2 = float(b[i+1][4].split('=')[-1])
	wkt = "POINT (" + str(x1) +" " + str(y1) + ")"
	pt = osgeo.ogr.CreateGeometryFromWkt(wkt)
	bufferDistance = np.sqrt(pow(x2-x1,2)+np.sqrt(pow(y2-y1,2)))
	print( bufferDistance)
	poly = pt.Buffer(bufferDistance)
	print( "%s buffered by %d is %s" % (pt.ExportToWkt(), bufferDistance, poly.ExportToWkt()))
	#Make sure we skip to the next tuple
	i = i+2
	##Now import it into a shapefile
        ftr = osgeo.ogr.Feature(lyrDef)
        ftr.SetGeometry(poly)
        ftr.SetFID(fidx)
        ftr.SetField(ftr.GetFieldIndex('ID_0'),i/2)
        lyr.CreateFeature(ftr)
        fidx += 1

shpData.Destroy()


#create shapefile projection file
sr.MorphToESRI()
file = open('craters.prj', 'w')
file.write(sr.ExportToWkt())
file.close()


 
