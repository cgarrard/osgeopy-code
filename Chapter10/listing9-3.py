# Script to add a color table to a raster.

import os
from osgeo import gdal

# Don't forget to change directory.
os.chdir(r'D:\osgeopy-data\Switzerland')

# Create a copy of the raster so you still have the original unmodified.
original_ds = gdal.Open('dem_class.tif')
driver = gdal.GetDriverByName('gtiff')
ds = driver.CreateCopy('dem_class2.tif', original_ds)
band = ds.GetRasterBand(1)

# Create a color table with colors for pixel values 1-5.
colors = gdal.ColorTable()
colors.SetColorEntry(1, (112, 153, 89))
colors.SetColorEntry(2, (242, 238, 162))
colors.SetColorEntry(3, (242, 206, 133))
colors.SetColorEntry(4, (194, 140, 124))
colors.SetColorEntry(5, (214, 193, 156))

# Add the color table to the raster.
band.SetRasterColorTable(colors)
band.SetRasterColorInterpretation(
    gdal.GCI_PaletteIndex)

del band, ds

