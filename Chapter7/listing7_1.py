# Use a flawed method to find out how many US cities are within 16,000
# meters of a volcano.

from osgeo import ogr

shp_ds = ogr.Open(r'D:\osgeopy-data\US')
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')
cities_lyr = shp_ds.GetLayer('cities_albers')

# Create a temporary layer in memory to store the buffers.
memory_driver = ogr.GetDriverByName('memory')
memory_ds = memory_driver.CreateDataSource('temp')
buff_lyr = memory_ds.CreateLayer('buffer')
buff_feat = ogr.Feature(buff_lyr.GetLayerDefn())

# Loop through the volcanoes, buffer each one, and store the result in the
# temporary layer (the tmp variables are there to keep a bunch of zeros from
# printing out when running this in an interactive window-- if you were
# really good, you could check their values to make sure nothing went wrong).
for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(16000)
    tmp = buff_feat.SetGeometry(buff_geom)
    tmp = buff_lyr.CreateFeature(buff_feat)

# Once all of the volcanoes have been buffered, intersect the temporary
# buffer layer with the cities layer to get the cities that fall in a buffer.
result_lyr = memory_ds.CreateLayer('result')
buff_lyr.Intersection(cities_lyr, result_lyr)
print('Cities: {}'.format(result_lyr.GetFeatureCount()))
