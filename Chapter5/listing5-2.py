import os
import sys

from osgeo import ogr

import ospybook as pb

# Make sure you change these paths!
original_fn = r'D:\osgeopy-data\Washington\large_cities2.shp'
new_fn = r'D:\osgeopy-data\output\large_cities2.shp'

# Work with a copy instead of the original.
pb.copy_datasource(original_fn, new_fn)

# Print attributes before editing.
pb.print_attributes(new_fn, geom=False)

# Pass a 1 to open for writing.
ds = ogr.Open(new_fn, 1)
if ds is None:
    sys.exit('Could not open {0}.'.format(new_fn))
lyr = ds.GetLayer(0)

# Change a field name.
i = lyr.GetLayerDefn().GetFieldIndex('Name')
fld_defn = ogr.FieldDefn('City_Name', ogr.OFTString)
lyr.AlterFieldDefn(i, fld_defn, ogr.ALTER_NAME_FLAG)

# Add a new field.
lyr.CreateField(ogr.FieldDefn('ID', ogr.OFTInteger))

n = 1
for feat in lyr:
    if feat.GetField('City_Name') == 'Seattle':
        # Delete the Seattle feature.
        lyr.DeleteFeature(feat.GetFID())
    else:
        # Update all other features.
        feat.SetField('ID', n)
        lyr.SetFeature(feat)
        n += 1

# Add a new feature for Redmond.
feat = ogr.Feature(lyr.GetLayerDefn())
pt = ogr.CreateGeometryFromWkt('POINT (-122.12 47.67)')
feat.SetGeometry(pt)
feat.SetField('City_Name', 'Redmond')
feat.SetField('X', pt.GetX())
feat.SetField('Y', pt.GetY())
feat.SetField('ID', n)
lyr.CreateFeature(feat)

# Shapefile housekeeping.
ds.ExecuteSQL('REPACK ' + lyr.GetName())
ds.ExecuteSQL('RECOMPUTE EXTENT ON ' + lyr.GetName())

# Print attributes after editing.
pb.print_attributes(lyr, geom=False)
