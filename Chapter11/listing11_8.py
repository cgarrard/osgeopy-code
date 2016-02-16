# Script to run a smoothing filter in chunks.

import os
import numpy as np
from osgeo import gdal
import ospybook as pb

in_fn = r"D:\osgeopy-data\Nepal\everest.tif"
out_fn = r'D:\Temp\everest_smoothed_chunks.tif'

# Open the input.
in_ds = gdal.Open(in_fn)
in_band = in_ds.GetRasterBand(1)
xsize = in_band.XSize
ysize = in_band.YSize

# Create the empty output raster.
driver = gdal.GetDriverByName('GTiff')
out_ds = driver.Create(out_fn, xsize, ysize, 1, gdal.GDT_Int32)
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())
out_band = out_ds.GetRasterBand(1)
out_band.SetNoDataValue(-99)

# Loop through the rows 100 at a time.
n = 100
for i in range(0, ysize, n):

    # Figure out how many rows can be read. Remember we want to read n + 2
    # rows if possible.
    if i + n + 1 < ysize:
        rows = n + 2
    else:
        rows = ysize - i

    # This makes sure we don't try to read off the top edge the first time
    # through.
    yoff = max(0, i - 1)

    # Read and process the data as before.
    in_data = in_band.ReadAsArray(0, yoff, xsize, rows)
    slices = pb.make_slices(in_data, (3, 3))
    stacked_data = np.ma.dstack(slices)
    out_data = np.ones(in_data.shape, np.int32) * -99
    out_data[1:-1, 1:-1] = np.mean(stacked_data, 2)

    # If it's the first time through, write the entire output array
    # starting at the first row. Otherwise, don't write the first row of
    # the output array because we don't want to overwrite good data from
    # the previous chunk. Because we're ignoring this first row, the row
    # offset needs to be increased.
    if yoff == 0:
        out_band.WriteArray(out_data)
    else:
        out_band.WriteArray(out_data[1:], 0, yoff + 1)

# Finish up.
out_band.FlushCache()
out_band.ComputeStatistics(False)

del out_ds, in_ds
