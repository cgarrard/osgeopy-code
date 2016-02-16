import os
import shutil
import numpy as np
from osgeo import gdal, osr


# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
data_dir = r'D:\osgeopy-data'
# data_dir =



##############################  10.1 Ground control points  ####################

# See listing10_1.py, since the example reuses some code from that listing.


#############  10.2 Converting pixel coordinates to another image  #############

# Create a function to get the extent of a raster and try it out on the
# raster just created in listing 10.1. This function is in
def get_extent(fn):
    '''Returns min_x, max_y, max_x, min_y'''
    ds = gdal.Open(fn)
    gt = ds.GetGeoTransform()
    return (gt[0], gt[3], gt[0] + gt[1] * ds.RasterXSize,
        gt[3] + gt[5] * ds.RasterYSize)

# The raster with GCPs doesn't have a geotransform so this extent isn't
# correct.
os.chdir(os.path.join(data_dir, 'Utah'))
print(get_extent('cache.tif'))

# But this one is.
print(get_extent('cache2.tif'))

# Extra examples...
# Remember the vashon.tif file created in the last chapter? Let's use it
# for a transformer example.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
vashon_ds = gdal.Open('vashon.tif')
full_ds = gdal.Open('nat_color.tif')

# Create a transformer that will map pixel coordinates from the Vashon
# dataset into the full one.
trans = gdal.Transformer(vashon_ds, full_ds, [])

# Use the transformer to figure out the pixel offsets in the full image
# that correspond with the upper left corner of the vashon one.
success, xyz = trans.TransformPoint(False, 0, 0)
print(success, xyz)

# If we use the output from that and go the reverse direction, we'll get the
# upper left corner for vashon.
success, xyz = trans.TransformPoint(True, 6606, 3753)
print(success, xyz)



##############################  10.3 Color tables  #############################

# Make a copy of the raster we just created in listing 10.3.
os.chdir(os.path.join(data_dir, 'Switzerland'))
original_ds = gdal.Open('dem_class2.tif')
ds = original_ds.GetDriver().CreateCopy('dem_class3.tif', original_ds)

# Get the existing color table from the band.
band = ds.GetRasterBand(1)
colors = band.GetRasterColorTable()

# Change the entry for 5.
colors.SetColorEntry(5, (250, 250, 250))

# Set the modified color table back on the raster.
band.SetRasterColorTable(colors)
del band, ds



#############################  10.3.1 Transparency  ############################

# Let's take the output from listing 10.3 and add some transparency. We have
# to make a copy of the dataset, though, so we can add the alpha band.
os.chdir(os.path.join(data_dir, 'Switzerland'))
original_ds = gdal.Open('dem_class2.tif')
driver = gdal.GetDriverByName('gtiff')

# This is the only line shown in the text. The rest of the copy code is
# left out for space reasons (and because you know all about it by now).
ds = driver.Create('dem_class4.tif', original_ds.RasterXSize,
    original_ds.RasterYSize, 2, gdal.GDT_Byte, ['ALPHA=YES'])

# Add the projection and and geotransform info to the copy.
ds.SetProjection(original_ds.GetProjection())
ds.SetGeoTransform(original_ds.GetGeoTransform())

# Read the data in from dem_class2.
original_band1 = original_ds.GetRasterBand(1)
data = original_band1.ReadAsArray()

# Write the data to band 1 of the new raster and copy the color table over.
band1 = ds.GetRasterBand(1)
band1.WriteArray(data)
band1.SetRasterColorTable(original_band1.GetRasterColorTable())
band1.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
band1.SetNoDataValue(original_band1.GetNoDataValue())

ds.FlushCache()


# Now that we're finally done copying, go back to the text and find
# everywhere in the data array that the pixel value is 5 and set
# the value to 65 instead. Set everything else to 255.
import numpy as np
data = band1.ReadAsArray()
data = np.where(data == 5, 65, 255)

# Now write the modified data array to the second (alpha) band in the new
# raster.
band2 = ds.GetRasterBand(2)
band2.WriteArray(data)
band2.SetRasterColorInterpretation(gdal.GCI_AlphaBand)

del ds, original_ds

# To get this output to render correctly in QGIS, you might have to change
# the symbology. Open up the Layer Properties dialog, go to the Style tab,
# and choose Pletted for the Render type. Try putting the swiss_dem raster
# under it so you can see the transparency.



###############################  10.4 Histograms  ##############################

# Look at approximate vs exact histogram values.
os.chdir(os.path.join(data_dir, 'Switzerland'))
ds = gdal.Open('dem_class2.tif')
band = ds.GetRasterBand(1)
approximate_hist = band.GetHistogram()
exact_hist = band.GetHistogram(approx_ok=False)
print('Approximate:', approximate_hist[:7], sum(approximate_hist))
print('Exact:', exact_hist[:7], sum(exact_hist))

# Look at the current default histogram.
print(band.GetDefaultHistogram())

# Change the default histogram so that it lumps 1 & 2, 3 & 4, and leaves 5
# by itself.
hist = band.GetHistogram(0.5, 6.5, 3, approx_ok=False)
band.SetDefaultHistogram(1, 6, hist)

# Look at what the default histogram is now.
print(band.GetDefaultHistogram())

# Get the individual bits of data from the default histogram.
min_val, max_val, n, hist = band.GetDefaultHistogram()
print(min_val, max_val, n)
print(hist)



##################################  10.6 VRTs  #################################

# XML defining a VRT band. It uses the first band in whatever dataset it's
# pointed to with the SourceFilename tag.
xml = '''
<SimpleSource>
  <SourceFilename>{0}</SourceFilename>
  <SourceBand>1</SourceBand>
</SimpleSource>
'''

# Create a 3-band VRT with the same dimensions as one of the Landsat bands.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
tmp_ds = gdal.Open('p047r027_7t20000730_z10_nn30.tif')
driver = gdal.GetDriverByName('vrt')
ds = driver.Create('nat_color.vrt', tmp_ds.RasterXSize,
    tmp_ds.RasterYSize, 3)
ds.SetProjection(tmp_ds.GetProjection())
ds.SetGeoTransform(tmp_ds.GetGeoTransform())

# Point the VRT to the 3 individual GeoTIFFs holding the Landsat bands.
# The bands are stored in the VRT in the order you add them, so we add
# them in 3,2,1 order so that we get RGB.
metadata = {'source_0': xml.format('p047r027_7t20000730_z10_nn30.tif')}
ds.GetRasterBand(1).SetMetadata(metadata, 'vrt_sources')

metadata = {'source_0': xml.format('p047r027_7t20000730_z10_nn20.tif')}
ds.GetRasterBand(2).SetMetadata(metadata, 'vrt_sources')

metadata = {'source_0': xml.format('p047r027_7t20000730_z10_nn10.tif')}
ds.GetRasterBand(3).SetMetadata(metadata, 'vrt_sources')

del ds, tmp_ds


##########################  10.6.2 Troublesome formats  ########################

# Use the VRT created in listing 9.5 to create a jpeg of Vashon Island.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
ds = gdal.Open('vashon.vrt')
gdal.GetDriverByName('jpeg').CreateCopy('vashon.jpg', ds)



##########################  10.6.3 Reprojecting images  ########################

# Reproject the nat_color.tif from UTM to unprojected lat/lon. First create
# the output SRS.
srs = osr.SpatialReference()
srs.SetWellKnownGeogCS('WGS84')

# Open the nat_color file.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
old_ds = gdal.Open('nat_color.tif')

# Create a VRT in memory that does the reproject.
vrt_ds = gdal.AutoCreateWarpedVRT(old_ds, None, srs.ExportToWkt(),
    gdal.GRA_Bilinear)

# Copy the VRT to a GeoTIFF so we have a file on disk.
gdal.GetDriverByName('gtiff').CreateCopy('nat_color_wgs84.tif', vrt_ds)



###########################  10.7 Callback functions  ##########################

# Let's calculate statistics on the natural color Landsat image and show
# progress while it does it (this image probably already has stats, so this
# will go really fast). Watch your output window to see what happens.
os.chdir(os.path.join(data_dir, 'Landsat', 'Washington'))
ds = gdal.Open('nat_color.tif')
for i in range(ds.RasterCount):
    ds.GetRasterBand(i + 1).ComputeStatistics(False, gdal.TermProgress_nocb)


# How about using the gdal callback function with my own stuff? Let's just
# list all of the files in the current diretory and pretend to do something
# with them.
def process_file(fn):
    # Slow things down a bit by counting to 1,000,000 for each file.
    for i in range(1000000):
        pass # do nothing

list_of_files = os.listdir('.')
for i in range(len(list_of_files)):
    process_file(list_of_files[i])
    gdal.TermProgress_nocb(i / float(len(list_of_files)))
gdal.TermProgress_nocb(100)



######################  10.8 Exceptions and error handlers  ####################

os.chdir(os.path.join(data_dir, 'Switzerland'))

# This will fail because the second filename has an extra f at the end. The
# first one is the only one that will get statistics calculated.
file_list = ['dem_class.tif', 'dem_class2.tiff', 'dem_class3.tif']
for fn in file_list:
    ds = gdal.Open(fn)
    ds.GetRasterBand(1).ComputeStatistics(False)

# You could check to see if the file could be opened and skip it if not.
for fn in file_list:
    ds = gdal.Open(fn)
    if ds is None:
        print('Could not compute stats for ' + fn)
    else:
        print('Computing stats for ' + fn)
        ds.GetRasterBand(1).ComputeStatistics(False)

# Or you could use exceptions and a try/except block.
gdal.UseExceptions()
for fn in file_list:
    try:
        ds = gdal.Open(fn)
        ds.GetRasterBand(1).ComputeStatistics(False)
    except:
        print('Could not compute stats for ' + fn)
        # Uncomment this if you also want it to print the gdal error message.
        # print(gdal.GetLastErrorMsg())

# Turn exceptions off.
gdal.DontUseExceptions()

# How about the second example, but without the gdal error message?
gdal.PushErrorHandler('CPLQuietErrorHandler')
for fn in file_list:
    ds = gdal.Open(fn)
    if ds is None:
        print('Could not compute stats for ' + fn)
    else:
        print('Computing stats for ' + fn)
        ds.GetRasterBand(1).ComputeStatistics(False)

# Get the default error handler back.
gdal.PopErrorHandler()

# Call the error function yourself.
def do_something(ds1, ds2):
    if ds1.GetProjection() != ds2.GetProjection():
        gdal.Error(gdal.CE_Failure, gdal.CPLE_AppDefined,
            'Datasets must have the same SRS')
        return False
    # now do your stuff
ds1 = gdal.Open(os.path.join(data_dir, 'Switzerland', 'dem_class.tif'))
ds2 = gdal.Open(os.path.join(data_dir, 'Landsat', 'Washington', 'nat_color.tif'))
do_something(ds1, ds2)
del ds1, ds2

# Create your own error handler.
import ospybook as pb
def log_error_handler(err_class, err_no, msg):
    logging.error('{} - {}: {}'.format(
        pb.get_gdal_constant_name('CE', err_class),
        pb.get_gdal_constant_name('CPLE', err_no),
        msg))

# Use your custom error handler to print messages to the screen.
import logging
gdal.PushErrorHandler(log_error_handler)
ds1 = gdal.Open(os.path.join(data_dir, 'Switzerland', 'dem_class.tif'))
ds2 = gdal.Open(os.path.join(data_dir, 'Landsat', 'Washington', 'nat_color.tif'))
do_something(ds1, ds2)
del ds1, ds2

# Or use it to write to a file (change to file path!).
import logging
logging.basicConfig(filename='d:/temp/log.txt')
gdal.PushErrorHandler(log_error_handler)
ds1 = gdal.Open(os.path.join(data_dir, 'Switzerland', 'dem_class.tif'))
ds2 = gdal.Open(os.path.join(data_dir, 'Landsat', 'Washington', 'nat_color.tif'))
do_something(ds1, ds2)
del ds1, ds2



######################  Get constant names with ospybook  #####################

import ospybook as pb

# Get the GDT constant that has a value of 5.
print(pb.get_gdal_constant_name('GDT', 5))
