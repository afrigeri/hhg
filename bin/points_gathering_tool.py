import sys
import pylab as plt
from osgeo import gdal
gdal.UseExceptions()

#if using a valid input file argument, then react accordingly
try:
	ds = gdal.Open(sys.argv[1])
except:
	print("No valid input file found, using example")
	ds = gdal.Open('../data/LO_22S337_CKSPK_subset.tif')

band = ds.GetRasterBand(1)
elevation = band.ReadAsArray()

print elevation.shape
print elevation

nrows, ncols = elevation.shape

# I'm making the assumption that the image isn't rotated/skewed/etc. 
# This is not the correct method in general, but let's ignore that for now
# If dxdy or dydx aren't 0, then this will be incorrect
x0, dx, dxdy, y0, dydx, dy = ds.GetGeoTransform()

x1 = x0 + dx * ncols
y1 = y0 + dy * nrows

fig = plt.figure()
plt.imshow(elevation, cmap='gist_earth', extent=[x0, x1, y1, y0])

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

