# Script to use ground control points to add a geotransform to a raster.

import glob
import math
import os
from osgeo import gdal, osr

# The get_extent function from the text is in ch10funcs.py.
import ch10funcs

# Don't forget to change the directory.
os.chdir(r'D:\osgeopy-data\Massachusetts')

# Get the list of tiffs that start with O.
in_files = glob.glob('O*.tif')

# Loop through all of the files and get the bounding coordinates for the
# whole batch. This will be the output extent.
min_x, max_y, max_x, min_y = ch10funcs.get_extent(in_files[0])
for fn in in_files[1:]:
    minx, maxy, maxx, miny = ch10funcs.get_extent(fn)
    min_x = min(min_x, minx)
    max_y = max(max_y, maxy)
    max_x = max(max_x, maxx)
    min_y = min(min_y, miny)

# Calculate the dimensions for the output based on the output extent.
in_ds = gdal.Open(in_files[0])
gt = in_ds.GetGeoTransform()
rows = math.ceil((max_y - min_y) / -gt[5])
columns = math.ceil((max_x - min_x) / gt[1])

# Create the output dataset.
driver = gdal.GetDriverByName('gtiff')
out_ds = driver.Create('mosaic.tif', columns, rows)
out_ds.SetProjection(in_ds.GetProjection())
out_band = out_ds.GetRasterBand(1)

# Change the upper left coordinates in the geotransform and add it to the
# output image.
gt = list(in_ds.GetGeoTransform())
gt[0], gt[3] = min_x, max_y
out_ds.SetGeoTransform(gt)

# Loop through the input files.
for fn in in_files:
    in_ds = gdal.Open(fn)

    # Create a transformer between this input image and the output mosaic
    # and then use it to calculate the offsets for this raster in the
    # mosaic.
    trans = gdal.Transformer(in_ds, out_ds, [])
    success, xyz = trans.TransformPoint(False, 0, 0)
    x, y, z = map(int, xyz)

    # Copy the data.
    data = in_ds.GetRasterBand(1).ReadAsArray()
    out_band.WriteArray(data, x, y)


# From later in the text, get the real-world coordinates from out_ds at
# column 1078 and row 648.
trans = gdal.Transformer(out_ds, None, [])
success, xyz = trans.TransformPoint(0, 1078, 648)
print(xyz)

del in_ds, out_band, out_ds
