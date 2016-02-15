from osgeo import ogr
import ch7funcs

ds = ogr.Open(r'D:\osgeopy-data\Galapagos', True)
pt_lyr = ds.GetLayerByName('albatross_lambert')
poly_lyr = ds.CreateLayer(
    'albatross_ranges', pt_lyr.GetSpatialRef(), ogr.wkbPolygon)
id_field = ogr.FieldDefn('tag_id', ogr.OFTString)
area_field = ogr.FieldDefn('area', ogr.OFTReal)                          #A
area_field.SetWidth(30)                                                  #A
area_field.SetPrecision(4)                                               #A
poly_lyr.CreateFields([id_field, area_field])
poly_row = ogr.Feature(poly_lyr.GetLayerDefn())

for tag_id in ch7funcs.get_unique(ds, 'albatross_lambert', 'tag_id'):
    print('Processing ' + tag_id)
    pt_lyr.SetAttributeFilter("tag_id = '{}'".format(tag_id))
    locations = ogr.Geometry(ogr.wkbMultiPoint)                          #B
    for pt_row in pt_lyr:                                                #B
        locations.AddGeometry(pt_row.geometry().Clone())                 #B

    homerange = locations.ConvexHull()                                   #C
    poly_row.SetGeometry(homerange)
    poly_row.SetField('tag_id', tag_id)
    poly_row.SetField('area', homerange.GetArea())
    poly_lyr.CreateFeature(poly_row)

del ds
