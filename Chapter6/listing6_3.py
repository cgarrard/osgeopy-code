# Make the garden boxes multipolygon. Create a regular polygon for each raised
# bed, and then add it to the multipolygon.

# This code is also in chapter6.py so that you can use it with the other examples.

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
