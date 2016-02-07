import os
from osgeo import ogr
from ospybook.vectorplotter import VectorPlotter


# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
data_dir = r'D:\osgeopy-data'
# data_dir =



#########################  6.2  Working with points  ##########################

###########################  6.2.1  Single points  ############################

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



###########################  6.2.2  Multiple points  ##########################

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



#########################  6.3  Working with lines  ###########################

###########################  6.3.1  Single lines  #############################

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



###########################  The Python *-operator  ###########################

pt = ogr.Geometry(ogr.wkbPoint)
vertex = (10, 20)

# Resolves to pt.AddPoint(10, 20), which works
pt.AddPoint(*vertex)

# Resolves to pt.AddPoint((10, 20)), which fails because only one thing
# (a tuple) is getting passed to AddPoint.
pt.AddPoint(vertex)



###########################  6.3.2  Multiple lines  ###########################

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



#########################  6.4  Working with polygons  ########################

#########################  6.4.1  Single polygons  ############################

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


#########################  6.4.2  Multiple polygons  ##########################

# Make the garden boxes multipolygon. Create a regular polygon for each raised
# bed, and then add it to the multipolygon. This is the code in listing 6.3.
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


#########################  6.4.3  Polygons with holes  #########################

# Make the yard multipolygon, but this time cut out a hole for the house.
# Make the outer boundary ring first (it's the same as earlier). Then make the
# ring for the house (hole). Then create a polygon and add the rings, making
# sure to add the outer boundary first. Close all of the rings at once by
# calling CloseRings *after* adding all of the rings. This is the code from
# listing 6.4.
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
