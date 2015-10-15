# Script to add an attribute table to a raster.

import os
from osgeo import gdal

# Don't forget to change the folder.
os.chdir(r'D:\osgeopy-data\Switzerland')

# Open the output from listing 9.3 and get the band.
ds = gdal.Open('dem_class2.tif')
band = ds.GetRasterBand(1)

# Change the NoData value to -1 so that the histogram will be computed
# using 0 values.
band.SetNoDataValue(-1)

# Create the raster attribute table and add 3 columns for the pixel value,
# number of pixels with that value, and elevation label.
rat = gdal.RasterAttributeTable()
rat.CreateColumn('Value', gdal.GFT_Integer, gdal.GFU_Name)
rat.CreateColumn('Count', gdal.GFT_Integer, gdal.GFU_PixelCount)
rat.CreateColumn('Elevation', gdal.GFT_String, gdal.GFU_Generic)

# Add 6 rows to the table, for values 0-5.
rat.SetRowCount(6)

# Write the values 0-5 (using range) to the first column (pixel value).
rat.WriteArray(range(6), 0)

# Get the histogram and write the results to the second column (count).
rat.WriteArray(band.GetHistogram(-0.5, 5.5, 6, False, False), 1)

# Add the labels for each pixel value to the third column.
rat.SetValueAsString(1, 2, '0 - 800')
rat.SetValueAsString(2, 2, '800 - 1300')
rat.SetValueAsString(3, 2, '1300 - 2000')
rat.SetValueAsString(4, 2, '2000 - 2600')
rat.SetValueAsString(5, 2, '2600 +')

# Add the attribute table to the raster and restore the NoData value.
band.SetDefaultRAT(rat)
band.SetNoDataValue(0)
del ds
