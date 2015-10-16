# Script to draw world countries as patches.

import numpy as np
import matplotlib.pyplot as  plt
from matplotlib.path import Path
import matplotlib.patches as patches
from osgeo import ogr

def order_coords(coords, clockwise):
    """Orders coordinates."""
    total = 0
    x1, y1 = coords[0]
    for x, y in coords[1:]:
        total += (x - x1) * (y + y1)
        x1, y1 = x, y
    x, y = coords[0]
    total += (x - x1) * (y + y1)
    is_clockwise = total > 0
    if clockwise != is_clockwise:
        coords.reverse()
    return coords

def make_codes(n):
    """Makes a list of path codes."""
    codes = [Path.LINETO] * n
    codes[0] = Path.MOVETO
    return codes

def plot_polygon_patch(poly, color):
    """Plots a polygon as a patch."""
    # Outer clockwise path.
    coords = poly.GetGeometryRef(0).GetPoints()
    coords = order_coords(coords, True)
    codes = make_codes(len(coords))
    for i in range(1, poly.GetGeometryCount()):

        # Inner counter-clockwise paths.
        coords2 = poly.GetGeometryRef(i).GetPoints()
        coords2 = order_coords(coords2, False)
        codes2 = make_codes(len(coords2))

        # Concatenate the paths.
        coords = np.concatenate((coords, coords2))
        codes = np.concatenate((codes, codes2))

    # Add the patch to the plot
    path = Path(coords, codes)
    patch = patches.PathPatch(path, facecolor=color)
    plt.axes().add_patch(patch)

# Loop through all of the features in the countries layer and create
# patches for the polygons.
ds = ogr.Open(r'D:\osgeopy-data\global\ne_110m_admin_0_countries.shp')
lyr = ds.GetLayer(0)
for row in lyr:
    geom = row.geometry()
    if geom.GetGeometryType() == ogr.wkbPolygon:
        plot_polygon_patch(geom, 'yellow')
    elif geom.GetGeometryType() == ogr.wkbMultiPolygon:
        for i in range(geom.GetGeometryCount()):
            plot_polygon_patch(geom.GetGeometryRef(i), 'yellow')
plt.axis('equal')
plt.show()
