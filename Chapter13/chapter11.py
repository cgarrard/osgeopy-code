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


##############################  11.1 Matplotlib  ###########################

import matplotlib.pyplot as plt

# Turn interactive mode on if you want.
#plt.ion()


#########################  11.1.1 Plotting vector data  ####################

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

# Draw polygons as patches isntead.
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


#########################  11.1.2 Plotting raster data  ####################

ds = gdal.Open(r'D:\osgeopy-data\Washington\dem\sthelens_utm.tif')
data = ds.GetRasterBand(1).ReadAsArray()

# Default color ramp
plt.imshow(data)
plt.show()

# Grayscale
plt.imshow(data, cmap='gray')
plt.show()


# # Use the function from listing 11.5 to get overview data and plot it.
def get_overview_data(fn, band_index=1, level=-1):
    """Returns an array containing data from an overview.

    fn    - path to raster file
    band  - band number to get overview for
    level - overview level, where 1 is the highest resolution;
            the coarsest can be retrieved with -1
    """
    ds = gdal.Open(fn)
    band = ds.GetRasterBand(band_index)
    if level > 0:
        ov_band = band.GetOverview(level)
    else:
        num_ov = band.GetOverviewCount()
        ov_band = band.GetOverview(num_ov + level)
    return ov_band.ReadAsArray()

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


# Function from listing 11.6.
def stretch_data(data, num_stddev):
    """Returns the data with a standard deviation stretch applied.

    data       - array containing data to stretch
    num_stddev - number of standard deviations to use
    """
    mean = np.mean(data)
    std_range = np.std(data) * 2
    new_min = max(mean - std_range, np.min(data))
    new_max = min(mean + std_range, np.max(data))
    clipped_data = np.clip(data, new_min, new_max)
    return clipped_data / (new_max - new_min)

# Plot 3 stretched bands.
red_data = stretch_data(get_overview_data(red_fn), 2)
green_data = stretch_data(get_overview_data(green_fn), 2)
blue_data = stretch_data(get_overview_data(blue_fn), 2)
alpha = np.where(red_data + green_data + blue_data > 0, 1, 0)
data = np.dstack((red_data, green_data, blue_data, alpha))
plt.imshow(data)
plt.show()


#########################  11.1.3 Plotting 3D data  ####################

# See listing 11.7.


##################### 11.2.2 Storing mapnik data as xml  ###############

# Run listing 11.10 in order to save the xml file you need with the
# correct paths for your machine.

# Load the xml file and create an image from it.
m = mapnik.Map(400, 300)
m.zoom_to_box(mapnik.Box2d(-90.3, 29.7, -89.5, 30.3))
mapnik.load_map(m, r'd:\temp\nola_map.xml')
mapnik.render_to_file(m, r'd:\temp\nola4.png')


 # See listing 11.9-edited to see the hydrography xml in action.
