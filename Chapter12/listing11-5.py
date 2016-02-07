# Function to retrieve overview data from a raster.

import gdal

def get_overview_data(fn, band_index=1, level=-1):
    """Returns an array containing data from an overview.

    fn         - path to raster file
    band_index - band number to get overview for
    level      - overview level, where 1 is the highest resolution;
                 the coarsest can be retrieved with -1
    """
    ds = gdal.Open(fn)
    band = ds.GetRasterBand(band_index)
    if level > 0:
        ov_band = band.GetOverview(level)
    else:
        num_ov = band.GetOverviewCount()
        ov_band = band.GetOverview(num_ov + level)
    return ov_band.ReadAsArray()
