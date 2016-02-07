import os
import sys
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



#########################  6.5  Spatial analysis  ##############################

#########################  6.5.1  Overlay tools  ###############################

# Look at New Orleans wetlands. First get a specific marsh feature near New
# Orleans.
vp = VectorPlotter(True)
water_ds = ogr.Open(os.path.join(data_dir, 'US', 'wtrbdyp010.shp'))
water_lyr = water_ds.GetLayer(0)
water_lyr.SetAttributeFilter('WaterbdyID = 1011327')
marsh_feat = water_lyr.GetNextFeature()
marsh_geom = marsh_feat.geometry().Clone()
vp.plot(marsh_geom, 'b')

# Get the New Orleans boundary.
nola_ds = ogr.Open(os.path.join(data_dir, 'Louisiana', 'NOLA.shp'))
nola_lyr = nola_ds.GetLayer(0)
nola_feat = nola_lyr.GetNextFeature()
nola_geom = nola_feat.geometry().Clone()
vp.plot(nola_geom, fill=False, ec='red', ls='dashed', lw=3)

# Intersect the marsh and boundary polygons to get the part of the marsh that
# falls within New Orleans city boundaries.
intersection = marsh_geom.Intersection(nola_geom)
vp.plot(intersection, 'yellow', hatch='x')

# Figure out how much of New Orleans is wetlands. Throw out lakes and anything
# not in the vicinity of New Orleans, and then loop through the remaining water
# body features. For each one, find the area of the feature that is contained
# within city boundaries and add it to a running total. Then it's easy to
# figure the percentage by dividing that total by the area of New Orleans.
water_lyr.SetAttributeFilter("Feature != 'Lake'")
water_lyr.SetSpatialFilter(nola_geom)
wetlands_area = 0
for feat in water_lyr:
    intersect = feat.geometry().Intersection(nola_geom)
    wetlands_area += intersect.GetArea()
pcnt = wetlands_area / nola_geom.GetArea()
print('{:.1%} of New Orleans is wetland'.format(pcnt))

# Another way to figure out how much of New Orleans is wetlands, this time
# using layers instead of individual geometries. You need to set the attribute
# filter, but a spatial filter isn't necessary. In this case you'll need an
# empty layer to store the intersection results in, so create a temporary one
# in memory. Then run the intersection and use SQL to sum up the areas.
water_lyr.SetSpatialFilter(None)
water_lyr.SetAttributeFilter("Feature != 'Lake'")

memory_driver = ogr.GetDriverByName('Memory')
temp_ds = memory_driver.CreateDataSource('temp')
temp_lyr = temp_ds.CreateLayer('temp')

nola_lyr.Intersection(water_lyr, temp_lyr)

sql = 'SELECT SUM(OGR_GEOM_AREA) AS area FROM temp'
lyr = temp_ds.ExecuteSQL(sql)
pcnt = lyr.GetFeature(0).GetField('area') / nola_geom.GetArea()
print('{:.1%} of New Orleans is wetland'.format(pcnt))


########################  6.5.2  Proximity tools  ##############################

# Find out how many US cities are within 16,000 meters of a volcano. Create a
# temporary layer in memory to store the buffers, then loop through the
# volcanoes, buffer each one, and store the result in the temporary layer (the
# tmp variables are there to keep a bunch of zeros from printing out when
# running this in an interactive window-- if you were really good, you could
# check their values to make sure nothing went wrong). Once all of the
# volcanoes have been buffered, intersect the temporary buffer layer with the
# cities layer to get the cites that fall in a buffer.
shp_ds = ogr.Open(os.path.join(data_dir, 'US'))
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')
cities_lyr = shp_ds.GetLayer('cities_albers')

memory_driver = ogr.GetDriverByName('memory')
memory_ds = memory_driver.CreateDataSource('temp')
buff_lyr = memory_ds.CreateLayer('buffer')
buff_feat = ogr.Feature(buff_lyr.GetLayerDefn())

for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(16000)
    tmp = buff_feat.SetGeometry(buff_geom)
    tmp = buff_lyr.CreateFeature(buff_feat)

result_lyr = memory_ds.CreateLayer('result')
buff_lyr.Intersection(cities_lyr, result_lyr)
print('Cities: {}'.format(result_lyr.GetFeatureCount()))

# A better method to count the cities within 16,000 meters of a volcano,
# because it doesn't double-count stuff. This time, add each buffer to a
# multipolygon instead of a temporary later. Then union all of the buffers
# together to get one polygon which you can use as a spatial filter.
volcano_lyr.ResetReading()
multipoly = ogr.Geometry(ogr.wkbMultiPolygon)
for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(16000)
    multipoly.AddGeometry(buff_geom)
cities_lyr.SetSpatialFilter(multipoly.UnionCascaded())
print('Cities: {}'.format(cities_lyr.GetFeatureCount()))

# Find out how far Seattle is from Mount Rainier.
volcano_lyr.SetAttributeFilter("NAME = 'Rainier'")
feat = volcano_lyr.GetNextFeature()
rainier = feat.geometry().Clone()

cities_lyr.SetSpatialFilter(None)
cities_lyr.SetAttributeFilter("NAME = 'Seattle'")
feat = cities_lyr.GetNextFeature()
seattle = feat.geometry().Clone()

meters = round(rainier.Distance(seattle))
miles = meters / 1600
print('{} meters ({} miles)'.format(meters, miles))



#############################  2.5D Geometries  ################################

# Take a look at the distance between two 2D points. The distance should be 4.
pt1_2d = ogr.Geometry(ogr.wkbPoint)
pt1_2d.AddPoint(15, 15)
pt2_2d = ogr.Geometry(ogr.wkbPoint)
pt2_2d.AddPoint(15, 19)
print(pt1_2d.Distance(pt2_2d))

# Now create some 2.5D points, using the same x and y coordinates, but adding
# z coordinates. The distance now, if three dimensions were taken into account,
# would be 5. But ogr still returns 4. This is because the z coordinates are
# ignored.
pt1_25d = ogr.Geometry(ogr.wkbPoint25D)
pt1_25d.AddPoint(15, 15, 0)
pt2_25d = ogr.Geometry(ogr.wkbPoint25D)
pt2_25d.AddPoint(15, 19, 3)
print(pt1_25d.Distance(pt2_25d))

# Take a look at the area of a 2D polygon. The area should be 100.
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(10, 10)
ring.AddPoint(10, 20)
ring.AddPoint(20, 20)
ring.AddPoint(20, 10)
poly_2d = ogr.Geometry(ogr.wkbPolygon)
poly_2d.AddGeometry(ring)
poly_2d.CloseRings()
print(poly_2d.GetArea())

# Now create a 2.5D polygon, again using the same x and y coordinates, but
# providing a z coordinate for a couple of the vertices. The area of this in
# three dimensions is around 141, but ogr still returns 100.
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(10, 10, 0)
ring.AddPoint(10, 20, 0)
ring.AddPoint(20, 20, 10)
ring.AddPoint(20, 10, 10)
poly_25d = ogr.Geometry(ogr.wkbPolygon25D)
poly_25d.AddGeometry(ring)
poly_25d.CloseRings()
print(poly_25d.GetArea())

# If three dimensions were taken into account, pt1_d2 would be contained in the
# 2D polygon, but not the 3D one. But since the 3D one is really 2.5D, ogr
# thinks the point is contained in both polygons.
print(poly_2d.Contains(pt1_2d))
print(poly_25d.Contains(pt1_2d))
