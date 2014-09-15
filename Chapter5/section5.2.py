import os
import sys

from osgeo import ogr

import ospybook as pb

# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
data_dir = r'D:\osgeopy-data'
# data_dir =


##################  5.2.1  Opening datasource fors writing######################

original_fn = os.path.join(data_dir, 'Washington', 'large_cities2.shp')
new_fn = os.path.join(data_dir, 'output', 'large_cities2.shp')

# First make a copy of a shapefile so you something to test things on.
pb.copy_datasource(original_fn, new_fn)

# Open the copied shapefile for writing.
ds = ogr.Open(new_fn, 1)
if ds is None:
    sys.exit('Could not open {0}.'.format(new_fn))
lyr = ds.GetLayer(0)

# Take a look at the attributes before you change anything.
print('Original attributes')
pb.print_attributes(lyr, geom=False)


##################  5.2.2   Changing the layer definition  #####################

# Add a field to the shapefile you just opened.
lyr.CreateField(ogr.FieldDefn('ID', ogr.OFTInteger))

# Change the name of the "Name" attribute field by creating a new field
# definition and using it to alter the existing field.
i = lyr.GetLayerDefn().GetFieldIndex('Name')
fld_defn = ogr.FieldDefn('City_Name', ogr.OFTString)
lyr.AlterFieldDefn(i, fld_defn, ogr.ALTER_NAME_FLAG)

# Change the name of the POINT_X field to X_coord and the precision to 4
# decimal places. Need to make sure that the width is big enough or things
# don't work right, so set it to the original width to be safe.
lyr_defn = lyr.GetLayerDefn()
i = lyr_defn.GetFieldIndex('X')
width = lyr_defn.GetFieldDefn(i).GetWidth()
fld_defn = ogr.FieldDefn('X_coord', ogr.OFTReal)
fld_defn.SetWidth(width)
fld_defn.SetPrecision(1)
flag = ogr.ALTER_NAME_FLAG + ogr.ALTER_WIDTH_PRECISION_FLAG
lyr.AlterFieldDefn(i, fld_defn, flag)

# # A slightly different method to change the name of the POINT_X field to
# # X_coord and the precision to 4 decimal places. Copy the original field
# # defintion and use it. This uses the built-in Python copy module. If you do
# # not copy the FieldDefn and instead try to use the original, you will
# # probably get weird results.
# import copy
# lyr_defn = lyr.GetLayerDefn()
# i = lyr_defn.GetFieldIndex('X')
# fld_defn = copy.copy(lyr_defn.GetFieldDefn(i))
# fld_defn.SetName('X_coord')
# fld_defn.SetPrecision(1)
# flag = ogr.ALTER_NAME_FLAG + ogr.ALTER_WIDTH_PRECISION_FLAG
# lyr.AlterFieldDefn(i, fld_defn, flag)

# Take a look at the attributes now. The precision won't be affected yet, but
# the field names should be changed and there should be a blank ID field.
print('\nNew field names and empty ID field')
pb.print_attributes(lyr, geom=False)


##############  5.2.3   Updating, adding, and deleting features  ###############

# Add a unique ID to each feature.
n = 1
for feat in lyr:
    feat.SetField('ID', n)
    lyr.SetFeature(feat)
    n += 1
print('\nID has been added and precision has taken effect')
pb.print_attributes(lyr, geom=False)

# Add a new feature for Redmond. Notice that we have to use the new field name
# for the x coordinate.
feat = ogr.Feature(lyr.GetLayerDefn())
pt = ogr.CreateGeometryFromWkt('POINT (-122.12 47.67)')
feat.SetGeometry(pt)
feat.SetField('City_Name', 'Redmond')
feat.SetField('X_coord', pt.GetX())
feat.SetField('Y', pt.GetY())
feat.SetField('ID', n)
lyr.CreateFeature(feat)
print('\nRedmond has been added')
pb.print_attributes(lyr, geom=False)

# Delete Seattle. Notice that although it doesn't print the record for Seattle,
# it still thinks there are 14 features.
for feat in lyr:
    if feat.GetField('City_Name') == 'Seattle':
        lyr.DeleteFeature(feat.GetFID())
print('\nSeattle deleted')
pb.print_attributes(lyr, geom=False)

# Pack the database in order to get rid of that ghost feature, and recompute
# the spatial extent.
ds.ExecuteSQL('REPACK ' + lyr.GetName())
ds.ExecuteSQL('RECOMPUTE EXTENT ON ' + lyr.GetName())
print('\nDatabase packed')
pb.print_attributes(lyr, geom=False)


#######################  5.2.4 Testing capabilities  ###########################

# Test if you can create a new shapefile in a folder opened for reading only.
dirname = os.path.join(data_dir, 'global')
ds = ogr.Open(dirname)
print(ds.TestCapability(ogr.ODsCCreateLayer))

# Test if you can create a new shapefile in a folder opened for writing.
ds = ogr.Open(dirname, 1)
print(ds.TestCapability(ogr.ODsCCreateLayer))


################## Listing 5.2 modified to test capabilities  ##################

import os
import sys
from osgeo import ogr
import ospybook as pb

original_fn = os.path.join(data_dir, 'Washington', 'large_cities2.shp')
new_fn = os.path.join(data_dir, 'output', 'large_cities2.shp')
pb.copy_datasource(original_fn, new_fn)

# Print attributes before editing.
pb.print_attributes(new_fn, geom=False)

# Pass a 1 to open for writing.
# ds = ogr.Open(new_fn)
ds = ogr.Open(new_fn, 1)
if ds is None:
    sys.exit('Could not open {0}.'.format(new_fn))
lyr = ds.GetLayer(0)

# Test capabilities. Try opening ds for read only and see what happens.
if not lyr.TestCapability(ogr.OLCCreateField):
    raise RuntimeError('Cannot create fields.')
if not lyr.TestCapability(ogr.OLCAlterFieldDefn):
    raise RuntimeError('Cannot alter fields.')
if not lyr.TestCapability(ogr.OLCDeleteFeature):
    raise RuntimeError('Cannot delete features.')

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


################## Use the ospybook print_capabilities function  ###############

driver = ogr.GetDriverByName('ESRI Shapefile')
pb.print_capabilities(driver)
