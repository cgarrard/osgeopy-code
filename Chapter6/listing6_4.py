# Make the yard multipolygon, but this time cut out a hole for the house.
# Make the outer boundary ring first (it's the same as earlier). Then make the
# ring for the house (hole). Then create a polygon and add the rings, making
# sure to add the outer boundary first. Close all of the rings at once by
# calling CloseRings *after* adding all of the rings.

# This code is also in chapter6.py so that you can use it with the other examples.

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
