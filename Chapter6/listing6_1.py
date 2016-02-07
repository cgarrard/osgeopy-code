def line_to_point_layer(ds, line_name, pt_name):
    """Creates a point layer from vertices in a line layer."""
    # Delete the point layer if it exists.
    if ds.GetLayer(pt_name):
        ds.DeleteLayer(pt_name)

    # Get the line layer and its spatial reference.
    line_lyr = ds.GetLayer(line_name)
    sr = line_lyr.GetSpatialRef()

    # Create a point layer with the same SR as the lines
    # and copy the field definitions from the line to
    # the point layer.
    pt_lyr = ds.CreateLayer(pt_name, sr, ogr.wkbPoint)
    pt_lyr.CreateFields(line_lyr.schema)

    # Create a feature and geometry to use over and over.
    pt_feat = ogr.Feature(pt_lyr.GetLayerDefn())
    pt_geom = ogr.Geometry(ogr.wkbPoint)

    # Loop through all of the lines.
    for line_feat in line_lyr:

        # Copy the attribute values from the line to the
        # new feature.
        atts = line_feat.items()
        for fld_name in atts.keys():
            pt_feat.SetField(fld_name, atts[fld_name])

        # Loop through the line's vertices and for each one,
        # set the coordinates on the point geometry, add
        # it to the feature, and use the feature to create
        # a new feature in the point layer.
        for coords in line_feat.geometry().GetPoints():
            pt_geom.AddPoint(*coords)
            pt_feat.SetGeometry(pt_geom)
            pt_lyr.CreateFeature(pt_feat)
