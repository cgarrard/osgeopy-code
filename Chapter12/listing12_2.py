# Script to perform K-means clustering with Spectral Python.

import os
import numpy as np
import spectral
from osgeo import gdal
import ospybook as pb

folder = r'D:\osgeopy-data\Landsat\Utah'
raster_fns = ['LE70380322000181EDC02_60m.tif',
              'LE70380322000181EDC02_TIR_60m.tif']
out_fn = 'kmeans_prediction_60m.tif'

# Stack the bands and run the analysis.
os.chdir(folder)
data = pb.stack_bands(raster_fns)
classes, centers = spectral.kmeans(data)

# Save the output.
ds = gdal.Open(raster_fns[0])
out_ds = pb.make_raster(ds, out_fn, classes, gdal.GDT_Byte)
levels = pb.compute_overview_levels(out_ds.GetRasterBand(1))
out_ds.BuildOverviews('NEAREST', levels)
out_ds.FlushCache()
out_ds.GetRasterBand(1).ComputeStatistics(False)

del out_ds, ds
