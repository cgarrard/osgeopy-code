from osgeo import ogr

ds = ogr.Open(r'D:\osgeopy-data\Galapagos')
lyr = ds.GetLayerByName('albatross_ranges2')
lyr.SetAttributeFilter("tag_id = '1163-1163' and location = 'island'")
row = next(lyr)
all_areas = row.geometry().Clone()
common_areas = row.geometry().Clone()
for row in lyr:
    all_areas = all_areas.Union(row.geometry())
    common_areas = common_areas.Intersection(row.geometry())
percent = common_areas.GetArea() / all_areas.GetArea() * 100
print('Percent of all area used in every visit: {0}'. format(percent))
