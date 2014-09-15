import os
import sys

from osgeo import ogr

import ospybook as pb
from ospybook.vectorplotter import VectorPlotter

# Make sure you change these paths!
shp_fn = r'D:\osgeopy-data\global\ne_10m_admin_0_countries.shp'
json_fn = r'D:\osgeopy-data\output\africa.geojson'

# Open the the input file for reading
shp_ds = ogr.Open(shp_fn, 0)
if shp_ds is None:
    sys.exit('Could not open {0}'.format(shp_fn))
shp_lyr = shp_ds.GetLayer(0)

# Get the correct output driver
json_driver = ogr.GetDriverByName('GeoJSON')

# Ensure that the output file does not exist
if os.path.exists(json_fn):
    json_driver.DeleteDataSource(json_fn)

# Create the GeoJSON file
json_ds = json_driver.CreateDataSource(json_fn)
if json_ds is None:
    sys.exit('Could not create {0}.'.format(json_fn))

# Create a new polygon layer
lyr_options = ['COORDINATE_PRECISION=6']
json_lyr = json_ds.CreateLayer('africa',
                               shp_lyr.GetSpatialRef(),
                               ogr.wkbMultiPolygon,
                               lyr_options)

# Add attribute fields to the layer
name_fld = ogr.FieldDefn('Name', ogr.OFTString)
json_lyr.CreateField(name_fld)
pop_fld = ogr.FieldDefn('Population', ogr.OFTInteger)
json_lyr.CreateField(pop_fld)

feat_defn = json_lyr.GetLayerDefn()

# Create an output feature to use repeatedly
json_feat = ogr.Feature(feat_defn)

for shp_feat in shp_lyr:
    if shp_feat.GetField('CONTINENT') == 'Africa':

        # Copy geometry and attribute values if in Africa
        name = shp_feat.GetField('NAME')
        pop = shp_feat.GetField('POP_EST')
        json_feat.SetField('Name', name)
        json_feat.SetField('Population', pop)
        json_feat.SetGeometry(shp_feat.geometry())

        # Insert the data into the GeoJSON file
        json_lyr.CreateFeature(json_feat)

# Delete the datasource. Python will write it to disk and close the file when
# the variable isn't needed anymore.
del json_ds

# Visualize the output
pb.print_attributes(json_fn)
vp = VectorPlotter(False)
vp.plot(shp_fn, fc='0.9')
vp.plot(json_fn, 'y')
vp.draw()
