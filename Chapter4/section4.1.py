#########################  4.1 Intro to OGR  ###################################

# Get some drivers.
from osgeo import ogr

driver = ogr.GetDriverByName('geojson')
print(driver)

driver = ogr.GetDriverByName('shapefile')
print(driver)

import ospybook as pb
pb.print_drivers()
