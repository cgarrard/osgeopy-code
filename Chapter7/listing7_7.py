# Use GPS locations and elapsed time to get maximum speeds.

from datetime import datetime
from osgeo import ogr
import ch7funcs

date_format = '%Y-%m-%d %H:%M:%S.%f'
ds = ogr.Open(r'D:\osgeopy-data\Galapagos')
lyr = ds.GetLayerByName('albatross_lambert')

# Loop through each tag, initialize max_speed to 0, and limit the GPS
# locations to that tag.
for tag_id in ch7funcs.get_unique(ds, 'albatross_lambert', 'tag_id'):
    max_speed = 0
    lyr.SetAttributeFilter("tag_id ='{}'".format(tag_id))

    # Get the timestamp for the first point and convert it to a datetime.
    row = next(lyr)
    ts = row.GetField('timestamp')
    previous_time = datetime.strptime(ts, date_format)

    # Loop through the rest of the locations for the current tag.
    for row in lyr:

        # Get the current timestamp, convert to a datetime, and calculate
        # the amount of time since the previous location.
        ts = row.GetField('timestamp')
        current_time = datetime.strptime(ts, date_format)
        elapsed_time = current_time - previous_time
        hours = elapsed_time.total_seconds() / 3600

        # Use the distance you calculated in listing 7.6 to calculate speed.
        distance = row.GetField('distance')
        speed = distance / hours

        # Keep this speed if it's the largest seen so far.
        max_speed = max(max_speed, speed)

    # When done looping through the locations for this tag, print out the
    # max speed.
    print 'Max speed for {0}: {1}'.format(tag_id, max_speed)
