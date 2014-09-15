import os
import sys

from osgeo import ogr

# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
# data_dir = r'D:\osgeopy-data'
data_dir =


#####################  5.1.1  Creating new data sources  #######################

# Get the same driver as an existing data source
ds = ogr.Open(os.path.join(data_dir, 'global', 'ne_10m_admin_0_countries.shp'))
driver = ds.GetDriver()
print(driver.name)

# Get a driver by name
json_driver = ogr.GetDriverByName('GeoJSON')
print(json_driver.name)

# Create a GeoJSON file
json_fn = os.path.join(data_dir, 'output', 'africa.geojson')
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


############################  Using OGR exceptions  ############################

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


#########################  5.1.2  Creating new layers  #########################

# Just set stuff up for the examples. Note that these examples do not copy any
# attribute data into the json files.
shp_fn = os.path.join(data_dir, 'global', 'ne_10m_admin_0_countries.shp')
shp_ds = ogr.Open(shp_fn, 0)
if shp_ds is None:
    sys.exit('Could not open {0}'.format(shp_fn))
shp_lyr = shp_ds.GetLayer(0)
json_driver = ogr.GetDriverByName('GeoJSON')


#########################  Example 1: Default precision  #######################
# Create a json file using the default precision. Use a text editor to comapare
# the file created here with the files created in the next two examples.

# Create the data source
json_fn = os.path.join(data_dir, 'output', 'africa-default.geojson')
if os.path.exists(json_fn):
    json_driver.DeleteDataSource(json_fn)
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))

# Create the layer with no options
json_lyr = json_ds.CreateLayer('africa',
                               shp_lyr.GetSpatialRef(),
                               ogr.wkbMultiPolygon)

# Write some data (you'll learn about this in section 5.1.4).
shp_lyr.ResetReading()
json_feat = ogr.Feature(json_lyr.GetLayerDefn())
for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':
        json_feat.SetGeometry(shp_feat.geometry())
        json_lyr.CreateFeature(json_feat)

#########################  Example 2: 6-digit precision  #######################
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

# Write some data (you'll learn about this in section 5.1.4).
shp_lyr.ResetReading()
json_feat = ogr.Feature(json_lyr.GetLayerDefn())
for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':
        json_feat.SetGeometry(shp_feat.geometry())
        json_lyr.CreateFeature(json_feat)


###########################  Example 3: Bounding box  ##########################
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

# Write some data (you'll learn about this in section 5.1.4).
shp_lyr.ResetReading()
json_feat = ogr.Feature(json_lyr.GetLayerDefn())
for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':
        json_feat.SetGeometry(shp_feat.geometry())
        json_lyr.CreateFeature(json_feat)


#########################  5.1.3  Creating new fields  #########################
# Create a shapefile that changes the precision for an attribute field. Also
# notice how the name field is not kept at 6 characters. If it were, many of
# the names would be truncated, but you shouldn't see that if you look at the
# attributes for the file created here. For the example, we'll create x and y
# fields for the Washington large_cities dataset.

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
coord_fld = ogr.FieldDefn('Y_default', ogr.OFTReal)
out_lyr.CreateField(coord_fld)

# Create two attribute fields using a smaller precision.
coord_fld = ogr.FieldDefn('X_short', ogr.OFTReal)
coord_fld.SetWidth(8)
coord_fld.SetPrecision(3)
out_lyr.CreateField(coord_fld)
coord_fld = ogr.FieldDefn('Y_short', ogr.OFTReal)
coord_fld.SetWidth(8)
coord_fld.SetPrecision(3)
out_lyr.CreateField(coord_fld)

# Copy data (you'll learn about this in section 5.1.4).
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


#########################  5.1.4  Creating new features  #######################
# This is essentially listing 5.1, because you can't add feataures without
# doing all of the preliminary stuff first.

shp_fn = os.path.join(data_dir, 'global', 'ne_10m_admin_0_countries.shp')
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

        # Insert the data into the GeoJSON file
        json_lyr.CreateFeature(json_feat)
