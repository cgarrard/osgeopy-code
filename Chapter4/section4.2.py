import os
from osgeo import ogr

# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
# data_dir = r'D:\osgeopy-data'
data_dir =


#########################  4.2 Reading vector data  ############################

#########################  4.2.1 The basics  ###################################

# Try to open the large_cities data source.
fn = os.path.join(data_dir, 'Washington', 'large_cities.geojson')
ds = ogr.Open(fn, 0)
if ds is None:
    sys.exit('Could not open {0}.'.format(fn))
print(ds)

# Get the layer from the large_cities.geojson file.
lyr = ds.GetLayer(0)
print(lyr)

# Print out information about each feature. Note that the output may be
# surrounded by parenthesis if you are using Python 2.7.
ds = ogr.Open(fn, 0)
lyr = ds.GetLayer(0)
for feat in lyr:
    pt = feat.geometry()
    x = pt.GetX()
    y = pt.GetY()
    name = feat.GetField('Name')
    pop = feat.GetField('Population')
    print(name, pop, x, y)

# Use GetFieldAsString.
ds = ogr.Open(fn, 0)
lyr = ds.GetLayer(0)
for feat in lyr:
    pt = feat.geometry()
    x = pt.GetX()
    y = pt.GetY()
    name = feat.GetFieldAsString('Name')
    pop = feat.GetFieldAsString('Population')
    print(name + ' has a population of ' + pop)


#########################  4.2.2 Accessing specific features  ##################

# Make sure we can open the data source for the examples.
fn = os.path.join(data_dir, 'Washington', 'large_cities.geojson')
ds = ogr.Open(fn, 0)
if ds is None:
    sys.exit('Could not open {0}.'.format(fn))

# Print out every other feature in a layer.
ds = ogr.Open(fn, 0)
lyr = ds.GetLayer(0)
for i in range(0, lyr.GetFeatureCount(), 2):
    print(lyr.GetFeature(i).GetField('Name'))

# Skip the first 10 features but print out the rest.
ds = ogr.Open(fn, 0)
lyr = ds.GetLayer(0)
lyr.GetFeature(9)
for feat in lyr:
    print(feat.GetField('Name'))

# Test what happens if you try to loop through a layer twice. The second
# loop should not print anything. (This is actually why we reopen the data
# source and get the layer for each little code snippet. If you ran them all
# at once without doing that, they wouldn't work.)
ds = ogr.Open(fn, 0)
lyr = ds.GetLayer(0)
print('First loop')
for feat in lyr:
    print(feat.GetField('Name'), feat.GetField('Population'))
print('Second loop')
for feat in lyr:
    pt = feat.geometry()
    print(feat.GetField('Name'), pt.GetX(), pt.GetY())

# # But it will if you reset reading first.
ds = ogr.Open(fn, 0)
lyr = ds.GetLayer(0)
print('First loop')
for feat in lyr:
    print(feat.GetField('Name'), feat.GetField('Population'))
print('Second loop')
lyr.ResetReading()
for feat in lyr:
    pt = feat.geometry()
    print(feat.GetField('Name'), pt.GetX(), pt.GetY())
