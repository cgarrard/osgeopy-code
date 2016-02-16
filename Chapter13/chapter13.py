import os
import numpy as np
from osgeo import gdal, ogr
import matplotlib.pyplot as plt
import mapnik


# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
data_dir = r'D:\osgeopy-data'
# data_dir =


##############################  13.1 Matplotlib  ###########################

import matplotlib.pyplot as plt

# Turn interactive mode on if you want.
#plt.ion()


#########################  13.1.1 Plotting vector data  ####################

# Plot a line.
x = range(10)
y = [i * i for i in x]
plt.plot(x, y)
plt.show()

# Plot dots.
plt.plot(x, y, 'ro', markersize=10)
plt.show()

# Make a polygon.
x = list(range(10))
y = [i * i for i in x]
x.append(0)
y.append(0)
plt.plot(x, y, lw=5)
plt.show()

# Draw polygons as patches instead.
from matplotlib.path import Path
import matplotlib.patches as patches

coords = [(0, 0), (0.5, 1), (1, 0), (0, 0)]
codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]
path = Path(coords, codes)
patch = patches.PathPatch(path, facecolor='red')
plt.axes().add_patch(patch)
plt.show()

# This one has a hole in it. The inner ring must go in the
# opposite direction of the outer ring. In this example,
# outer_coords are clockwise and inner_coords are
# counter-clockwise.
outer_coords = [(0, 0), (0.5, 1), (1, 0), (0, 0)]
outer_codes = [Path.MOVETO, Path.LINETO,
               Path.LINETO, Path.LINETO]
inner_coords = [(0.4, 0.4), (0.5, 0.2),
                (0.6, 0.4), (0.4, 0.4)]
inner_codes = [Path.MOVETO, Path.LINETO,
               Path.LINETO, Path.LINETO]
coords = np.concatenate((outer_coords, inner_coords))
codes = np.concatenate((outer_codes, inner_codes))
path = Path(coords, codes)
patch = patches.PathPatch(path, facecolor='red')
plt.axes().add_patch(patch)
plt.show()



################################## Animation ############################
# Animate the albatross GPS locations from chapter 7.

# First set things up.
ds = ogr.Open(os.path.join(data_dir, 'Galapagos'))
gps_lyr = ds.GetLayerByName('albatross_lambert')
extent = gps_lyr.GetExtent()
fig = plt.figure()
plt.axis('equal')
plt.xlim(extent[0] - 1000, extent[1] + 1000)
plt.ylim(extent[2] - 1000, extent[3] + 1000)
plt.gca().get_xaxis().set_ticks([])
plt.gca().get_yaxis().set_ticks([])

# Plot the background continents.
import ch13funcs
land_lyr = ds.GetLayerByName('land_lambert')
row = next(land_lyr)
geom = row.geometry()
for i in range(geom.GetGeometryCount()):
    ch13funcs.plot_polygon(geom.GetGeometryRef(i))

# Get the timestamps for one of the birds.
timestamps, coordinates = [], []
gps_lyr.SetAttributeFilter("tag_id = '2131-2131'")
for row in gps_lyr:
    timestamps.append(row.GetField('timestamp'))
    coordinates.append((row.geometry().GetX(), row.geometry().GetY()))

# Initialize the points and annotation.
point = plt.plot(None, None, 'o')[0]
label = plt.gca().annotate('', (0.25, 0.95), xycoords='axes fraction')
label.set_animated(True)

# Write a function that tells matplotlib which items will change.
def init():
    point.set_data(None, None)
    return point, label

# Write a function to update the point location and annotation.
def update(i, point, label, timestamps, coordinates):
    label.set_text(timestamps[i])
    point.set_data(coordinates[i][0], coordinates[i][1])
    return point, label

# Finally run the animation.
import matplotlib.animation as animation
a = animation.FuncAnimation(
    fig, update, frames=len(timestamps), init_func=init,
    fargs=(point, label, timestamps, coordinates),
    interval=25, blit=True, repeat=False)
plt.show()

# Write a function that rounds timestamps.
from datetime import datetime, timedelta
def round_timestamp(ts, minutes=60):
    ts += timedelta(minutes=minutes/2.0)
    ts -= timedelta(
        minutes=ts.minute % minutes, seconds=ts.second,
        microseconds=ts.microsecond)
    return ts

# Initialize the timestamp and coordinates lists with the first set of values.
gps_lyr.SetAttributeFilter("tag_id = '2131-2131'")
time_format = '%Y-%m-%d %H:%M:%S.%f'
row = next(gps_lyr)
timestamp = datetime.strptime(row.GetField('timestamp'), time_format)
timestamp = round_timestamp(timestamp)
timestamps = [timestamp]
coordinates = [(row.geometry().GetX(), row.geometry().GetY())]

# Now get timestamps and coordinates, but fill in empty time slots with
# filler data.
hour = timedelta(hours=1)
for row in gps_lyr:
    timestamp = datetime.strptime(row.GetField('timestamp'), time_format)
    timestamp = round_timestamp(timestamp)
    while timestamps[-1] < timestamp:
        timestamps.append(timestamps[-1] + hour)
        coordinates.append((None, None))
    coordinates[-1] = (row.geometry().GetX(), row.geometry().GetY())

# Change the update function so it only updates coordinates if there are
# some for the current timestamp.
def update(i, point, label, timestamps, coordinates):
    label.set_text(timestamps[i])
    if coordinates[i][0] is not None:
        point.set_data(coordinates[i][0], coordinates[i][1])
    return point, label

# Run the animation again, but now it has constant time intervals.
a = animation.FuncAnimation(
    fig, update, frames=len(timestamps), init_func=init,
    fargs=(point, label, timestamps, coordinates),
    interval=25, blit=True, repeat=False)
plt.show()

#########################  13.1.2 Plotting raster data  ####################

ds = gdal.Open(r'D:\osgeopy-data\Washington\dem\sthelens_utm.tif')
data = ds.GetRasterBand(1).ReadAsArray()

# Default color ramp
plt.imshow(data)
plt.show()

# Grayscale
plt.imshow(data, cmap='gray')
plt.show()

# Use the function from listing 13.5 to get overview data and plot it.
from listing13_5 import get_overview_data
fn = r'D:\osgeopy-data\Landsat\Washington\p047r027_7t20000730_z10_nn10.tif'
data = get_overview_data(fn)
data = np.ma.masked_equal(data, 0)
plt.imshow(data, cmap='gray')
plt.show()

# Plot it using stretched data.
mean = np.mean(data)
std_range = np.std(data) * 2
plt.imshow(data, cmap='gray', vmin=mean-std_range, vmax=mean+std_range)
plt.show()

# Try plotting 3 bands.
os.chdir(r'D:\osgeopy-data\Landsat\Washington')
red_fn = 'p047r027_7t20000730_z10_nn30.tif'
green_fn = 'p047r027_7t20000730_z10_nn20.tif'
blue_fn = 'p047r027_7t20000730_z10_nn10.tif'

red_data = get_overview_data(red_fn)
green_data = get_overview_data(green_fn)
blue_data = get_overview_data(blue_fn)
data = np.dstack((red_data, green_data, blue_data))
plt.imshow(data)
plt.show()


# Plot 3 stretched bands.
from listing13_6 import stretch_data
red_data = stretch_data(get_overview_data(red_fn), 2)
green_data = stretch_data(get_overview_data(green_fn), 2)
blue_data = stretch_data(get_overview_data(blue_fn), 2)
alpha = np.where(red_data + green_data + blue_data > 0, 1, 0)
data = np.dstack((red_data, green_data, blue_data, alpha))
plt.imshow(data)
plt.show()


#########################  13.1.3 Plotting 3D data  ####################

# See listing 13.7.


##################### 13.2.2 Storing mapnik data as xml  ###############

# Run listing 13.10 in order to save the xml file you need with the
# correct paths for your machine.

# Load the xml file and create an image from it.
m = mapnik.Map(400, 300)
m.zoom_to_box(mapnik.Box2d(-90.3, 29.7, -89.5, 30.3))
mapnik.load_map(m, r'd:\temp\nola_map.xml')
mapnik.render_to_file(m, r'd:\temp\nola4.png')


 # See listing 13.9-edited to see the hydrography xml in action.
