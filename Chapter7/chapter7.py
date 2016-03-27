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



##########################  7.1  Overlay tools  ###############################

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


#########################  7.2  Proximity tools  ##############################

# Open layers for examples.
shp_ds = ogr.Open(os.path.join(data_dir, 'US'))
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')
cities_lyr = shp_ds.GetLayer('cities_albers')

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


############################  7.3  Wind farms  ################################

# Open the census layer and add a field containing population per square
# kilometer.
census_fn = os.path.join(data_dir, 'California', 'ca_census_albers.shp')
census_ds = ogr.Open(census_fn, True)
census_lyr = census_ds.GetLayer()
density_field = ogr.FieldDefn('popsqkm', ogr.OFTReal)
census_lyr.CreateField(density_field)
for row in census_lyr:
    pop = row.GetField('HD01_S001')
    sqkm = row.geometry().GetArea() / 1000000
    row.SetField('popsqkm', pop / sqkm)
    census_lyr.SetFeature(row)

# Get the Imperial County geomtery.
county_fn = os.path.join(data_dir, 'US', 'countyp010.shp')
county_ds = ogr.Open(county_fn)
county_lyr = county_ds.GetLayer()
county_lyr.SetAttributeFilter("COUNTY ='Imperial County'")
county_row = next(county_lyr)
county_geom = county_row.geometry().Clone()
del county_ds

# Transform the county geometry to the same spatial reference as the census
# data and then use it as a spatial filter on the census data.
county_geom.TransformTo(census_lyr.GetSpatialRef())
census_lyr.SetSpatialFilter(county_geom)

# Set an attribute filter based on the population field you created a minute
# ago.
census_lyr.SetAttributeFilter('popsqkm < 0.5')

# Open the wind layer and select the polygons with a good enough wind rating.
wind_fn = os.path.join(data_dir, 'California', 'california_50m_wind_albers.shp')
wind_ds = ogr.Open(wind_fn)
wind_lyr = wind_ds.GetLayer()
wind_lyr.SetAttributeFilter('WPC >= 3')

# Create a shapefile to hold the output data.
out_fn = os.path.join(data_dir, 'California', 'wind_farm.shp')
out_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(out_fn)
out_lyr = out_ds.CreateLayer('wind_farm', wind_lyr.GetSpatialRef(), ogr.wkbPolygon)
out_lyr.CreateField(ogr.FieldDefn('wind', ogr.OFTInteger))
out_lyr.CreateField(ogr.FieldDefn('popsqkm', ogr.OFTReal))
out_row = ogr.Feature(out_lyr.GetLayerDefn())

# The following code is the same as listing 7.3.
# Loop through the census rows and intersect the census geometry with the
# county geometry and use that as a spatial filter on the wind data.
for census_row in census_lyr:
    census_geom = census_row.geometry()
    census_geom = census_geom.Intersection(county_geom)
    wind_lyr.SetSpatialFilter(census_geom)

    print('Intersecting census tract with {0} wind polygons'.format(
        wind_lyr.GetFeatureCount()))

    # Only bother with adding new rows to the output if there are wind
    # polygons selected by the filters.
    if wind_lyr.GetFeatureCount() > 0:
        out_row.SetField('popsqkm', census_row.GetField('popsqkm'))
        for wind_row in wind_lyr:
            wind_geom = wind_row.geometry()

            # Again, only bother with adding rows to the output if there is
            # an intersection to add.
            if census_geom.Intersect(wind_geom):
                new_geom = census_geom.Intersection(wind_geom)
                out_row.SetField('wind', wind_row.GetField('WPC'))
                out_row.SetGeometry(new_geom)
                out_lyr.CreateFeature(out_row)
del out_ds


##########################  7.3  Animal tracking  #############################

# Delete the bad points from the output of listing 7.5.
shp_fn = os.path.join(data_dir, 'Galapagos', 'albatross_dd.shp')
shp_ds = ogr.Open(shp_fn, True)
shp_lyr = shp_ds.GetLayer()
shp_lyr.SetSpatialFilterRect(-1, -1, 1, 1)
for shp_row in shp_lyr:
    shp_lyr.DeleteFeature(shp_row.GetFID())
shp_lyr.SetSpatialFilter(None)
shp_ds.ExecuteSQL('REPACK ' + shp_lyr.GetName())
shp_ds.ExecuteSQL('RECOMPUTE EXTENT ON ' + shp_lyr.GetName())
del shp_ds

# ogr2ogr command for projecting the shapefile. You need to run this from the
# folder containing the shapefile.
ogr2ogr -f "ESRI Shapefile" -t_srs "+proj=lcc +lat_1=-5 +lat_2=-42 +lat_0=-32 +lon_0=-60 +x_0=0 +y_0=0 +ellps=aust_SA +units=m +no_defs" albatross_lambert.shp albatross_dd.shp


# Function to get unique values from an attribute field. This is in the
# ch7funcs module.
def get_unique(datasource, layer_name, field_name):
    sql = 'SELECT DISTINCT {0} FROM {1}'.format(field_name, layer_name)
    lyr = datasource.ExecuteSQL(sql)
    values = []
    for row in lyr:
        values.append(row.GetField(field_name))
    datasource.ReleaseResultSet(lyr)
    return values

# Get the maximum distance between GPS fixes for each animal tag.
ds = ogr.Open(os.path.join(data_dir, 'Galapagos'))
for tag_id in get_unique(ds, 'albatross_lambert', 'tag_id'):
    sql = """SELECT MAX(distance) FROM albatross_lambert
             WHERE tag_id = '{0}'""".format(tag_id)
    lyr = ds.ExecuteSQL(sql)
    for row in lyr:
        print '{0}: {1}'.format(tag_id, row.GetField(0))
