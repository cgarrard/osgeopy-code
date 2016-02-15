# Script to combine small polygons from the wind farm example.
from osgeo import ogr

# Open the original output layer and create a new one.
folder = r'D:\osgeopy-data\California'
ds = ogr.Open(folder, True)
in_lyr = ds.GetLayerByName('wind_farm')
out_lyr = ds.CreateLayer(
    'wind_farm2', in_lyr.GetSpatialRef(), ogr.wkbPolygon)
out_row = ogr.Feature(out_lyr.GetLayerDefn())

# Create a multipolygon to hold the small polygons to be combined.
multipoly = ogr.Geometry(ogr.wkbMultiPolygon)

# Loop through the rows in the original output and get the geometry.
for in_row in in_lyr:
    in_geom = in_row.geometry().Clone()
    in_geom_type = in_geom.GetGeometryType()

    # If the geometry is a polygon, go ahead and add it to the multipolygon.
    if in_geom_type == ogr.wkbPolygon:
        multipoly.AddGeometry(in_geom)

    # But if it's a multipoly, break it up and add each polygon individually.
    elif in_geom_type == ogr.wkbMultiPolygon:
        for i in range(in_geom.GetGeometryCount()):
            multipoly.AddGeometry(
                in_geom.GetGeometryRef(i))

# Union all of the small polygons together. This will create a new
# multipolygon.
multipoly = multipoly.UnionCascaded()

# Now loop through the single polygons contained in the unioned multipolygon
# and write them out to the new layer if they have a large enough area.
for i in range(multipoly.GetGeometryCount()):
    poly = multipoly.GetGeometryRef(i)
    if poly.GetArea() > 1000000:
        out_row.SetGeometry(poly)
        out_lyr.CreateFeature(out_row)
del ds
