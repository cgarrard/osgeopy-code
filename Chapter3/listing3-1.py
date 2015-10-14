# Script to read attributes from a shapefile.

# Don't forget to import ogr
import sys
from osgeo import ogr

# Open the data source and get the layer
fn = r'D:\osgeopy-data\global\ne_50m_populated_places.shp'
ds = ogr.Open(fn, 0)
if ds is None:
    sys.exit('Could not open {0}.'.format(fn))
lyr = ds.GetLayer(0)

i = 0
for feat in lyr:

    # Get the x,y coordinates
    pt = feat.geometry()
    x = pt.GetX()
    y = pt.GetY()

    # Get the attribute values
    name = feat.GetField('NAME')
    pop = feat.GetField('POP_MAX')
    print(name, pop, x, y)
    i += 1
    if i == 10:
        break
del ds
