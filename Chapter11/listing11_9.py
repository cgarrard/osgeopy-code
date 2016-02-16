# Zonal analysis with SciPy

import os
import numpy as np
import scipy.stats
from osgeo import gdal

def get_bins(data):
    """Return bin edges for all unique values in data."""
    bins = np.unique(data)
    return np.append(bins, max(bins) + 1)

os.chdir(r'D:\osgeopy-data\Utah')
landcover_fn = 'landcover60.tif'
ecoregion_fn = 'utah_ecoIII60.tif'
out_fn = r'D:\Temp\histogram.csv'

# Read in the ecoregion data and get appropriate bins.
eco_ds = gdal.Open(ecoregion_fn)
eco_band = eco_ds.GetRasterBand(1)
eco_data = eco_band.ReadAsArray().flatten()
eco_bins = get_bins(eco_data)

# Read in the landcover data and get appropriate bins.
lc_ds = gdal.Open(landcover_fn)
lc_band = lc_ds.GetRasterBand(1)
lc_data = lc_band.ReadAsArray().flatten()
lc_bins = get_bins(lc_data)

# Calculate the histogram.
hist, eco_bins2, lc_bins2, bn = \
    scipy.stats.binned_statistic_2d(
        eco_data, lc_data, lc_data, 'count',
        [eco_bins, lc_bins])

# Add bin information to the histogram so the output file
# is more useful.
hist = np.insert(hist, 0, lc_bins[:-1], 0)
row_labels = np.insert(eco_bins[:-1], 0, 0)
hist = np.insert(hist, 0, row_labels, 1)

# Save the output
np.savetxt(out_fn, hist, fmt='%1.0f', delimiter=',')
