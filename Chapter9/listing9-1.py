# Script to add ground control points to a raster.

import os
import shutil
from osgeo import gdal, osr

# Don't forget to change the directory.
# Make a copy of the original image so we're leaving it alone and changing
# the new one. Try opening the original in a GIS. It doesn't have any
# SRS info and the upper left corner should have coordinates of 0,0.
os.chdir(r'D:\osgeopy-data\Utah')
shutil.copy('cache_no_gcp.tif', 'cache.tif')

# Open the copied image so we can add GCPs to it.
ds = gdal.Open('cache.tif', gdal.GA_Update)

# Create the SRS that the GCP coordinates use.
sr = osr.SpatialReference()
sr.SetWellKnownGeogCS('WGS84')

# Create the list of GCPs.
gcps = [gdal.GCP(-111.931075, 41.745836, 0, 1078, 648),
        gdal.GCP(-111.901655, 41.749269, 0, 3531, 295),
        gdal.GCP(-111.899180, 41.739882, 0, 3722, 1334),
        gdal.GCP(-111.930510, 41.728719, 0, 1102, 2548)]

# Add the GCPs to the raster
ds.SetGCPs(gcps, sr.ExportToWkt())
ds.SetProjection(sr.ExportToWkt())
ds = None



###############################################################################

# This time we'll use the driver to make a copy of the raster and then add
# a geotransform instead of GCPs. This still uses the sr and gcps variables
# from above.
old_ds = gdal.Open('cache_no_gcp.tif')
ds = old_ds.GetDriver().CreateCopy('cache2.tif', old_ds)
ds.SetProjection(sr.ExportToWkt())
ds.SetGeoTransform(gdal.GCPsToGeoTransform(gcps))
del ds, old_ds
