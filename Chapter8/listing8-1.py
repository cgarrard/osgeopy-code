# Script to stack three 1-band rasters into a a single 3-band image.

import os
from osgeo import gdal

# Be sure to change your directory.
os.chdir(r'D:\osgeopy-data\Landsat\Washington')
band1_fn = 'p047r027_7t20000730_z10_nn10.tif'
band2_fn = 'p047r027_7t20000730_z10_nn20.tif'
band3_fn = 'p047r027_7t20000730_z10_nn30.tif'

# Open band 1.
in_ds = gdal.Open(band1_fn)
in_band = in_ds.GetRasterBand(1)

# Create a 3-band GeoTIFF with the same dimensions, data type, projection,
# and georeferencing info as band 1. This will be overwritten if it exists.
gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('nat_color.tif',
    in_band.XSize, in_band.YSize, 3, in_band.DataType)
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())

# Copy data from band 1 into the output image.
in_data = in_band.ReadAsArray()
out_band = out_ds.GetRasterBand(3)
out_band.WriteArray(in_data)

# Copy data from band 2 into the output image.
in_ds = gdal.Open(band2_fn)
out_band = out_ds.GetRasterBand(2)
out_band.WriteArray(in_ds.ReadAsArray())

# Copy data from band 3 into the output image.
out_ds.GetRasterBand(1).WriteArray(
    gdal.Open(band3_fn).ReadAsArray())

# Compute statistics on each output band.
out_ds.FlushCache()
for i in range(1, 4):
    out_ds.GetRasterBand(i).ComputeStatistics(False)

# Build overview layers for faster display.
out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])

# This will effectively close the file and flush data to disk.
del out_ds
