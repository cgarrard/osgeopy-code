# Script that uses meshgrid to get map coordinates and then plots
# the DEM in 3d.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from osgeo import gdal


ds = gdal.Open(r'D:\osgeopy-data\Washington\dem\sthelens_utm.tif')
band = ds.GetRasterBand(1)
ov_band = band.GetOverview(band.GetOverviewCount() - 3)
data = ov_band.ReadAsArray()

# Calculate bounding coordinates.
geotransform = ds.GetGeoTransform()
minx = geotransform[0]
maxy = geotransform[3]
maxx = minx + ov_band.XSize * geotransform[1]
miny = maxy + ov_band.YSize * geotransform[5]

# Get the x and y arrays.
x = np.arange(minx, maxx, geotransform[1])
y = np.arange(maxy, miny, geotransform[5])
x, y = np.meshgrid(x[:ov_band.XSize], y[:ov_band.YSize])

# Make the 3D plot.
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(x, y, data, cmap='gist_earth', lw=0)
plt.axis('equal')

# # Change the viewpoint and turn the ticks off.
# ax.view_init(elev=55, azim=60)
# plt.axis('off')

# # Create an animation.
# import matplotlib.animation as animation
# def animate(i):
#     ax.view_init(elev=65, azim=i)
# anim = animation.FuncAnimation(
#     fig, animate, frames=range(0, 360, 10), interval=100)
# plt.axis('off')

# # If you have FFmpeg and it's in your path, you can save the
# # animation.
# anim.save('d:/temp/helens.mp4', 'ffmpeg')

plt.show()
