# Script to calculate slope using SciPy.

import os
import numpy as np
import scipy.ndimage
from osgeo import gdal
import ospybook as pb

in_fn = r"D:\osgeopy-data\Nepal\everest_utm.tif"
out_fn = r'D:\Temp\everest_slope_scipy2.tif'

# Write a function that calculates slope using a 3x3 window.
# This will be passed to the SciPy filter function below.
def slope(data, cell_width, cell_height):
    """Calculates slope using a 3x3 window.

    data        - 1D array containing the 9 pixel values, starting
                  in the upper left and going left to right and down
    cell_width  - pixel width in the same units as the data
    cell_height - pixel height in the same units as the data
    """
    rise = ((data[6] + (2 * data[7]) + data[8]) -
            (data[0] + (2 * data[1]) + data[2])) / \
           (8 * cell_height)
    run =  ((data[2] + (2 * data[5]) + data[8]) -
            (data[0] + (2 * data[3]) + data[6])) / \
           (8 * cell_width)
    dist = np.sqrt(np.square(rise) + np.square(run))
    return np.arctan(dist) * 180 / np.pi

# Read the data as floating point.
in_ds = gdal.Open(in_fn)
in_band = in_ds.GetRasterBand(1)
in_data = in_band.ReadAsArray().astype(np.float32)

cell_width = in_ds.GetGeoTransform()[1]
cell_height = in_ds.GetGeoTransform()[5]

# Pass your slope function, along with the pixel size, to the
# generic_filter function. This will apply your function to
# each window, and each time it will pass the extra arguments
# in to the function along with the data.
out_data = scipy.ndimage.filters.generic_filter(
    in_data, slope, size=3, mode='nearest',
    extra_arguments=(cell_width, cell_height))

# Save the output
pb.make_raster(in_ds, out_fn, out_data, gdal.GDT_Float32)
del in_ds
