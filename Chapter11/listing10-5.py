# Script to compute slope from a DEM.

import os
import numpy as np
from osgeo import gdal
import ospybook as pb

in_fn = r"D:\osgeopy-data\Nepal\everest_utm.tif"
out_fn = r'D:\Temp\everest_slope.tif'

# Get cell width and height.
in_ds = gdal.Open(in_fn)
cell_width = in_ds.GetGeoTransform()[1]
cell_height = in_ds.GetGeoTransform()[5]

# Read the data into a floating point array.
band = in_ds.GetRasterBand(1)
in_data = band.ReadAsArray().astype(np.float)

# Initialize the output array with -99.
out_data = np.ones((band.YSize, band.XSize)) * -99

# Make the slices.
slices = pb.make_slices(in_data, (3, 3))

# Compute the slope using the equations from the text.
rise = ((slices[6] + (2 * slices[7]) + slices[8]) -
        (slices[0] + (2 * slices[1]) + slices[2])) / \
       (8 * cell_height)
run =  ((slices[2] + (2 * slices[5]) + slices[8]) -
        (slices[0] + (2 * slices[3]) + slices[6])) / \
       (8 * cell_width)
dist = np.sqrt(np.square(rise) + np.square(run))

# The output from the last equation is inserted into the middle
# of the output array, ignoring the edges again.
out_data[1:-1, 1:-1] = np.arctan(dist) * 180 / np.pi

# Save the data.
pb.make_raster(in_ds, out_fn, out_data, gdal.GDT_Float32, -99)
del in_ds
