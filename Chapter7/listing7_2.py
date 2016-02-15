# Use a better method to count the cities within 16,000 meters of a volcano,
# because it doesn't double-count stuff.

import ogr

# Open the layers as in listing 7.1 instead of reset reading.
shp_ds = ogr.Open(r'D:\osgeopy-data\US')
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')
cities_lyr = shp_ds.GetLayer('cities_albers')

# This time, add each buffer to a multipolygon instead of a temporary later.
multipoly = ogr.Geometry(ogr.wkbMultiPolygon)
for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(16000)
    multipoly.AddGeometry(buff_geom)

# Then union all of the buffers together to get one polygon which you can use
# as a spatial filter.
cities_lyr.SetSpatialFilter(multipoly.UnionCascaded())
print('Cities: {}'.format(cities_lyr.GetFeatureCount()))
