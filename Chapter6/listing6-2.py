def poly_to_line_layer(ds, poly_name, line_name):
    """Creates a line layer from a polygon layer."""
    # Delete the line layer if it exists.
    if ds.GetLayer(line_name):
        ds.DeleteLayer(line_name)

    # Get the polygon layer and its spatial reference.
    poly_lyr = ds.GetLayer(poly_name)
    sr = poly_lyr.GetSpatialRef()

    # Create a line layer with the same SR as the polygons
    # and copy the field definitions from the polygons to
    # the line layer.
    line_lyr = ds.CreateLayer(line_name, sr, ogr.wkbLineString)
    line_lyr.CreateFields(poly_lyr.schema)

    # Create a feature to use over and over.
    line_feat = ogr.Feature(line_lyr.GetLayerDefn())

    # Loop through all of the polygons.
    for poly_feat in poly_lyr:

        # Copy the attribute values from the polygon to the
        # new feature.
        atts = poly_feat.items()
        for fld_name in atts.keys():
            line_feat.SetField(fld_name, atts[fld_name])

        # Loop through the rings in the polygon.
        poly_geom = poly_feat.geometry()
        for i in range(poly_geom.GetGeometryCount()):
            ring = poly_geom.GetGeometryRef(i)

            # Create a new line using the ring's vertices.
            line_geom = ogr.Geometry(ogr.wkbLineString)
            for coords in ring.GetPoints():
                line_geom.AddPoint(*coords)

            # Insert the new line feature.
            line_feat.SetGeometry(line_geom)
            line_lyr.CreateFeature(line_feat)
