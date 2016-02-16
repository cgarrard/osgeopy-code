# Script to compute NDVI.

import os
import numpy as np
from osgeo import gdal
import ospybook as pb

os.chdir(r'D:\osgeopy-data\Massachusetts')
in_fn = 'm_4207162_ne_19_1_20140718_20140923_clip.tif'
out_fn = 'ndvi.tif'

ds = gdal.Open(in_fn)
red = ds.GetRasterBand(1).ReadAsArray().astype(np.float)
nir = ds.GetRasterBand(4).ReadAsArray()

# Mask the red band.
red = np.ma.masked_where(nir + red == 0, red)

# Do the calculation.
ndvi = (nir - red) / (nir + red)

# Fill the empty cells.
ndvi = ndvi.filled(-99)

# Set NoData to the fill value when creating the new raster.
out_ds = pb.make_raster(
    ds, out_fn, ndvi, gdal.GDT_Float32, -99)

overviews = pb.compute_overview_levels(out_ds.GetRasterBand(1))
out_ds.BuildOverviews('average', overviews)
del ds, out_ds
