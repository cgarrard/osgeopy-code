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


#########################  7.2  Working with points  ###########################

###########################  7.2.1  Single points  #############################

# Create the firepit point.
firepit = ogr.Geometry(ogr.wkbPoint)
firepit.AddPoint(59.5, 11.5)

# Try out GetX and GetY.
x, y = firepit.GetX(), firepit.GetY()
print('{}, {}'.format(x, y))

# Take a look at the point.
print(firepit)
vp = VectorPlotter(True)
vp.plot(firepit, 'bo')

# Edit the point coordinates.
firepit.AddPoint(59.5, 13)
vp.plot(firepit, 'rs')
print(firepit)

# Or edit the point using SetPoint instead of AddPoint.
firepit.SetPoint(0, 59.5, 13)
print(firepit)

# Make a 2.5D point.
firepit = ogr.Geometry(ogr.wkbPoint25D)
firepit.AddPoint(59.5, 11.5, 2)
print(firepit)


###########################  7.2.2  Multiple points  ###########################

# Create the multipoint to hold the water spigots. Create multipoint and point
# geometries. For each spigot, edit the point coordinates and add the point to
# the multipoint.
faucets = ogr.Geometry(ogr.wkbMultiPoint)
faucet = ogr.Geometry(ogr.wkbPoint)
faucet.AddPoint(67.5, 16)
faucets.AddGeometry(faucet)
faucet.AddPoint(73, 31)
faucets.AddGeometry(faucet)
faucet.AddPoint(91, 24.5)
faucets.AddGeometry(faucet)

# Take a look at the multipoint.
vp.clear()
vp.plot(faucets, 'bo')
vp.zoom(-5)
print(faucets)

# Edit the coordinates for the second faucet.
faucets.GetGeometryRef(1).AddPoint(75, 32)
vp.plot(faucets, 'k^', 'tmp')
print(faucets)

# Change the coordinates back for the next example.
faucets.GetGeometryRef(1).AddPoint(73, 31)
vp.remove('tmp')

# Move all spigots two units to the east. After plotting, you will probably
# have to zoom out a bit in order to really see what happened.
for i in range(faucets.GetGeometryCount()):
    pt = faucets.GetGeometryRef(i)
    pt.AddPoint(pt.GetX() + 2, pt.GetY())
vp.plot(faucets, 'rs')
vp.zoom(-5)


#########################  7.3  Working with lines  ############################

###########################  7.3.1  Single lines  ##############################

# Create the sidewalk line. Make sure to add the vertices in order.
sidewalk = ogr.Geometry(ogr.wkbLineString)
sidewalk.AddPoint(54, 37)
sidewalk.AddPoint(62, 35.5)
sidewalk.AddPoint(70.5, 38)
sidewalk.AddPoint(74.5, 41.5)

# Take a look at the line.
vp = VectorPlotter(True)
vp.plot(sidewalk, 'b-')
print(sidewalk)

# Change the last vertex.
sidewalk.SetPoint(3, 76, 41.5)
vp.plot(sidewalk, 'k--', 'tmp')
print(sidewalk)

# Change the coordinates back for the next example.
sidewalk.SetPoint(3, 74.5, 41.5)
vp.remove('tmp')

# Move the line one unit to the north.
for i in range(sidewalk.GetPointCount()):
    sidewalk.SetPoint(i, sidewalk.GetX(i), sidewalk.GetY(i) + 1)
vp.plot(sidewalk, 'r--')
print(sidewalk)

# Try out GetGeometryCount to prove it that it returns zero for a single
# geometry.
print(sidewalk.GetPointCount()) # vertices
print(sidewalk.GetGeometryCount()) # sub-geometries

# Move the sidewalk back to its original location for the next example.
for i in range(sidewalk.GetPointCount()):
    sidewalk.SetPoint(i, sidewalk.GetX(i), sidewalk.GetY(i) - 1)

# Look at the list of tuples containing vertex coordinates.
print(sidewalk.GetPoints())

# Insert a new vertex between the 2nd and 3rd vertices.
vertices = sidewalk.GetPoints()
vertices[2:2] = [(66.5, 35)]
print(vertices)

# Create a new line geometry from the list of vertices.
new_sidewalk = ogr.Geometry(ogr.wkbLineString)
for vertex in vertices:
    new_sidewalk.AddPoint(*vertex)
vp.plot(new_sidewalk, 'g:')

# Get the original line for the multiple vertices example.
ds = ogr.Open(os.path.join(data_dir, 'misc', 'line-example.geojson'))
lyr = ds.GetLayer()
feature = lyr.GetFeature(0)
line = feature.geometry().Clone()
vp.clear()
vp.plot(line, 'b-')

# Add a bunch of vertices at different locations. Start from the end so that
# earlier indices don't get messed up.
vertices = line.GetPoints()
vertices[26:26] = [(87, 57)]
vertices[19:19] = [(95, 38), (97, 43), (101, 42)]
vertices[11:11] = [(121, 18)]
vertices[5:5] = [(67, 32), (74, 30)]
new_line = ogr.Geometry(ogr.wkbLineString)
for vertex in vertices:
    new_line.AddPoint(*vertex)
vp.plot(new_line, 'b--')

# Insert a vertex without creating a new line.
vertices = sidewalk.GetPoints()
vertices[2:2] = [(66.5, 35)]
for i in range(len(vertices)):
    sidewalk.SetPoint(i, *vertices[i])
vp.plot(sidewalk, 'k-', lw=3)


###########################  The Python *-operator  ############################

pt = ogr.Geometry(ogr.wkbPoint)
vertex = (10, 20)

# Resolves to pt.AddPoint(10, 20), which works
pt.AddPoint(*vertex)

# Resolves to pt.AddPoint((10, 20)), which fails because only one thing
# (a tuple) is getting passed to AddPoint.
pt.AddPoint(vertex)


###########################  7.3.2  Multiple lines  ############################

# Create the pathways multiline. Create three individual lines, one for each
# path. Then add them all to the multiline geometry.
path1 = ogr.Geometry(ogr.wkbLineString)
path1.AddPoint(61.5, 29)
path1.AddPoint(63, 20)
path1.AddPoint(62.5, 16)
path1.AddPoint(60, 13)

path2 = ogr.Geometry(ogr.wkbLineString)
path2.AddPoint(60.5, 12)
path2.AddPoint(68.5, 13.5)

path3 = ogr.Geometry(ogr.wkbLineString)
path3.AddPoint(69.5, 33)
path3.AddPoint(80, 33)
path3.AddPoint(86.5, 22.5)

paths = ogr.Geometry(ogr.wkbMultiLineString)
paths.AddGeometry(path1)
paths.AddGeometry(path2)
paths.AddGeometry(path3)

# Take a look at the multiline.
vp.clear()
vp.plot(paths, 'b-')
print(paths)

# Edit the second vertex in the first path.
paths.GetGeometryRef(0).SetPoint(1, 63, 22)
vp.plot(paths, 'k--', 'tmp')
print(paths)

# Change the coordinates back for the next example.
paths.GetGeometryRef(0).SetPoint(1, 63, 20)
vp.remove('tmp')

# Move the line two units east and three south. Get each individual path from
# the multipath with GetGeometryRef, and then edit the vertices for the path.
for i in range(paths.GetGeometryCount()):
    path = paths.GetGeometryRef(i)
    for j in range(path.GetPointCount()):
        path.SetPoint(j, path.GetX(j) + 2, path.GetY(j) - 3)
vp.plot(paths, 'r--')


#########################  7.4  Working with polygons  #########################

#########################  7.4.1  Single polygons  #############################

# Make the yard boundary polygon. Create a ring and add the vertices in order,
# and then add the ring to the polygon.
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(58, 38.5)
ring.AddPoint(53, 6)
ring.AddPoint(99.5, 19)
ring.AddPoint(73, 42)
yard = ogr.Geometry(ogr.wkbPolygon)
yard.AddGeometry(ring)
yard.CloseRings()

# Take a look at the polygon. Setting fill=False makes the polygon hollow when
# it is drawn.
vp = VectorPlotter(True)
vp.plot(yard, fill=False, edgecolor='blue')
print(yard)

# Move the polygon five units west, by moving the ring.
ring = yard.GetGeometryRef(0)
for i in range(ring.GetPointCount()):
    ring.SetPoint(i, ring.GetX(i) - 5, ring.GetY(i))
vp.plot(yard, fill=False, ec='red', linestyle='dashed')

# Move the yard back to its original location for the next example.
ring = yard.GetGeometryRef(0)
for i in range(ring.GetPointCount()):
    ring.SetPoint(i, ring.GetX(i) + 5, ring.GetY(i))

# Cut off one of the sharp corners by replacing the third vertex with two other
# vertices.
ring = yard.GetGeometryRef(0)
vertices = ring.GetPoints()
vertices[2:3] = ((90, 16), (90, 27))
for i in range(len(vertices)):
    ring.SetPoint(i, *vertices[i])
vp.plot(yard, fill=False, ec='black', ls='dotted', linewidth=3)


#########################  7.4.2  Multiple polygons  ###########################

# Make the garden boxes multipolygon. Create a regular polygon for each raised
# bed, and then add it to the multipolygon.
box1 = ogr.Geometry(ogr.wkbLinearRing)
box1.AddPoint(87.5, 25.5)
box1.AddPoint(89, 25.5)
box1.AddPoint(89, 24)
box1.AddPoint(87.5, 24)
garden1 = ogr.Geometry(ogr.wkbPolygon)
garden1.AddGeometry(box1)

box2 = ogr.Geometry(ogr.wkbLinearRing)
box2.AddPoint(89, 23)
box2.AddPoint(92, 23)
box2.AddPoint(92,22)
box2.AddPoint(89,22)
garden2 = ogr.Geometry(ogr.wkbPolygon)
garden2.AddGeometry(box2)

gardens = ogr.Geometry(ogr.wkbMultiPolygon)
gardens.AddGeometry(garden1)
gardens.AddGeometry(garden2)
gardens.CloseRings()

# Take a look at the multipolygon.
vp.clear()
vp.plot(gardens, fill=False, ec='blue')
vp.zoom(-1)
print(gardens)

# Move the garden boxes on unit east and half a unit north. For each polygon
# contained in the multipolygon, get the ring and edit its vertices.
for i in range(gardens.GetGeometryCount()):
    ring = gardens.GetGeometryRef(i).GetGeometryRef(0)
    for j in range(ring.GetPointCount()):
        ring.SetPoint(j, ring.GetX(j) + 1, ring.GetY(j) + 0.5)
vp.plot(gardens, fill=False, ec='red', ls='dashed')
vp.zoom(-1)

#########################  7.4.3  Polygons with holes  #########################

# Make the yard multipolygon, but this time cut out a hole for the house.
# Make the outer boundary ring first (it's the same as earlier). Then make the
# ring for the house (hole). Then create a polygon and add the rings, making
# sure to add the outer boundary first. Close all of the rings at once by
# calling CloseRings *after* adding all of the rings.
lot = ogr.Geometry(ogr.wkbLinearRing)
lot.AddPoint(58, 38.5)
lot.AddPoint(53, 6)
lot.AddPoint(99.5, 19)
lot.AddPoint(73, 42)

house = ogr.Geometry(ogr.wkbLinearRing)
house.AddPoint(67.5, 29)
house.AddPoint(69, 25.5)
house.AddPoint(64, 23)
house.AddPoint(69, 15)
house.AddPoint(82.5, 22)
house.AddPoint(76, 31.5)

yard = ogr.Geometry(ogr.wkbPolygon)
yard.AddGeometry(lot)
yard.AddGeometry(house)
yard.CloseRings()

# Take a look at the polygon.
vp.clear()
vp.plot(yard, 'yellow')
print(yard)

# Move the yard five units south. Get each ring the same way you would get an
# inner polygon from a multipolygon.
for i in range(yard.GetGeometryCount()):
    ring = yard.GetGeometryRef(i)
    for j in range(ring.GetPointCount()):
        ring.SetPoint(j, ring.GetX(j) - 5, ring.GetY(j))
vp.plot(yard, fill=False, hatch='x', color='blue')


#########################  7.5  Spatial analysis  ##############################

#########################  7.5.1  Overlay tools  ###############################

# Write some code to get results from figures (might already exist somewhere).


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


########################  7.5.2  Proximity tools  ##############################

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
