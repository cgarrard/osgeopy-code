# Plot world landmasses as simple polygons.

import matplotlib.pyplot as plt
from osgeo import ogr

ds = ogr.Open(r'D:\osgeopy-data\global\ne_110m_land.shp')
lyr = ds.GetLayer(0)
for row in lyr:
    geom = row.geometry()
    ring = geom.GetGeometryRef(0)

    # This returns a list of (x,y) tuples.
    coords = ring.GetPoints()
    x, y = zip(*coords)

    # The 'k' means black. Try 'b' or 'r'.
    plt.plot(x, y, 'k')

# Equalize the axis units so things aren't warped. Comment out
# this line and see what happens.
plt.axis('equal')
plt.show()
