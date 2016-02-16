# Script to resample a raster to a smaller pixel size.

import os
from osgeo import gdal

# Don't forget to change the folder.
os.chdir(r'D:\osgeopy-data\Landsat\Washington')

# Open the input raster.
in_ds = gdal.Open('p047r027_7t20000730_z10_nn10.tif')
in_band = in_ds.GetRasterBand(1)

# Computer the number of output rows and columns (double the input numbers
# because we're cutting pixel size in half).
out_rows = in_band.YSize * 2
out_columns = in_band.XSize * 2

# Create the output raster using the computed dimensions.
gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('band1_resampled.tif',
    out_columns, out_rows)

# Change the geotransform so it reflects the smaller cell size before
# setting it onto the output.
out_ds.SetProjection(in_ds.GetProjection())
geotransform = list(in_ds.GetGeoTransform())
geotransform[1] /= 2
geotransform[5] /= 2
out_ds.SetGeoTransform(geotransform)

# Read in the data, but have gdal resample it so that it has the specified
# number of rows and columns instead of the numbers that the input has.
# This effectively resizes the pixels.
data = in_band.ReadAsArray(
    buf_xsize=out_columns, buf_ysize=out_rows)

# Write the data to the output raster.
out_band = out_ds.GetRasterBand(1)
out_band.WriteArray(data)

# Compute statistics and build overviews.
out_band.FlushCache()
out_band.ComputeStatistics(False)
out_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64])

del out_ds
