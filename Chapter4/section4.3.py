import os

# Set this variable to your osgeopy-data directory so that the following
# examples will work without editing. We'll use the os.path.join() function
# to combine this directory and the filenames to make a complete path. Of
# course, you can type the full path to the file for each example if you'd
# prefer.
# data_dir = r'D:\osgeopy-data'
data_dir =


#########################  4.3 Viewing your data  ##############################

# Set a filename to use for the next several examples.
fn = os.path.join(data_dir, 'Washington', 'large_cities.geojson')

# Print name and population attributes.
import ospybook as pb
pb.print_attributes(fn, fields=['NAME', 'POPULATION'])

# Import VectorPlotter
from ospybook.vectorplotter import VectorPlotter

# Plot large_cities on top of counties from an interactive session.
vp = VectorPlotter(True)
vp.plot(os.path.join(data_dir, 'Washington', 'counties.shp'), fill=False)
vp.plot(os.path.join(data_dir, 'Washington', 'large_cities.geojson'), 'bo', ms=8)

# Plot big_cities on top of counties non-interactively.
vp = VectorPlotter(False)
vp.plot(os.path.join(data_dir, 'Washington', 'counties.shp'), fill=False)
vp.plot(os.path.join(data_dir, 'Washington', 'large_cities.geojson'), 'bo', ms=8)
vp.draw()
