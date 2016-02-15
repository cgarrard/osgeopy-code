# Create a shapefile from a CSV.

from osgeo import ogr, osr

csv_fn = r"D:\osgeopy-data\Galapagos\Galapagos Albatrosses.csv"
shp_fn = r"D:\osgeopy-data\Galapagos\albatross_dd.shp"
sr = osr.SpatialReference(osr.SRS_WKT_WGS84)

# Create the shapefile with two attribute fields.
shp_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(shp_fn)
shp_lyr = shp_ds.CreateLayer('albatross_dd', sr, ogr.wkbPoint)
shp_lyr.CreateField(ogr.FieldDefn('tag_id', ogr.OFTString))
shp_lyr.CreateField(ogr.FieldDefn('timestamp', ogr.OFTString))
shp_row = ogr.Feature(shp_lyr.GetLayerDefn())

# Open the csv and loop through each row.
csv_ds = ogr.Open(csv_fn)
csv_lyr = csv_ds.GetLayer()
for csv_row in csv_lyr:

    # Get the x,y coordinates from the csv and create a point geometry.
    x = csv_row.GetFieldAsDouble('location-long')
    y = csv_row.GetFieldAsDouble('location-lat')
    shp_pt = ogr.Geometry(ogr.wkbPoint)
    shp_pt.AddPoint(x, y)

    # Get the attribute data from the csv.
    tag_id = csv_row.GetField('individual-local-identifier')
    timestamp = csv_row.GetField('timestamp')

    # Add the data to the shapefile.
    shp_row.SetGeometry(shp_pt)
    shp_row.SetField('tag_id', tag_id)
    shp_row.SetField('timestamp', timestamp)
    shp_lyr.CreateFeature(shp_row)

del csv_ds, shp_ds
