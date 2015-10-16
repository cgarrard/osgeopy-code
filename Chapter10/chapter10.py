
import os
import numpy as np
from osgeo import gdal
import scipy.stats
import ospybook as pb

# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
data_dir = r'D:\osgeopy-data'
# data_dir =



##############################  10.1 Intro to NumPy  ##########################

# Test out an array.
import numpy as np
a = np.arange(12)
a
a[1]
a[1:5]

# Change an array's shape.
a = np.reshape(a, (3,4))
a
a[1,2]

# Access entire rows or columns.
a[1]
a[:,2]

# Access 2-dimensional slice.
a[1:,1:3]
a[2,:-1]

# Math
a = np.array([[1, 3, 4], [2, 7, 6]])
b = np.array([[5, 2, 9], [3, 6, 4]])
a
b
a + b
a > b

# Where
np.where(a > b, 10, 5)
np.where(a > b, a, b)

# Access non-contiguous data.
a = np.random.randint(0, 20, 12)
a
a[[8, 0, 3]]

a = np.reshape(a, (3, 4))
a
a[[2, 0, 0], [0, 0, 3]]

# Use Booleans.
b
a[b]
np.mean(a[a>5])

# Create arrays.
np.zeros((3,2))
np.ones((2,3), np.int)
np.ones((2,3), np.int) * 5
np.empty((2,2))


##############################  10.2 Map Algebra  #############################

###########################  10.2.1 Local Analyses  ###########################

# These examples are here because they're in the text, but really you should
# follow the method shown in listing 10.2.

os.chdir(os.path.join(data_dir, 'Massachusetts'))
in_fn = 'm_4207162_ne_19_1_20140718_20140923.tif'
out_fn = 'ndvi2.tif'

ds = gdal.Open(in_fn)
red = ds.GetRasterBand(1).ReadAsArray().astype(np.float)
nir = ds.GetRasterBand(4).ReadAsArray()
red = np.ma.masked_where(nir + red == 0, red)

# This is the first method shown in the text.
ndvi = (nir - red) / (nir + red)
ndvi = np.where(np.isnan(ndvi), -99, ndvi)
ndvi = np.where(np.isinf(ndvi), -99, ndvi)
pb.make_raster(ds, 'ndvi2.tif', ndvi, gdal.GDT_Float32, -99)

# This is the second method shown in the text.
ndvi = np.where(nir + red > 0, (nir - red) / (nir + red), -99)
pb.make_raster(ds, 'ndvi3.tif', ndvi, gdal.GDT_Float32, -99)

del ds


###########################  10.2.2 Focal Analyses  ###########################

indata  = np.array([
    [3, 5, 6, 4, 4, 3],
    [4, 5, 8, 9, 6, 5],
    [2, 2, 5, 7, 6, 4],
    [5, 7, 9, 8, 9, 7],
    [4, 6, 5, 7, 7, 5],
    [3, 2, 5, 3, 4, 4]])

outdata =  np.zeros((6, 6))

outdata[2,2] = (indata[1,1] + indata[1,2] + indata[1,3] +
                indata[2,1] + indata[2,2] + indata[2,3] +
                indata[3,1] + indata[3,2] + indata[3,3]) / 9
print(outdata)

# DO NOT try this on a real image because it's way too slow.
rows, cols = indata.shape
outdata = np.zeros(indata.shape, np.float32)
for i in range(1, rows-1):
    for j in range(1, cols-1):
        outdata[i,j] = np.mean(indata[i-1:i+2, j-1:j+2])
print(outdata)

# This one is fine, but is a pain to type out.
outdata = np.zeros(indata.shape, np.float32)
outdata[1:rows-1, 1:cols-1] = (
    indata[0:-2, 0:-2] + indata[0:-2, 1:-1] + indata[0:-2, 2:] +
    indata[1:-1, 0:-2] + indata[1:-1, 1:-1] + indata[1:-1, 2:] +
    indata[2:  , 0:-2] + indata[2:  , 1:-1] + indata[2:  , 2:]) / 9
print(outdata)

# Check out some slices
slices = []
for i in range(3):
    for j in range(3):
        slices.append(indata[i:rows-2+i, j:cols-2+j])
print(slices)

# This is the upper left slice.
print(slices[0])

# Stack the slices and compute the mean.
stacked = np.dstack(slices)
outdata = np.zeros(indata.shape, np.float32)
outdata[1:-1, 1:-1] = np.mean(stacked, 2)
print(outdata)


###########################  10.2.3 Zonal Analyses  ###########################

# Function to get histogram bins.
def get_bins(data):
    """Return bin edges for all unique values in data. """
    bins = np.unique(data)
    return np.append(bins[~np.isnan(bins)], max(bins) + 1)

# Load the data from the figure.
os.chdir(os.path.join(data_dir, 'misc'))
landcover = gdal.Open('grid102.tif').ReadAsArray()
zones = gdal.Open('grid101.tif').ReadAsArray()

# Calculate the 2-way histogram.
hist, zone_bins, landcover_bins = np.histogram2d(
    zones.flatten(), landcover.flatten(),
    [get_bins(zones), get_bins(landcover)])
print(hist)


# Example to create a one-dimensional bin instead of the 2-d one in
# listing 10.8.

data_dir = r'D:\osgeopy-data'

# Read in the ecoregion data and get appropriate bins.
os.chdir(os.path.join(data_dir, 'Utah'))

eco_ds = gdal.Open('utah_ecoIII60.tif')
eco_band = eco_ds.GetRasterBand(1)
eco_data = eco_band.ReadAsArray().flatten()
eco_bins = get_bins(eco_data)

lc_ds = gdal.Open('landcover60.tif')
lc_band = lc_ds.GetRasterBand(1)
lc_data = lc_band.ReadAsArray().flatten()
lc_bins = get_bins(lc_data)

# Function to calculate mode.
def my_mode(data):
    return scipy.stats.mode(data)[0]

# Get the histogram.
modes, bins, bn = scipy.stats.binned_statistic(
    eco_data, lc_data, my_mode, eco_bins)
print(modes)
