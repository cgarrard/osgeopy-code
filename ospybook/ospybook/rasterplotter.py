import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

class RasterPlotter(object):

    def __init__(self):
        pass

    def plot_fn(self, fn):
        ds = gdal.Open(fn)
        data = ds.ReadAsArray()
        print(data.shape)
        if data.ndim == 2:
            plt.imshow(np.ma.masked_equal(data, 0), cmap='gray')
        elif data.shape[0] == 3:
            plt.imshow(np.transpose(data, (1, 2, 0)))
        else:
            print('nope')
        plt.show()

    def plot_band(self, band, cmap=None, nodata=None):
        if not cmap:
            ctable = band.GetColorTable()
            if ctable:
                colors = []
                for i in range(ctable.GetCount()):
                    colors.append([n / 255.0 for n in ctable.GetColorEntry(i)])
                cmap = matplotlib.colors.ListedColormap(colors)
            else:
                cmap = 'gray'
        data = band.ReadAsArray()
        if nodata is not None:
            data = np.ma.masked_equal(data, nodata)
        elif band.GetNoDataValue() is not None:
            data = np.ma.masked_equal(data, band.GetNoDataValue())
        plt.imshow(data, cmap)
        # plt.colorbar()
        plt.show()

fn = r"D:\osgeopy-data\Utah\cache_utm.tif"
fn = r"D:\osgeopy-data\Landsat\Washington\vashon.tif"
fn = r"D:\GeoData\Utah\ut_landcover_erdas\landcover.img"
rp = RasterPlotter()
rp.plot_fn(fn)
