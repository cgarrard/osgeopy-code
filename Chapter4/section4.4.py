import os
from osgeo import ogr
import ospybook as pb
from ospybook.vectorplotter import VectorPlotter

# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
# data_dir = r'D:\osgeopy-data'
data_dir =


#########################  4.4 More data formats  ##############################

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


#########################  SpatiaLite  #########################################

# Use the function in ospybook to look at a SpatiaLite database.
pb.print_layers(os.path.join(data_dir, 'global', 'natural_earth_50m.sqlite'))

# Get the populated_places layer.
ds = ogr.Open(os.path.join(data_dir, 'global', 'natural_earth_50m.sqlite'))
lyr = ds.GetLayer('populated_places')

# Plot the populated places layer in the SpatiaList database interactively.
vp = VectorPlotter(True)
vp.plot(lyr)

# Plot the populated places layer in the SpatiaList database non-interactively.
vp = VectorPlotter(False)
vp.plot(lyr)
vp.draw()


#########################  PostGIS  ############################################

# Print out layers in a PostGIS database. This will not work for you unless
# you set up a PostGIS server.
pb.print_layers('PG:user=chris password=mypass dbname=geodata')


#########################  Esri file geodatabase  ##############################

# Print out layers in an Esri file geodatabase.
pb.print_layers(os.path.join(data_dir, 'global', 'natural_earth.gdb'))


#########################  Web Feature Service  ################################

# Print out layers in a WFS.
url = 'WFS:http://gis.srh.noaa.gov/arcgis/services/watchwarn/MapServer/WFSServer'
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

# Plot the WatchesWarnings layer (this will probably take a while).
vp = VectorPlotter(False)
ds = ogr.Open(os.path.join(data_dir, 'US', 'states_48.shp'))
lyr = ds.GetLayer(0)
vp.plot(lyr, fill=False)
ds = ogr.Open(url)
lyr = ds.GetLayer('watchwarn:WatchesWarnings')
vp.plot(lyr)
vp.draw()


#########################  Folders  ############################################

# Get the shapefile layers in a folder.
pb.print_layers(os.path.join(data_dir, 'US'))

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
