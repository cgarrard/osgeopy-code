# Script that uses SciPy to smooth a DEM.

import os
import scipy.ndimage
from osgeo import gdal
import ospybook as pb

in_fn = r"D:\osgeopy-data\Nepal\everest.tif"
out_fn = r'D:\Temp\everest_smoothed.tif'

in_ds = gdal.Open(in_fn)
in_data = in_ds.GetRasterBand(1).ReadAsArray()

# Use SciPy to run a 3x3 filter.
out_data = scipy.ndimage.filters.uniform_filter(
    in_data, size=3, mode='nearest')

pb.make_raster(in_ds, out_fn, out_data, gdal.GDT_Int32)
del in_ds
