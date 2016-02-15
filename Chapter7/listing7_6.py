# Calculate distance between adjacent points.

from osgeo import ogr
import ch7funcs

# Open the layer and add a distance field.
ds = ogr.Open(r'D:\osgeopy-data\Galapagos', True)
lyr = ds.GetLayerByName('albatross_lambert')
lyr.CreateField(ogr.FieldDefn('distance', ogr.OFTReal))


# Get the unique tags. Notice this uses the ch7funcs module but the text
# assumes the function is in the same script.
tag_ids = ch7funcs.get_unique(ds, 'albatross_lambert', 'tag_id')

# Loop through the IDs.
for tag_id in tag_ids:
    print('Processing ' + tag_id)

    # Limit the GPS points to the ones with the current tag ID.
    lyr.SetAttributeFilter(
        "tag_id ='{}'".format(tag_id))

    # Get the point and timestamp for the first location.
    row = next(lyr)
    previous_pt = row.geometry().Clone()
    previous_time = row.GetField('timestamp')

    # Loop the rest of the locations for the current tag.
    for row in lyr:
        current_time = row.GetField('timestamp')
        if current_time < previous_time:
            raise Exception('Timestamps out of order')

        # Calculate the distance to the previous point and save it.
        current_pt = row.geometry().Clone()
        distance = current_pt.Distance(previous_pt)
        row.SetField('distance', distance)
        lyr.SetFeature(row)

        # Remember the current point so it can be used as the "previous"
        # one when processing the next location.
        previous_pt = current_pt
        previous_time = current_time
del ds
