import matplotlib.pyplot as plt
from osgeo import ogr

def plot_polygon(poly, symbol='k-', **kwargs):
    """Plots a polygon using the given symbol."""
    for i in range(poly.GetGeometryCount()):
        subgeom = poly.GetGeometryRef(i)
        x, y = zip(*subgeom.GetPoints())
        plt.plot(x, y, symbol, **kwargs)
