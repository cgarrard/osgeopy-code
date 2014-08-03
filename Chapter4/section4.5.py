import os
from osgeo import ogr

# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
# data_dir = r'D:\osgeopy-data'
data_dir =


#########################  4.5 Getting metadata  ###############################

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

# Get spatial reference system.
print(lyr.GetSpatialRef())

# Get field names and types
for field in lyr.schema:
    print(field.name, field.GetTypeName())

