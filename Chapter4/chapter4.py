import os
from osgeo import ogr
import ospybook as pb
from ospybook.vectorplotter import VectorPlotter


# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
data_dir = r'D:\osgeopy-data'
# data_dir =



#########################  4.2 More data formats  #############################

# A function to print out the layers in a data source.
def print_layers(fn):
    ds = ogr.Open(fn, 0)
    if ds is None:
        raise OSError('Could not open {}'.format(fn))
    for i in range(ds.GetLayerCount()):
        lyr = ds.GetLayer(i)
        print('{0}: {1}'.format(i, lyr.GetName()))

# Try out the function.
print_layers(os.path.join(data_dir, 'Washington', 'large_cities.geojson'))


#########################  4.2.1 SpatiaLite  ##################################

# Use the function in ospybook to look at a SpatiaLite database.
pb.print_layers(os.path.join(data_dir, 'global', 'natural_earth_50m.sqlite'))

# Get the populated_places layer.
ds = ogr.Open(os.path.join(data_dir, 'global', 'natural_earth_50m.sqlite'))
lyr = ds.GetLayer('populated_places')

# Plot the populated places layer in the SpatiaList database interactively.
vp = VectorPlotter(True)
vp.plot(lyr, 'bo')

# Plot the populated places layer in the SpatiaList database non-interactively.
vp = VectorPlotter(False)
vp.plot(lyr, 'bo')
vp.draw()


#########################  4.2.2 PostGIS  #####################################

# Print out layers in a PostGIS database. This will not work for you unless
# you set up a PostGIS server.
pb.print_layers('PG:user=chris password=mypass dbname=geodata')


#########################  4.2.3 Folders  #####################################

# Get the shapefile layers in a folder.
pb.print_layers(os.path.join(data_dir, 'US'))

# EXTRA
# Get the csv layers in a folder.
pb.print_layers(os.path.join(data_dir, 'US', 'csv'))

# Use csv or shapefiles as data sources.
pb.print_layers(os.path.join(data_dir, 'US', 'volcanoes.csv'))
pb.print_layers(os.path.join(data_dir, 'US', 'citiesx020.shp'))

# Just for the fun of it, try to force the CSV driver to use a folder with
# other stuff in it. The folder will not be opened successfully and ds will be
# None.
driver = ogr.GetDriverByName('CSV')
ds = driver.Open(os.path.join(data_dir, 'US'))
print(ds)


#########################  4.2.4 Esri file geodatabase  #######################

# Print out layers in an Esri file geodatabase.
fn = os.path.join(data_dir, 'global', 'natural_earth.gdb')
pb.print_layers(fn)

# Get a layer inside a feature dataset.
ds = ogr.Open(fn)
lyr = ds.GetLayer('countries_10m')

# Print out some attributes to make sure it worked.
pb.print_attributes(lyr, 5, ['NAME', 'POP_EST'])

# Export a feature class from geodatabase to a shapefile.
out_folder = os.path.join(data_dir, 'global')
gdb_ds = ogr.Open(fn)
gdb_lyr = gdb_ds.GetLayerByName('countries_110m')
shp_ds = ogr.Open(out_folder, 1)
shp_ds.CopyLayer(gdb_lyr, 'countries_110m')
del shp_ds, gdb_ds

# Use listing 4.2 to copy shapefiles in a folder into a file geodatabase.
import listing4_2
shp_folder = os.path.join(data_dir, 'global')
gdb_fn = os.path.join(shp_folder, 'osgeopy-data.gdb')
listing4_2.layers_to_feature_dataset(shp_folder, gdb_fn, 'global')


#########################  4.2.5 Web Feature Service  #########################

# Print out layers in a WFS.
url = 'WFS:http://gis.srh.noaa.gov/arcgis/services/watchWarn/MapServer/WFSServer'
pb.print_layers(url)

# Get the first warning from the WFS. This might take a while because it has
# to download all of the data first.
ds = ogr.Open(url)
lyr = ds.GetLayer(1)
print(lyr.GetFeatureCount())
feat = lyr.GetNextFeature()
print(feat.GetField('prod_type'))

# Get the first warning from the WFS by limiting the returned features to 1.
ds = ogr.Open(url + '?MAXFEATURES=1')
lyr = ds.GetLayer(1)
print(lyr.GetFeatureCount())

# Extra: Plot the WatchesWarnings layer (this will probably take a while).
vp = VectorPlotter(False)
ds = ogr.Open(os.path.join(data_dir, 'US', 'states_48.shp'))
lyr = ds.GetLayer(0)
vp.plot(lyr, fill=False)
ds = ogr.Open(url)
lyr = ds.GetLayer('watchWarn:WatchesWarnings')
vp.plot(lyr)
vp.draw()



########################  4.3 Testing capabilities  ###########################

# Test if you can create a new shapefile in a folder opened for reading only.
dirname = os.path.join(data_dir, 'global')
ds = ogr.Open(dirname)
print(ds.TestCapability(ogr.ODsCCreateLayer))

# Test if you can create a new shapefile in a folder opened for writing.
ds = ogr.Open(dirname, 1)
print(ds.TestCapability(ogr.ODsCCreateLayer))


# Make a copy of a shapefile for the following examples.
original_fn = os.path.join(data_dir, 'Washington', 'large_cities2.shp')
new_fn = os.path.join(data_dir, 'output', 'large_cities3.shp')
pb.copy_datasource(original_fn, new_fn)

# Try opening the datasource read-only and see if you can add a field (you
# can't). The example in the book opens it for writing, as in the next
# snippet in this file).
ds = ogr.Open(new_fn, 0)
if ds is None:
    sys.exit('Could not open {0}.'.format(new_fn))
lyr = ds.GetLayer(0)

if not lyr.TestCapability(ogr.OLCCreateField):
    raise RuntimeError('Cannot create fields.')
lyr.CreateField(ogr.FieldDefn('ID', ogr.OFTInteger))

# Now try it with the datasource opened for writing. This is the way the
# book does it, because this is how it should be done.
ds = ogr.Open(new_fn, 1)
if ds is None:
    sys.exit('Could not open {0}.'.format(new_fn))
lyr = ds.GetLayer(0)

if not lyr.TestCapability(ogr.OLCCreateField):
    raise RuntimeError('Cannot create fields.')
lyr.CreateField(ogr.FieldDefn('ID', ogr.OFTInteger))

# Use the ospybook print_capabilities function.
driver = ogr.GetDriverByName('ESRI Shapefile')
pb.print_capabilities(driver)
