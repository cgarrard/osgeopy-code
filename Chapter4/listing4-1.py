import sys
from osgeo import ogr

# Open the datasource and get the layer. Make sure you change the file path.
fn = r'D:\osgeopy-data\Washington\large_cities.geojson'
ds = ogr.Open(fn, 0)
if ds is None:
    sys.exit('Could not open {0}.'.format(fn))
lyr = ds.GetLayer(0)

# Iterate through the features and print info.
for feat in lyr:
    pt = feat.geometry()
    x = pt.GetX()
    y = pt.GetY()
    name = feat.GetField('Name')
    pop = feat.GetField('Population')
    print(name, pop, x, y)
