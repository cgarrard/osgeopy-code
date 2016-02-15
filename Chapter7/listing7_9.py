from osgeo import ogr
import ch7funcs

ds = ogr.Open(r'D:\osgeopy-data\Galapagos', True)
pt_lyr = ds.GetLayerByName('albatross_lambert')
poly_lyr = ds.CreateLayer(
    'albatross_ranges2', pt_lyr.GetSpatialRef(), ogr.wkbPolygon)
id_field = ogr.FieldDefn('tag_id', ogr.OFTString)
area_field = ogr.FieldDefn('area', ogr.OFTReal)                          #A
area_field.SetWidth(30)                                                  #A
area_field.SetPrecision(4)
location_field = ogr.FieldDefn('location', ogr.OFTString)                                              #A
poly_lyr.CreateFields([id_field, area_field, location_field])
poly_row = ogr.Feature(poly_lyr.GetLayerDefn())



land_lyr = ds.GetLayerByName('land_lambert')                             #A
land_row = next(land_lyr)                                                #A
land_poly = land_row.geometry().Buffer(100000)                           #A



for tag_id in ch7funcs.get_unique(ds, 'albatross_lambert', 'tag_id'):
    print('Processing ' + tag_id)
    pt_lyr.SetAttributeFilter("tag_id = '{}'".format(tag_id))
    pt_locations = ogr.Geometry(ogr.wkbMultiPoint)
    last_location = None
    for pt_row in pt_lyr:
        pt = pt_row.geometry().Clone()
        if not land_poly.Contains(pt):                                   #B
            continue                                                     #B
        if pt.GetX() < -2800000:                                         #C
            location = 'island'                                          #C
        else:                                                            #C
            location = 'mainland'                                        #C
        if location != last_location:                                    #D
            if pt_locations.GetGeometryCount() > 2:
                homerange = pt_locations.ConvexHull()
                poly_row.SetGeometry(homerange)
                poly_row.SetField('tag_id', tag_id)
                poly_row.SetField('area', homerange.GetArea())
                poly_row.SetField('location', last_location)
                poly_lyr.CreateFeature(poly_row)
            pt_locations = ogr.Geometry(ogr.wkbMultiPoint)
            last_location = location
        pt_locations.AddGeometry(pt)
    if pt_locations.GetGeometryCount() > 2:                              #E
        homerange = pt_locations.ConvexHull()
        poly_row.SetGeometry(homerange)
        poly_row.SetField('tag_id', tag_id)
        poly_row.SetField('area', homerange.GetArea())
        poly_row.SetField('location', last_location)
        poly_lyr.CreateFeature(poly_row)
