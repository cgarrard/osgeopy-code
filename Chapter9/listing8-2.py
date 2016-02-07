# Script to convert an elevation raster from meters to feet,
# one block at a time.

import os
import numpy as np
from osgeo import gdal

# Don't forget to change your directory.
os.chdir(r'D:\osgeopy-data\Washington\dem')

# Open the input raster and get its dimensions.
in_ds = gdal.Open('gt30w140n90.tif')
in_band = in_ds.GetRasterBand(1)
xsize = in_band.XSize
ysize = in_band.YSize

# Get the block size and NoData value.
block_xsize, block_ysize = in_band.GetBlockSize()
nodata = in_band.GetNoDataValue()

# Create an output file with the same dimensions and data type.
out_ds = in_ds.GetDriver().Create(
    'dem_feet.tif', xsize, ysize, 1, in_band.DataType)
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())
out_band = out_ds.GetRasterBand(1)

# Loop through the blocks in the x direction.
for x in range(0, xsize, block_xsize):

    # Get the number of columns to read.
    if x + block_xsize < xsize:
        cols = block_xsize
    else:
        cols = xsize - x

    # Loop through the blocks in the y direction.
    for y in range(0, ysize, block_ysize):

        # Get the number of rows to read.
        if y + block_ysize < ysize:
            rows = block_ysize
        else:
            rows = ysize - y

        # Read in one block's worth of data, convert it to feet, and then
        # write the results out to the same block location in the output.
        data = in_band.ReadAsArray(x, y, cols, rows)
        data = np.where(data == nodata, nodata, data * 3.28084)
        out_band.WriteArray(data, x, y)

# Compute statistics after flushing the cache and setting the NoData value.
out_band.FlushCache()
out_band.SetNoDataValue(nodata)
out_band.ComputeStatistics(False)
out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])
del out_ds
