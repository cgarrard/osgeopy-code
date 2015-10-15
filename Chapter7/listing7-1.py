# Script to reproject a shapefile.

from osgeo import ogr, osr

# Create an output SRS.
sr = osr.SpatialReference()
sr.ImportFromProj4('''+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23
                      +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80
                      +datum=NAD83 +units=m +no_defs''')

# Don't forget to change your directory here.
ds = ogr.Open(r'D:\osgeopy-data\US', 1)

# Get the input layer.
in_lyr = ds.GetLayer('us_volcanos')

# Create the empty output layer.
out_lyr = ds.CreateLayer('us_volcanos_aea', sr,
                         ogr.wkbPoint)
out_lyr.CreateFields(in_lyr.schema)

# Loop through the features in the input layer.
out_feat = ogr.Feature(out_lyr.GetLayerDefn())
for in_feat in in_lyr:

    # Clone the geometry, project it, and add it to the feature.
    geom = in_feat.geometry().Clone()
    geom.TransformTo(sr)
    out_feat.SetGeometry(geom)

    # Copy attributes.
    for i in range(in_feat.GetFieldCount()):
        out_feat.SetField(i, in_feat.GetField(i))

    # Insert the feature
    out_lyr.CreateFeature(out_feat)
