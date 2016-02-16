import os
import numpy as np
from osgeo import gdal


# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
data_dir = r'D:\osgeopy-data'
# data_dir =



########################  9.3 Reading partial datasets  #######################

# Open a Landsat band.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
ds = gdal.Open('p047r027_7t20000730_z10_nn10.tif')
band = ds.GetRasterBand(1)

# Read in 3 rows and 6 columns starting at row 6000 and column 1400.
data = band.ReadAsArray(1400, 6000, 6, 3)
print(data)

# Convert the data to floating point using numpy.
data = band.ReadAsArray(1400, 6000, 6, 3).astype(float)
print(data)

# Or convert them to float by reading them into a floating point array.
data = np.empty((3, 6), dtype=float)
band.ReadAsArray(1400, 6000, 6, 3, buf_obj=data)
print(data)

# Write these few pixels to the middle of a tiny dummy raster (this
# isn't exactly like the text example because that would be hard to see
# what actually happened). You'll be able to see it best if you open the
# output in GIS software.
test_ds = gdal.GetDriverByName('GTiff').Create('test.tif', 10, 10)
band2 = test_ds.GetRasterBand(1)
band2.WriteArray(data, 4, 6)
del test_ds


########################  Access window out of range  #########################

# Try reading 5 rows and columns from the test image you just made, but
# start at row 8 and column 2. This will fail because it's trying to read
# rows 8 through 13, but there are only 10 rows.
ds = gdal.Open('test.tif')
band = ds.GetRasterBand(1)
data = band.ReadAsArray(8, 2, 5, 5)

# What happens if you try to write more data than there is room for? First
# create an array of fake data.
data = np.reshape(np.arange(25), (5,5))
print(data)

# Now try to write it into the same area we just failed to read data from.
# That fails, too.
band.WriteArray(data, 8, 2)


#####################  9.3.1 Using real-world coordinates  ####################

# Get the geotransform from one of the Landsat bands.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
ds = gdal.Open('p047r027_7t20000730_z10_nn10.tif')
band = ds.GetRasterBand(1)
gt = ds.GetGeoTransform()
print(gt)

# Now get the inverse geotransform. The original can be used to convert
# offsets to real-world coordinates, and the inverse can be used to convert
# real-world coordinates to offsets.

# GDAL 1.x: You get a success flag and the geotransform.
success, inv_gt = gdal.InvGeoTransform(gt)
print(success, inv_gt)

# GDAL 2.x: You get the geotransform or None
inv_gt = gdal.InvGeoTransform(gt)
print(inv_gt)

# Use the inverset geotransform to get some pixel offsets from real-world
# UTM coordinates (since that's what the Landsat image uses). The offsets
# are returned as floating point.
offsets = gdal.ApplyGeoTransform(inv_gt, 465200, 5296000)
print(offsets)

# Convert the offsets to integers.
xoff, yoff = map(int, offsets)
print(xoff, yoff)

# And use them to read a pixel value.
value = band.ReadAsArray(xoff, yoff, 1, 1)[0,0]
print(value)

# Reading in one pixel at a time is really inefficient if you need to read
# a lot of pixels, though, so here's how you could do it by reading in all
# of the pixel values first and then pulling out the one you need.
data = band.ReadAsArray()
x, y = map(int, gdal.ApplyGeoTransform(inv_gt, 465200, 5296000))
value = data[yoff, xoff]
print(value)


############################  9.3.2 Resampling data  ##########################

# Get the first band from the raster created with listing 8.1.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
ds = gdal.Open('nat_color.tif')
band = ds.GetRasterBand(1)

# Read in 2 rows and 3 columns.
original_data = band.ReadAsArray(1400, 6000, 3, 2)
print(original_data)

# Now resample those same 2 rows and 3 columns to a smaller pixel size by
# doubling the number of rows and columns to read (now 4 rows and 6 columns).
resampled_data = band.ReadAsArray(1400, 6000, 3, 2, 6, 4)
print(resampled_data)

# Read in 4 rows and 6 columns.
original_data2 = band.ReadAsArray(1400, 6000, 6, 4)
print(original_data2)

# Now resample those same 4 rows and 6 columns to a larger pixel size by
# halving the number of rows and columns to read (now 2 rows and 3 columns).
resampled_data2 = np.empty((2, 3), np.int)
band.ReadAsArray(1400, 6000, 6, 4, buf_obj=resampled_data2)
print(resampled_data2)



#############################  9.4 Byte sequences  ############################

# Read a few pixels as a byte string from the raster created with listing 8.1.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
ds = gdal.Open('nat_color.tif')
data = ds.ReadRaster(1400, 6000, 2, 2, band_list=[1])
print(data)

# Pull the first value out. It will be converted from a byte string to a
# number.
print(data[0])

# Try to change the value of that first pixel. This will fail because you
# can't change byte strings.
data[0] = 50

# Convert the byte string to a byte array and then change the first value.
bytearray_data = bytearray(data)
bytearray_data[0] = 50
print(bytearray_data[0])

# Convert the byte string to tuple of pixel values.
import struct
tuple_data = struct.unpack('B' * 4, data)
print(tuple_data)

# Convert the tuple to a numpy array.
numpy_data1 = np.array(tuple_data)
print(numpy_data1)

# Conver the byte string to a numpy array.
numpy_data2 = np.fromstring(data, np.int8)
print(numpy_data2)

# Reshape one of the numpy arrays so it has 2 rows and 2 columns, just like
# the original data we read in.
reshaped_data = np.reshape(numpy_data2, (2,2))
print(reshaped_data)

# Write our little byte string to the middle of a tiny dummy raster (this
# isn't exactly like the text example because that would be hard to see
# what actually happened). You'll be able to see it best if you open the
# output in GIS software.
test_ds = gdal.GetDriverByName('GTiff').Create('test2.tif', 10, 10)
test_ds.WriteRaster(4, 6, 2, 2, data, band_list=[1])
del test_ds



###############################  9.5 Subdatasets  #############################

# Get the subdatasets from a MODIS file.
os.chdir(os.path.join(data_dir, 'Modis'))
ds = gdal.Open('MYD13Q1.A2014313.h20v11.005.2014330092746.hdf')
subdatasets = ds.GetSubDatasets()
print('Number of subdatasets: {}'.format(len(subdatasets)))
for sd in subdatasets:
    print('Name: {0}\nDescription:{1}\n'.format(*sd))

# Open the the first subdataset in the Modis file.
ndvi_ds = gdal.Open(subdatasets[0][0])

# Make sure that it worked by by printing out the dimensions. You can use
# ndvi_ds just like any other dataset.
print('Dataset dimensions: {} {}'.format(ndvi_ds.RasterXSize, ndvi_ds.RasterYSize))

# For example, you still need to get the band before you can read data.
ndvi_band = ndvi_ds.GetRasterBand(1)
print('Band dimensions: {} {}'.format(ndvi_band.XSize, ndvi_band.YSize))



###################################  9.6 WMS  #################################

ds = gdal.Open('listing9_6.xml')
gdal.GetDriverByName('PNG').CreateCopy(r'D:\Temp\liberty.png', ds)
