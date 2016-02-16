import numpy as np

def get_indices(source_ds, target_width, target_height):
    """Returns x, y lists of all possible resampling offsets.

    source_ds     - dataset to get offsets from
    target_width  - target pixel width
    target_height - target pixel height (negative)
    """
    source_geotransform = source_ds.GetGeoTransform()
    source_width = source_geotransform[1]
    source_height = source_geotransform[5]
    dx = target_width / source_width
    dy = target_height / source_height
    target_x = np.arange(dx / 2, source_ds.RasterXSize, dx)
    target_y = np.arange(dy / 2, source_ds.RasterYSize, dy)
    return np.meshgrid(target_x, target_y)
