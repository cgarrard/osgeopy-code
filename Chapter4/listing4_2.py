import os
from osgeo import ogr

def layers_to_feature_dataset(ds_name, gdb_fn, dataset_name):
    """Copy layers to a feature dataset in a file geodatabase."""

    # Open the input datasource.
    in_ds = ogr.Open(ds_name)
    if in_ds is None:
        raise RuntimeError('Could not open datasource')

    # Open the geodatabase or create it if it doesn't exist.
    gdb_driver = ogr.GetDriverByName('FileGDB')
    if os.path.exists(gdb_fn):
        gdb_ds = gdb_driver.Open(gdb_fn, 1)
    else:
        gdb_ds = gdb_driver.CreateDataSource(gdb_fn)
    if gdb_ds is None:
        raise RuntimeError('Could not open file geodatabase')

    # Create an option list so the feature classes will be
    # saved in a feature dataset.
    options = ['FEATURE_DATASET=' + dataset_name]

    # Loop through the layers in the input datasource and copy
    # each one into the geodatabase.
    for i in range(in_ds.GetLayerCount()):
        lyr = in_ds.GetLayer(i)
        lyr_name = lyr.GetName()
        print('Copying ' + lyr_name + '...')
        gdb_ds.CopyLayer(lyr, lyr_name, options)
