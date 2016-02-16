# Script to resample a raster to a larger pixel size using byte sequences.

import os
import numpy as np
from osgeo import gdal

# Don't forget to change the folder.
os.chdir(r'D:\osgeopy-data\Landsat\Washington')

# Open the input raster.
in_ds = gdal.Open('nat_color.tif')

# Computer the number of output rows and columns (half the input numbers
# because we're making the pixels twice as big).
out_rows = int(in_ds.RasterYSize / 2)
out_columns = int(in_ds.RasterXSize / 2)
num_bands = in_ds.RasterCount

# Create the output raster using the computed dimensions.
gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('nat_color_resampled.tif',
    out_columns, out_rows, num_bands)

# Change the geotransform so it reflects the larger cell size before
# setting it onto the output.
out_ds.SetProjection(in_ds.GetProjection())
geotransform = list(in_ds.GetGeoTransform())
geotransform[1] *= 2
geotransform[5] *= 2
out_ds.SetGeoTransform(geotransform)

# Read in the data for all bands, but have gdal resample it so that it has
# the specified number of rows and columns instead of the numbers that the
# input has. This effectively resizes the pixels.
data = in_ds.ReadRaster(
    buf_xsize=out_columns, buf_ysize=out_rows)

# Write the data to the output raster.
out_ds.WriteRaster(0, 0, out_columns, out_rows, data)

# Compute statistics and build overviews.
out_ds.FlushCache()
for i in range(num_bands):
    out_ds.GetRasterBand(i + 1).ComputeStatistics(False)
out_ds.BuildOverviews('average', [2, 4, 8, 16])

del out_ds
