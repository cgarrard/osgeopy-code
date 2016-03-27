# Script to subset a raster using a VRT.

import os
from osgeo import gdal

# Change your directory.
os.chdir(r'D:\osgeopy-data\Landsat\Washington')

# Open the original raster and get its geotransform info.
tmp_ds = gdal.Open('nat_color.tif')
tmp_gt = tmp_ds.GetGeoTransform()

# Make sure the inverse geotransform worked. Remember that InvGeoTransform
# returns a success flag and the new geotransform in GDAL 1.x but just the
# new geotransform or None in GDAL 2.x.
inv_gt = gdal.InvGeoTransform(tmp_gt)
if gdal.VersionInfo()[0] == '1':
    if inv_gt[0] == 1:
        inv_gt = inv_gt[1]
    else:
        raise RuntimeError('Inverse geotransform failed')
elif inv_gt is None:
    raise RuntimeError('Inverse geotransform failed')

# Figure out what the new geotransform is.
vashon_ul = (532000, 5262600)
vashon_lr = (548500, 5241500)
ulx, uly = map(int, gdal.ApplyGeoTransform(inv_gt, *vashon_ul))
lrx, lry = map(int, gdal.ApplyGeoTransform(inv_gt, *vashon_lr))
rows = lry - uly
columns = lrx - ulx
gt = list(tmp_gt)
gt[0] += gt[1] * ulx
gt[3] += gt[5] * uly

# Create the output VRT, which is really just an XML file.
ds = gdal.GetDriverByName('vrt').Create('vashon3.vrt', columns, rows, 3)
ds.SetProjection(tmp_ds.GetProjection())
ds.SetGeoTransform(gt)

# The XML definition for each band in the output.
xml = '''
<SimpleSource>
  <SourceFilename relativeToVRT="1">{fn}</SourceFilename>
  <SourceBand>{band}</SourceBand>
  <SrcRect xOff="{xoff}" yOff="{yoff}"
           xSize="{cols}" ySize="{rows}" />
  <DstRect xOff="0" yOff="0"
           xSize="{cols}" ySize="{rows}" />
</SimpleSource>
'''

# The data that will be used to fill the placeholders in the XML.
data = {'fn': 'nat_color.tif', 'band': 1,
        'xoff': ulx, 'yoff': uly,
        'cols': columns, 'rows': rows}

# Add the first band.
meta = {'source_0': xml.format(**data)}
ds.GetRasterBand(1).SetMetadata(meta, 'vrt_sources')

# Change the XML so it's pointing to the second band in the full
# dataset and then add band 2 to the output.
data['band'] = 2
meta = {'source_0': xml.format(**data)}
ds.GetRasterBand(2).SetMetadata(meta, 'vrt_sources')

data['band'] = 3
meta = {'source_0': xml.format(**data)}
ds.GetRasterBand(3).SetMetadata(meta, 'vrt_sources')

del ds, tmp_ds
