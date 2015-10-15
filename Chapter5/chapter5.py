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
# data_dir = r'D:\osgeopy-data'
data_dir =



########################  5.1  Attribute filters  #############################

# Set up an interactive plotter. Because this is the most fun if you do it
# interactively, you'll probably want to do it from the Python interactive
# prompt. If you're going to run it as a script instead, you might want to use
# a non-interactive plotter instead. Just remember to call draw() when you're
# done.
vp = VectorPlotter(True)

# Get the countries shapefile layer
ds = ogr.Open(os.path.join(data_dir, 'global'))
lyr = ds.GetLayer('ne_50m_admin_0_countries')

# Plot the countries with no fill and also print out the first 4 attribute
# records.
vp.plot(lyr, fill=False)
pb.print_attributes(lyr, 4, ['name'], geom=False)

# Apply a filter that finds countries in Asia and see how many records there
# are now.
lyr.SetAttributeFilter('continent = "Asia"')
lyr.GetFeatureCount()

# Draw the Asian countries in yellow and print out a few features.
vp.plot(lyr, 'y')
pb.print_attributes(lyr, 4, ['name'], geom=False)

# You can still get a feature that is not in Asia by using its FID.
lyr.GetFeature(2).GetField('name')

# Set a new filter that selects South American countries and show the results
# in blue. The old filter is no longer in effect.
lyr.SetAttributeFilter('continent = "South America"')
vp.plot(lyr, 'b')

# Clear all attribute filters.
lyr.SetAttributeFilter(None)
lyr.GetFeatureCount()



##########################  5.2  Spatial filters  #############################

# Set up an interactive plotter.
vp = VectorPlotter(True)

# Get the Germany polygon. Make sure to plot the full layer before setting the
# filter, or you'll only plot Germany (or you could clear the filter and then
# plot).
ds = ogr.Open(os.path.join(data_dir, 'global'))
country_lyr = ds.GetLayer('ne_50m_admin_0_countries')
vp.plot(country_lyr, fill=False)
country_lyr.SetAttributeFilter('name = "Germany"')
feat = country_lyr.GetNextFeature()
germany = feat.geometry().Clone()

# Plot world cities as yellow dots.
city_lyr = ds.GetLayer('ne_50m_populated_places')
city_lyr.GetFeatureCount()
vp.plot(city_lyr, 'y.')

# Use the Germany polygon to set a spatial filter and draw the result as blue
# circles.
city_lyr.SetSpatialFilter(germany)
city_lyr.GetFeatureCount()
vp.plot(city_lyr, 'bo')

# Add an attribute filter to find the cities with a population over 1,000,000
# and draw them as red squares. Since the spatial filter is still in effect,
# you should only get large cities in Germany.
city_lyr.SetAttributeFilter('pop_min > 1000000')
city_lyr.GetFeatureCount()
vp.plot(city_lyr, 'rs')

# Remove the spatial filter so now you get global cities with a population
# over 1,000,000. Draw the results as magenta triangles.
city_lyr.SetSpatialFilter(None)
city_lyr.GetFeatureCount()
vp.plot(city_lyr, 'm^', markersize=8)

# Clear the plot and then replot country outlines.
vp.clear()
country_lyr.SetAttributeFilter(None)
vp.plot(country_lyr, fill=False)

# Set a spatial filter using bounding coordinates and draw the result in yellow.
country_lyr.SetSpatialFilterRect(110, -50, 160, 10)
vp.plot(country_lyr, 'y')



########################  To clone or not to clone?  ###########################

# Get a sample layer and the first feature from it.
ds = ogr.Open(os.path.join(data_dir, 'global'))
lyr = ds.GetLayer('ne_50m_admin_0_countries')
feat = lyr.GetNextFeature()

# Now get the feature's geometry and also a clone of that geometry.
geom = feat.geometry()
geom_clone = feat.geometry().Clone()

# Set the feat variable to a new feature, so the original one is no longer
# accessible.
feat = lyr.GetNextFeature()

# Try to get the area of the cloned polygon. This should work just fine.
print(geom_clone.GetArea())

# Try to get the area of the original polygon. This should cause Python to
# crash because the polygon is linked to the feature that is no longer
# available.
print(geom.GetArea())

# Here are some more examples that would all cause Python to crash for similar
# reasons.
fn = os.path.join(data_dir, 'global')

# Neither the data source or layer are stored in memory.
feat = ogr.Open(fn, 0).GetLayer(0).GetNextFeature()

# The data source is not stored in memory.
lyr = ogr.Open(fn, 0).GetLayer(0)
feat = lyr.GetNextFeature()

# The data source is deleted from memory
ds = ogr.Open(fn, 0)
lyr = ds.GetLayer(0)
del ds
feat = lyr.GetNextFeature()



######################  5.3  Using SQL to create temp layers  #################

# Use the OGR SQL dialect and a shapefile to order the world's countries by
# population in descending order and print out the first three (which will be
# the ones with the highest population since you used descending order).
ds = ogr.Open(os.path.join(data_dir, 'global'))
sql = '''SELECT ogr_geom_area as area, name, pop_est
         FROM 'ne_50m_admin_0_countries' ORDER BY POP_EST DESC'''
lyr = ds.ExecuteSQL(sql)
pb.print_attributes(lyr, 3)

# Use the SQLite dialect and a SQLite database to do the same thing, but now
# you can limit the result set itself to three records. This will only work if
# you have SQLite support.
ds = ogr.Open(os.path.join(data_dir, 'global',
                           'natural_earth_50m.sqlite'))
sql = '''SELECT geometry, area(geometry) AS area, name, pop_est
         FROM countries ORDER BY pop_est DESC LIMIT 3'''
lyr = ds.ExecuteSQL(sql)
pb.print_attributes(lyr)

# Join the populated places and country shapefiles together so that you can
# see information about cities but also the countries that they're in, at the
# same time. This uses the default OGR dialect.
ds = ogr.Open(os.path.join(data_dir, 'global'))
sql = '''SELECT pp.name AS city, pp.pop_min AS city_pop,
             c.name AS country, c.pop_est AS country_pop
         FROM ne_50m_populated_places pp
         LEFT JOIN ne_50m_admin_0_countries c
         ON pp.adm0_a3 = c.adm0_a3
         WHERE pp.adm0cap = 1'''
lyr = ds.ExecuteSQL(sql)
pb.print_attributes(lyr, 3, geom=False)

# Try plotting the results to see that it returns cities, not countries.
vp = VectorPlotter(True)
vp.plot(lyr)

# You can also compute data on the fly. Multiplying pp.pop_min by 1.0 turns
# it into a float so that the math works. Otherwise it does integer math and
# percent is 0. Instead of '1.0 * pp.pop_min', you could also do something like
# 'CAST(pp.pop_min AS float(10))'. This example is not in the text.
ds = ogr.Open(os.path.join(data_dir, 'global'))
sql = '''SELECT pp.name AS city, pp.pop_min AS city_pop,
             c.name AS country, c.pop_est AS country_pop,
             1.0 * pp.pop_min / c.pop_est * 100  AS percent
         FROM ne_50m_populated_places pp
         LEFT JOIN ne_50m_admin_0_countries c
         ON pp.adm0_a3 = c.adm0_a3
         WHERE pp.adm0cap = 1'''
lyr = ds.ExecuteSQL(sql)
pb.print_attributes(lyr, 3, geom=False)

# Join two shapefiles again, but this time use the SQLite dialect. Now you can
# also include fields from the secondary (countries) table in the WHERE clause.
# You could also include a LIMIT if you wanted.
ds = ogr.Open(os.path.join(data_dir, 'global'))
sql = '''SELECT pp.name AS city, pp.pop_min AS city_pop,
             c.name AS country, c.pop_est AS country_pop
         FROM ne_50m_populated_places pp
         LEFT JOIN ne_50m_admin_0_countries c
         ON pp.adm0_a3 = c.adm0_a3
         WHERE pp.adm0cap = 1 AND c.continent = "South America"'''
lyr = ds.ExecuteSQL(sql, dialect='SQLite')
pb.print_attributes(lyr, 3)

# Plot the counties in California.
ds = ogr.Open(os.path.join(data_dir, 'US'))
sql = 'SELECT * FROM countyp010 WHERE state = "CA"'
lyr = ds.ExecuteSQL(sql)
vp = VectorPlotter(True)
vp.plot(lyr, fill=False)

# Union the counties together and plot the result. This will only work if you
# have SpatiaLite support.
sql = 'SELECT st_union(geometry) FROM countyp010 WHERE state = "CA"'
lyr = ds.ExecuteSQL(sql, dialect='SQLite')
vp.plot(lyr, 'w')

# Do the same with PostGIS, but only if you've set up a PostGIS server and
# loaded your data in.
conn_str = 'PG:host=localhost user=chrisg password=mypass dbname=geodata'
ds = ogr.Open(conn_str)
sql = "SELECT st_union(geom) FROM us.counties WHERE state = 'CA'"
lyr = ds.ExecuteSQL(sql)
vp.plot(lyr)



#####################  5.4  Taking advantage of filters  ######################

# Use a filter and CopyLayer to easily copy all capital cities to a new
# shapefile.
ds = ogr.Open(os.path.join(data_dir, 'global'), 1)

# Open the global cities shapefile and set a filter for capital cities.
in_lyr = ds.GetLayer('ne_50m_populated_places')
in_lyr.SetAttributeFilter("FEATURECLA = 'Admin-0 capital'")

# Copy the filtered layer to a new shapefile.
out_lyr = ds.CopyLayer(in_lyr, 'capital_cities2')
out_lyr.SyncToDisk()


# Use ExecuteSQL to pull out just a few attributes and copy that to a new
# shapefile.
sql = """SELECT NAME, ADM0NAME FROM ne_50m_populated_places
         WHERE FEATURECLA = 'Admin-0 capital'"""
in_lyr2 = ds.ExecuteSQL(sql)
out_lyr2 = ds.CopyLayer(in_lyr2, 'capital_cities3')
out_lyr2.SyncToDisk()

del ds
