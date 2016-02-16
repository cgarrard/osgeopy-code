# Script to extract a spatial subset from a raster.

import os
from osgeo import gdal

# Coordinates for the bounding box to extract.
vashon_ulx, vashon_uly = 532000, 5262600
vashon_lrx, vashon_lry = 548500, 5241500

# Don't forget to change the directory.
os.chdir(r'D:\osgeopy-data\Landsat\Washington')
in_ds = gdal.Open('nat_color.tif')

# Create an inverse geotransform for the raster. This converts real-world
# coordinates to pixel offsets.
in_gt = in_ds.GetGeoTransform()
inv_gt = gdal.InvGeoTransform(in_gt)
if gdal.VersionInfo()[0] == '1':
    if inv_gt[0] == 1:
        inv_gt = inv_gt[1]
    else:
        raise RuntimeError('Inverse geotransform failed')
elif inv_gt is None:
    raise RuntimeError('Inverse geotransform failed')

# Get the offsets that correspond to the bounding box corner coordinates.
offsets_ul = gdal.ApplyGeoTransform(
    inv_gt, vashon_ulx, vashon_uly)
offsets_lr = gdal.ApplyGeoTransform(
    inv_gt, vashon_lrx, vashon_lry)

# The offsets are returned as floating point, but we need integers.
off_ulx, off_uly = map(int, offsets_ul)
off_lrx, off_lry = map(int, offsets_lr)

# Compute the numbers of rows and columns to extract, based on the offsets.
rows = off_lry - off_uly
columns = off_lrx - off_ulx

# Create an output raster with the correct number of rows and columns.
gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('vashon.tif', columns, rows, 3)
out_ds.SetProjection(in_ds.GetProjection())

# Convert the offsets to real-world coordinates for the georeferencing info.
# We can't use the coordinates above because they don't correspond to the
# pixel edges.
subset_ulx, subset_uly = gdal.ApplyGeoTransform(
    in_gt, off_ulx, off_uly)
out_gt = list(in_gt)
out_gt[0] = subset_ulx
out_gt[3] = subset_uly
out_ds.SetGeoTransform(out_gt)

# Loop through the 3 bands.
for i in range(1, 4):
    in_band = in_ds.GetRasterBand(i)
    out_band = out_ds.GetRasterBand(i)

    # Read the data from the input raster starting at the computed offsets.
    data = in_band.ReadAsArray(
        off_ulx, off_uly, columns, rows)

    # Write the data to the output, but no offsets are needed because we're
    # filling the entire image.
    out_band.WriteArray(data)

del out_ds
