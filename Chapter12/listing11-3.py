# Plot world features as points, lines, and polygons.

import os
import matplotlib.pyplot as plt
from osgeo import ogr

# This is the function from listing 11.2.
def plot_polygon(poly, symbol='k-', **kwargs):
    """Plots a polygon using the given symbol."""
    for i in range(poly.GetGeometryCount()):
        subgeom = poly.GetGeometryRef(i)
        x, y = zip(*subgeom.GetPoints())
        plt.plot(x, y, symbol, **kwargs)

# Use this function to fill polygons (shown shortly after
# this listing in the text). Uncomment this one and comment
# out the one above.
# def plot_polygon(poly, symbol='w', **kwargs):
#     """Plots a polygon using the given symbol."""
#     for i in range(poly.GetGeometryCount()):
#         x, y = zip(*poly.GetGeometryRef(i).GetPoints())
#         plt.fill(x, y, symbol, **kwargs)


# This function is new.
def plot_line(line, symbol='k-', **kwargs):
    """Plots a line using the given symbol."""
    x, y = zip(*line.GetPoints())
    plt.plot(x, y, symbol, **kwargs)

# This function is new.
def plot_point(point, symbol='ko', **kwargs):
    """Plots a point using the given symbol."""
    x, y = point.GetX(), point.GetY()
    plt.plot(x, y, symbol, **kwargs)

# More code for lines and points has been added to this function
# from listing 11.2.
def plot_layer(filename, symbol, layer_index=0, **kwargs):
    """Plots an OGR layer using the given symbol."""
    ds = ogr.Open(filename)
    for row in ds.GetLayer(layer_index):
        geom = row.geometry()
        geom_type = geom.GetGeometryType()

        # Polygons
        if geom_type == ogr.wkbPolygon:
            plot_polygon(geom, symbol, **kwargs)

        # Multipolygons
        elif geom_type == ogr.wkbMultiPolygon:
            for i in range(geom.GetGeometryCount()):
                subgeom = geom.GetGeometryRef(i)
                plot_polygon(subgeom, symbol, **kwargs)

        # Lines
        elif geom_type == ogr.wkbLineString:
            plot_line(geom, symbol, **kwargs)

        # Multilines
        elif geom_type == ogr.wkbMultiLineString:
            for i in range(geom.GetGeometryCount()):
                subgeom = geom.GetGeometryRef(i)
                plot_line(subgeom, symbol, **kwargs)

        # Points
        elif geom_type == ogr.wkbPoint:
            plot_point(geom, symbol, **kwargs)

        # Multipoints
        elif geom_type == ogr.wkbMultiPoint:
            for i in range(geom.GetGeometryCount()):
                subgeom = geom.GetGeometryRef(i)
                plot_point(subgeom, symbol, **kwargs)

# Now plot countries, rivers, and cities.
os.chdir(r'D:\osgeopy-data\global')

plot_layer('ne_110m_admin_0_countries.shp', 'k-')
# If you want to try filling polygons with the second plot_polygon
# function, you'll probably want to change the color for countries.
# plot_layer('ne_110m_admin_0_countries.shp', 'yellow')

plot_layer('ne_110m_rivers_lake_centerlines.shp', 'b-')
plot_layer('ne_110m_populated_places_simple.shp', 'ro', ms=3)
plt.axis('equal')
plt.gca().get_xaxis().set_ticks([])
plt.gca().get_yaxis().set_ticks([])
plt.show()
