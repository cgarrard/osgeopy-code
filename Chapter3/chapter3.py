# I use the print function in this code, even though I don't in the book text,
# so that you can run it as a regular script and still get the output. You only
# get output without using print if you're using the interactive window.


# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
import os
import sys
data_dir = r'D:\osgeopy-data'
# data_dir =



##########################  3.2 Introduction to OGR  ##########################

# Import the module.
from osgeo import ogr

# Get the GeoJSON driver.
driver = ogr.GetDriverByName('GeoJSON')
print(driver)

# It's not case sensitive, so this also works.
driver = ogr.GetDriverByName('geojson')
print(driver)

# This does not work because the real name is 'Esri shapefile'.
driver = ogr.GetDriverByName('shapefile')
print(driver)

# Print out a list of drivers.
import ospybook as pb
pb.print_drivers()



###########################  3.3 Reading vector data  #########################

####################  3.3.1 Accessing specific features  ######################

# Open the data source for the examples.
fn = os.path.join(data_dir, 'global', 'ne_50m_populated_places.shp')
ds = ogr.Open(fn, 0)
if ds is None:
    sys.exit('Could not open {0}.'.format(fn))
lyr = ds.GetLayer(0)

# Get the total number of features and the last one.
num_features = lyr.GetFeatureCount()
last_feature = lyr.GetFeature(num_features - 1)
print(last_feature.NAME)

# Test what happens if you try to loop through a layer twice. The second
# loop should not print anything. (This is actually why in later examples we
# reopen the data source and get the layer for each little code snippet.
# If you ran them all at once without doing that, they wouldn't work.)
fn = os.path.join(data_dir, 'Washington', 'large_cities.geojson')
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
lyr.ResetReading() # This is the important line.
for feat in lyr:
    pt = feat.geometry()
    print(feat.GetField('Name'), pt.GetX(), pt.GetY())


#########################  3.3.2 Viewing your data  ###########################

# Print name and population attributes.
import ospybook as pb
fn = os.path.join(data_dir, 'global', 'ne_50m_populated_places.shp')
pb.print_attributes(fn, 3, ['NAME', 'POP_MAX'])

# Turn off geometries but skip field list parameters that come before the
# "geom" one.
pb.print_attributes(fn, 3, geom=False)

# If you want to see what happens without the "geom" keyword in the last
# example, try this:
pb.print_attributes(fn, 3, False)

# Import VectorPlotter and change directories
from ospybook.vectorplotter import VectorPlotter
os.chdir(os.path.join(data_dir, 'global'))

# Plot populated places on top of countries from an interactive session.
vp = VectorPlotter(True)
vp.plot('ne_50m_admin_0_countries.shp', fill=False)
vp.plot('ne_50m_populated_places.shp', 'bo')

# Plot populated places on top of countries non-interactively. Delete the vp
# variable if you tried the interactive one first.
del vp
vp = VectorPlotter(False)
vp.plot('ne_50m_admin_0_countries.shp', fill=False)
vp.plot('ne_50m_populated_places.shp', 'bo')
vp.draw()



#########################  3.4 Getting metadata  ##############################

# Open the large_cities data source.
fn = os.path.join(data_dir, 'Washington', 'large_cities.geojson')
ds = ogr.Open(fn)
if ds is None:
    sys.exit('Could not open {0}.'.format(fn))

# Get the spatial extent.
lyr = ds.GetLayer(0)
extent = lyr.GetExtent()
print(extent)
print('Upper left corner: {}, {}'.format(extent[0], extent[3]))
print('Lower right corner: {}, {}'.format(extent[1], extent[2]))

# Get geometry type
print(lyr.GetGeomType())
print(lyr.GetGeomType() == ogr.wkbPoint)
print(lyr.GetGeomType() == ogr.wkbPolygon)

# Get geometry type as human-readable string.
feat = lyr.GetFeature(0)
print(feat.geometry().GetGeometryName())

# Get spatial reference system. The output is also in listing3_2.py.
print(lyr.GetSpatialRef())

# Get field names and types
for field in lyr.schema:
    print(field.name, field.GetTypeName())



########################  3.5 Writing vector data  ############################

# Check the results from listing 3.2.
os.chdir(os.path.join(data_dir, 'global'))
vp = VectorPlotter(True)
vp.plot('ne_50m_admin_0_countries.shp', fill=False)
vp.plot('capital_cities.shp', 'bo')


######################  3.5.1 Creating new data sources  ######################

# Get the same driver as an existing data source
ds = ogr.Open(os.path.join(data_dir, 'global', 'ne_50m_admin_0_countries.shp'))
driver = ds.GetDriver()
print(driver.name)

# Get a driver by name
json_driver = ogr.GetDriverByName('GeoJSON')
print(json_driver.name)

# Create a GeoJSON file
json_fn = os.path.join(data_dir, 'output', 'example.geojson')
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))

# Create a SpatiaLite database. This will fail if your version of OGR wasn't
# built with SpatiaLite suppoert.
driver = ogr.GetDriverByName('SQLite')
ds = driver.CreateDataSource(os.path.join(data_dir, 'output', 'earth.sqlite'),
                             ['SPATIALITE=yes'])

# Delete a data source if it exists instead of trying to overwrite it.
if os.path.exists(json_fn):
    json_driver.DeleteDataSource(json_fn)
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))


############################  Using OGR exceptions  ###########################

# Try running this when output/africa.geojson already exists in order to raise
# the error.

# Turn on OGR exceptions. Try commenting this out to see how the behavior
# changes.
ogr.UseExceptions()

fn = os.path.join(data_dir, 'output', 'africa.geojson')
driver = ogr.GetDriverByName('GeoJSON')
print('Doing some preliminary analysis...')

try:
    # This will fail if the file already exists
    ds = driver.CreateDataSource(fn)
    lyr = ds.CreateLayer('layer')
    # Do more stuff, like fields and save data
except RuntimeError as e:
    # This runs if the data source already exists and an error was raised
    print(e)

print('Doing some more analysis...')


#########################  3.5.2 Creating new fields  #########################
# Create a shapefile that changes the precision for an attribute field. Also
# notice how the name field is not kept at 6 characters. If it were, many of
# the names would be truncated, but you shouldn't see that if you look at the
# attributes for the file created here. For the example, we'll create x and y
# fields for the Washington large_cities dataset.

# Much of this code is not in the book text.

# Open the input shapefile.
in_fn = os.path.join(data_dir, 'Washington', 'large_cities.shp')
in_ds = ogr.Open(in_fn, 0)
if in_ds is None:
    sys.exit('Could not open {0}.'.format(in_fn))
in_lyr = in_ds.GetLayer(0)

# Create the output shapefile.
driver = in_ds.GetDriver()
out_fn = os.path.join(data_dir, 'output', 'precision_test.shp')
if os.path.exists(out_fn):
    driver.DeleteDataSource(out_fn)
out_ds = driver.CreateDataSource(out_fn)
if out_ds is None:
    sys.exit('Could not create {0}.'.format(out_fn))

# Create the shapefile layer.
out_lyr = out_ds.CreateLayer('precision_test',
                             in_lyr.GetSpatialRef(),
                             ogr.wkbPoint)

# Set the name field to have a width of 6, but it will be expanded.
name_fld = ogr.FieldDefn('Name', ogr.OFTString)
name_fld.SetWidth(6)
out_lyr.CreateField(name_fld)

# Create two attribute fields using default precision.
coord_fld = ogr.FieldDefn('X_default', ogr.OFTReal)
out_lyr.CreateField(coord_fld)
coord_fld.SetName('Y_default')
out_lyr.CreateField(coord_fld)

# Create two attribute fields using a smaller precision. THIS IS THE
# EXAMPLE IN THE BOOK.
coord_fld = ogr.FieldDefn('X_short', ogr.OFTReal)
coord_fld.SetWidth(8)
coord_fld.SetPrecision(3)
out_lyr.CreateField(coord_fld)
coord_fld.SetName('Y_short')
out_lyr.CreateField(coord_fld)

# Copy data. After doing this, look at the attributes for your new shapefile
# and see the difference between the default and short fields.
out_feat = ogr.Feature(out_lyr.GetLayerDefn())
for in_feat in in_lyr:
    pt = in_feat.geometry()
    name = in_feat.GetField('NAME')
    out_feat.SetGeometry(in_feat.geometry())
    out_feat.SetField('Name', name)
    out_feat.SetField('X_default', pt.GetX())
    out_feat.SetField('Y_default', pt.GetY())
    out_feat.SetField('X_short', pt.GetX())
    out_feat.SetField('Y_short', pt.GetY())
    out_lyr.CreateFeature(out_feat)



########################  3.6 Updating existing data  #########################

# Set things up for the following examples.
original_fn = os.path.join(data_dir, 'Washington', 'large_cities.shp')
new_fn = os.path.join(data_dir, 'output', 'large_cities2.shp')

# First make a copy of a shapefile so you have something to test things on.
pb.copy_datasource(original_fn, new_fn)

# Open the copied shapefile for writing.
ds = ogr.Open(new_fn, 1)
if ds is None:
    sys.exit('Could not open {0}.'.format(new_fn))
lyr = ds.GetLayer(0)

# Take a look at the attributes before you change anything.
print('Original attributes')
pb.print_attributes(lyr, geom=False)


####################  3.6.1 Changing the layer definition  ####################

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
fld_defn.SetPrecision(4)
flag = ogr.ALTER_NAME_FLAG + ogr.ALTER_WIDTH_PRECISION_FLAG
lyr.AlterFieldDefn(i, fld_defn, flag)

# A slightly different method to change the name of the POINT_X field to
# X_coord and the precision to 4 decimal places. Copy the original field
# definition and use it. This uses the built-in Python copy module. If you
# do not copy the FieldDefn and instead try to use the original, you will
# probably get weird results.
import copy
lyr_defn = lyr.GetLayerDefn()
i = lyr_defn.GetFieldIndex('X')
fld_defn = copy.copy(lyr_defn.GetFieldDefn(i))
fld_defn.SetName('X_coord')
fld_defn.SetPrecision(4)
flag = ogr.ALTER_NAME_FLAG + ogr.ALTER_WIDTH_PRECISION_FLAG
lyr.AlterFieldDefn(i, fld_defn, flag)

# Take a look at the attributes now. The precision won't be affected yet,
# but the field names should be changed and there should be a blank ID
# field.
print('\nNew field names and empty ID field')
pb.print_attributes(lyr, geom=False)


###############  3.6.2 Adding, updating, and deleting features  ###############

# Add a unique ID to each feature.
lyr.ResetReading()
lyr.CreateField(ogr.FieldDefn('ID', ogr.OFTInteger))
n = 1
for feat in lyr:
    feat.SetField('ID', n)
    lyr.SetFeature(feat)
    n += 1
print('\nID has been added and precision has taken effect')
pb.print_attributes(lyr, geom=False)

# Delete Seattle. Notice that although it doesn't print the record for Seattle,
# it still thinks there are 14 features.
lyr.ResetReading()
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



##################  Bonus examples for creating new layers  ###################

# Just set stuff up for the examples. Note that these examples do not copy any
# attribute data into the json files.
shp_fn = os.path.join(data_dir, 'global', 'ne_50m_admin_0_countries.shp')
shp_ds = ogr.Open(shp_fn, 0)
if shp_ds is None:
    sys.exit('Could not open {0}'.format(shp_fn))
shp_lyr = shp_ds.GetLayer(0)
json_driver = ogr.GetDriverByName('GeoJSON')


#########################  Example 1: Default precision
# Create a json file using the default precision. Use a text editor to comapare
# the file created here with the files created in the next two examples.

# Create the data source.
json_fn = os.path.join(data_dir, 'output', 'africa-default.geojson')
if os.path.exists(json_fn):
    json_driver.DeleteDataSource(json_fn)
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))

# Create the layer with no options.
json_lyr = json_ds.CreateLayer('africa',
                               shp_lyr.GetSpatialRef(),
                               ogr.wkbMultiPolygon)

# Write some data.
shp_lyr.ResetReading()
json_feat = ogr.Feature(json_lyr.GetLayerDefn())
for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':
        json_feat.SetGeometry(shp_feat.geometry())
        json_lyr.CreateFeature(json_feat)
del json_ds

#########################  Example 2: 6-digit precision
# Create a json file using the optional COORDINATE_PRECISION creation option
# and set the precision to 6 digits.
json_fn = os.path.join(data_dir, 'output', 'africa-6digit.geojson')
if os.path.exists(json_fn):
    json_driver.DeleteDataSource(json_fn)
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))

lyr_options = ['COORDINATE_PRECISION=6']
json_lyr = json_ds.CreateLayer('africa',
                               shp_lyr.GetSpatialRef(),
                               ogr.wkbMultiPolygon,
                               lyr_options)

# Write some data.
shp_lyr.ResetReading()
json_feat = ogr.Feature(json_lyr.GetLayerDefn())
for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':
        json_feat.SetGeometry(shp_feat.geometry())
        json_lyr.CreateFeature(json_feat)
json_ds

###########################  Example 3: Bounding box
# Create a json file using the optional COORDINATE_PRECISION and WRITE_BBOX
# creation options.
json_fn = os.path.join(data_dir, 'output', 'africa-bbox.geojson')
if os.path.exists(json_fn):
    json_driver.DeleteDataSource(json_fn)
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))

lyr_options = ['COORDINATE_PRECISION=6', 'WRITE_BBOX=YES']
json_lyr = json_ds.CreateLayer('africa',
                               shp_lyr.GetSpatialRef(),
                               ogr.wkbMultiPolygon,
                               lyr_options)

# Write some data.
shp_lyr.ResetReading()
json_feat = ogr.Feature(json_lyr.GetLayerDefn())
for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':
        json_feat.SetGeometry(shp_feat.geometry())
        json_lyr.CreateFeature(json_feat)
del json_ds


#################  Bonus examples for creating new features  ##################

shp_fn = os.path.join(data_dir, 'global', 'ne_50m_admin_0_countries.shp')
json_fn = os.path.join(data_dir, 'output', 'africa.geojson')

# Open input.
shp_ds = ogr.Open(shp_fn, 0)
if shp_ds is None:
    sys.exit('Could not open {0}'.format(shp_fn))
shp_lyr = shp_ds.GetLayer(0)

# Create output file.
json_driver = ogr.GetDriverByName('GeoJSON')
if os.path.exists(json_fn):
    json_driver.DeleteDataSource(json_fn)
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))
lyr_options = ['COORDINATE_PRECISION=6']
json_lyr = json_ds.CreateLayer('africa',
                               shp_lyr.GetSpatialRef(),
                               ogr.wkbMultiPolygon,
                               lyr_options)

# Add attribute fields to the layer.
name_fld = ogr.FieldDefn('Name', ogr.OFTString)
json_lyr.CreateField(name_fld)
pop_fld = ogr.FieldDefn('Population', ogr.OFTInteger)
json_lyr.CreateField(pop_fld)

# For the fun of it, let's also add an integer field but "mistakenly" put a
# string in it to see what happens.
test_fld = ogr.FieldDefn('Test_field', ogr.OFTInteger)
json_lyr.CreateField(test_fld)

# Get the feature definition.
feat_defn = json_lyr.GetLayerDefn()

# Create an output feature to use repeatedly.
json_feat = ogr.Feature(feat_defn)

for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':

        # Copy attribute values if in Africa.
        name = shp_feat.GetField('NAME')
        pop = shp_feat.GetField('POP_EST')
        json_feat.SetField('Name', name)
        json_feat.SetField('Population', pop)

        # Put a string in an integer field.
        json_feat.SetField('Test_field', name)

        # Copy the geometry.
        json_feat.SetGeometry(shp_feat.geometry())

        # Insert the data into the GeoJSON file.
        json_lyr.CreateFeature(json_feat)

del json_ds, shp_ds
