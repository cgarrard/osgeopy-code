# Script to run a bilinear interpolation

from osgeo import gdal
import listing11_12
import listing11_13

in_fn = r"D:\osgeopy-data\Nepal\everest.tif"
out_fn = r'D:\Temp\everest_bilinear.tif'
cell_size = (0.02, -0.02)

in_ds = gdal.Open(in_fn)
x, y = listing11_12.get_indices(in_ds, *cell_size)
outdata = listing11_13.bilinear(in_ds.ReadAsArray(), x, y)

driver = gdal.GetDriverByName('GTiff')
rows, cols = outdata.shape
out_ds = driver.Create(
    out_fn, cols, rows, 1, gdal.GDT_Int32)
out_ds.SetProjection(in_ds.GetProjection())

gt = list(in_ds.GetGeoTransform())
gt[1] = cell_size[0]
gt[5] = cell_size[1]
out_ds.SetGeoTransform(gt)

out_band = out_ds.GetRasterBand(1)
out_band.WriteArray(outdata)
out_band.FlushCache()
out_band.ComputeStatistics(False)
