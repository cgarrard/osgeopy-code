# Script to smooth an elevation dataset.

import os
import numpy as np
from osgeo import gdal
import ospybook as pb

in_fn = r"D:\osgeopy-data\Nepal\everest.tif"
out_fn = r'D:\Temp\everest_smoothed_edges.tif'

in_ds = gdal.Open(in_fn)
in_band = in_ds.GetRasterBand(1)
in_data = in_band.ReadAsArray()

# Stack the slices
slices = pb.make_slices(in_data, (3, 3))
stacked_data = np.ma.dstack(slices)

rows, cols = in_band.YSize, in_band.XSize

# Initialize an output array to the NoData value (-99)
out_data = np.ones((rows, cols), np.int32) * -99

# Put the result into the middle of the output, leaving the
# outside rows and columns alone, so they still have -99.
out_data[1:-1, 1:-1] = np.mean(stacked_data, 2)

pb.make_raster(in_ds, out_fn, out_data, gdal.GDT_Int32, -99)
del in_ds
