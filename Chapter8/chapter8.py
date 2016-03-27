import os
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



###################  8.2 Using spatial references with OSR  ###################

# import osr so you can work with spatial references.
from osgeo import osr


######################  8.2.1 Spatial reference objects  ######################

# Look at a geographic SRS.
ds = ogr.Open(os.path.join(data_dir, 'US', 'states_48.shp'))
srs = ds.GetLayer().GetSpatialRef()

# Well Known Text (WKT)
print(srs)

# PROJ.4
print(srs.ExportToProj4())

# XML
print(srs.ExportToXML())

# Look at a UTM SRS.
utm_sr = osr.SpatialReference()
utm_sr.ImportFromEPSG(26912)
print(utm_sr) # WKT
print(utm_sr.ExportToProj4()) # PROJ.4
print(utm_sr.ExportToXML()) # XML

# Get the projection name.
print(utm_sr.GetAttrValue('PROJCS'))

# Get the authority.
print(utm_sr.GetAttrValue('AUTHORITY'))
print(utm_sr.GetAttrValue('AUTHORITY', 1))

# Get the datum code.
print(utm_sr.GetAuthorityCode('DATUM'))

# Get the false easting.
print(utm_sr.GetProjParm(osr.SRS_PP_FALSE_EASTING))


##################  8.2.2 Creating spatial reference objects  #################

# Create a UTM SRS from an EPSG code.
sr = osr.SpatialReference()
sr.ImportFromEPSG(26912)
print(sr.GetAttrValue('PROJCS'))

# Create a UTM SRS from a PROJ.4 string.
sr = osr.SpatialReference()
sr.ImportFromProj4('''+proj=utm +zone=12 +ellps=GRS80
                      +towgs84=0,0,0,0,0,0,0 +units=m +no_defs ''')
print(sr.GetAttrValue('PROJCS'))

# Create a unprojected SRS from a WKT string.
wkt = '''GEOGCS["GCS_North_American_1983",
           DATUM["North_American_Datum_1983",
             SPHEROID["GRS_1980",6378137.0,298.257222101]],
           PRIMEM["Greenwich",0.0],
           UNIT["Degree",0.0174532925199433]]'''
sr = osr.SpatialReference(wkt)
print(sr)

# Create an Albers SRS using parameters.
sr = osr.SpatialReference()
sr.SetProjCS('USGS Albers')
sr.SetWellKnownGeogCS('NAD83')
sr.SetACEA(29.5, 45.5, 23, -96, 0, 0)
sr.Fixup()
sr.Validate()
print(sr)


########################  8.2.3 Assigning a SRS to data  ######################

# Make sure that the output folder exists in your data directory before
# trying this example.
out_fn = os.path.join(data_dir, 'output', 'testdata.shp')

# Create an empty shapefile that uses a UTM SRS. If you run this it will
# create the shapefile with a .prj file containing the SRS info.
sr = osr.SpatialReference()
sr.ImportFromEPSG(26912)
ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(out_fn)
lyr = ds.CreateLayer('counties', sr, ogr.wkbPolygon)


#########################  8.2.4 Projecting geometries  #######################

# Get the world landmasses and plot them.
world = pb.get_shp_geom(os.path.join(data_dir, 'global', 'ne_110m_land_1p.shp'))
vp = VectorPlotter(True)
vp.plot(world)

# Create a point for the Eiffel Tower.
tower = ogr.Geometry(wkt='POINT (2.294694 48.858093)')
tower.AssignSpatialReference(osr.SpatialReference(osr.SRS_WKT_WGS84))

# Try to reproject the world polygon to Web Mercator. This should spit out
# an error.
web_mercator_sr = osr.SpatialReference()
web_mercator_sr.ImportFromEPSG(3857)
world.TransformTo(web_mercator_sr)

# Set a config variable and try the projection again.
from osgeo import gdal
gdal.SetConfigOption('OGR_ENABLE_PARTIAL_REPROJECTION', 'TRUE')
web_mercator_sr = osr.SpatialReference()
web_mercator_sr.ImportFromEPSG(3857)
world.TransformTo(web_mercator_sr)
tower.TransformTo(web_mercator_sr)
print(tower)
vp.clear()
vp.plot(world)

# Create a coordinate transformation between Web Mercator and Gall-Peters.
peters_sr = osr.SpatialReference()
peters_sr.ImportFromProj4("""+proj=cea +lon_0=0 +x_0=0 +y_0=0
                             +lat_ts=45 +ellps=WGS84 +datum=WGS84
                             +units=m +no_defs""")
ct = osr.CoordinateTransformation(web_mercator_sr, peters_sr)
world.Transform(ct)
vp.clear()
vp.plot(world)

# Create an unprojected NAD27 SRS and add datum shift info.
sr = osr.SpatialReference()
sr.SetWellKnownGeogCS('NAD27')
sr.SetTOWGS84(-8, 160, 176)
print(sr)



#################################  8.3 pyproj  ################################

#######################  8.3.1 Transforming between SRS  ######################

# Transform lat/lon to UTM.
import pyproj
utm_proj = pyproj.Proj('+proj=utm +zone=31 +ellps=WGS84')
x, y = utm_proj(2.294694, 48.858093)
print(x, y)

# Go back to lat/lon.
x1, y1 = utm_proj(x, y, inverse=True)
print(x1, y1)

# Convert UTM WGS84 coordinates to UTM NAD27.
wgs84 = pyproj.Proj('+proj=utm +zone=18 +datum=WGS84')
nad27 = pyproj.Proj('+proj=utm +zone=18 +datum=NAD27')
x, y = pyproj.transform(wgs84, nad27, 580744.32, 4504695.26)
print(x, y)


#######################  8.3.2 Great-circle calculations  #####################

# Set lat/lon coordinates for Los Angeles and Berlin.
la_lat, la_lon = 34.0500, -118.2500
berlin_lat, berlin_lon = 52.5167, 13.3833

# Create a WGS84 Geod.
geod = pyproj.Geod(ellps='WGS84')

# Get the bearings and distance between LA and Berlin
forward, back, dist = geod.inv(la_lon, la_lat, berlin_lon, berlin_lat)
print('forward: {}\nback: {}\ndist: {}'.format(forward, back, dist))

# Get your final coordinates if you start in Berlin and go dist distance in
# the back direction. These coordinates should match LA.
x, y, bearing = geod.fwd(berlin_lon, berlin_lat, back, dist)
print('{}, {}\n{}'.format(x, y, bearing))

# Get a list of equally spaced coordinates along the great circel from LA
# to Berlin.
coords = geod.npts(la_lon, la_lat, berlin_lon, berlin_lat, 100)

# Only print the first 3.
for i in range(3):
    print(coords[i])
