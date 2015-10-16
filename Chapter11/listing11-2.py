# Plot countries as multipolygons.

import matplotlib.pyplot as plt
from osgeo import ogr

def plot_polygon(poly, symbol='k-', **kwargs):
    """Plots a polygon using the given symbol."""
    for i in range(poly.GetGeometryCount()):
        subgeom = poly.GetGeometryRef(i)
        x, y = zip(*subgeom.GetPoints())
        plt.plot(x, y, symbol, **kwargs)

def plot_layer(filename, symbol, layer_index=0, **kwargs):
    """Plots an OGR polygon layer using the given symbol."""
    ds = ogr.Open(filename)

    # Loop through all of the features in the layer.
    for row in ds.GetLayer(layer_index):
        geom = row.geometry()
        geom_type = geom.GetGeometryType()

        # If the geometry is a single polygon.
        if geom_type == ogr.wkbPolygon:
            plot_polygon(geom, symbol, **kwargs)

        # Else if the geometry is a multipolygon, send each
        # part to plot_polygon individually.
        elif geom_type == ogr.wkbMultiPolygon:
            for i in range(geom.GetGeometryCount()):
                subgeom = geom.GetGeometryRef(i)
                plot_polygon(subgeom, symbol, **kwargs)

# Plot countries.
plot_layer(r'D:\osgeopy-data\global\ne_110m_admin_0_countries.shp', 'k-')
plt.axis('equal')

# Get rid of the tick marks on the side of the plot.
plt.gca().get_xaxis().set_ticks([])
plt.gca().get_yaxis().set_ticks([])
plt.show()
