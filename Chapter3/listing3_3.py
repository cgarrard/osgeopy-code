# Script to extract certain features from a shapefile and save them to
# another file.

import sys
from osgeo import ogr

# Open the folder dataa source for writing
ds = ogr.Open(r'D:\osgeopy-data\global', 1)
if ds is None:
    sys.exit('Could not open folder.')

# Get the input shapefile
in_lyr = ds.GetLayer('ne_50m_populated_places')

# Create a point layer
if ds.GetLayer('capital_cities'):
    ds.DeleteLayer('capital_cities')
out_lyr = ds.CreateLayer('capital_cities',
                         in_lyr.GetSpatialRef(),
                         ogr.wkbPoint)
out_lyr.CreateFields(in_lyr.schema)

# Create a blank feature
out_defn = out_lyr.GetLayerDefn()
out_feat = ogr.Feature(out_defn)

for in_feat in in_lyr:
    if in_feat.GetField('FEATURECLA') == 'Admin-0 capital':

        # Copy geometry and attributes
        geom = in_feat.geometry()
        out_feat.SetGeometry(geom)
        for i in range(in_feat.GetFieldCount()):
            value = in_feat.GetField(i)
            out_feat.SetField(i, value)

        # Insert the feature
        out_lyr.CreateFeature(out_feat)

# Close files
del ds
