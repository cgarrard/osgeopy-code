# Script demonstrating how to use multiple rules in a mapnik style.

#####################  The first part is from listing 13.8.

import mapnik

# Create the map object.
srs = "+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs"
m = mapnik.Map(800, 600, srs)
m.zoom_to_box(mapnik.Box2d(-90.3, 29.7, -89.5, 30.3))

# Create a layer from a shapefile.
tiger_fn = r'D:\osgeopy-data\Louisiana\tiger_la_water_CENSUS_2006'
tiger_shp = mapnik.Shapefile(file=tiger_fn)
tiger_lyr = mapnik.Layer('Tiger')
tiger_lyr.datasource = tiger_shp

# Create a polygon fill symbol.
water_color = mapnik.Color(165, 191, 221)
water_fill_sym = mapnik.PolygonSymbolizer(water_color)

# Create a symbology style and add it to the layer.
tiger_rule = mapnik.Rule()
tiger_rule.symbols.append(water_fill_sym)
tiger_style = mapnik.Style()
tiger_style.rules.append(tiger_rule)
m.append_style('tiger', tiger_style)

# Add the style and layer to the map.
tiger_lyr.styles.append('tiger')

# Comment out this line to get the layers in the right order.
m.layers.append(tiger_lyr)


#####################  Here's the new stuff.

atlas_lyr = mapnik.Layer('National Atlas')
atlas_shp = mapnik.Shapefile(file=r'D:\osgeopy-data\US\wtrbdyp010')
atlas_lyr.datasource = atlas_shp

# Create a rule for open water.
water_rule = mapnik.Rule()
water_rule.filter = mapnik.Expression(
    "[Feature]='Canal' or [Feature]='Lake'")
water_rule.symbols.append(water_fill_sym)

# Create fill and outline symbolizers for marshes.
marsh_color = mapnik.Color('#66AA66')
marsh_fill_sym = mapnik.PolygonSymbolizer(marsh_color)
marsh_line_sym = mapnik.LineSymbolizer(marsh_color, 2)

# Create a rule for marshes using the marsh symbols.
marsh_rule = mapnik.Rule()
marsh_rule.filter = mapnik.Expression(
    "[Feature]='Swamp or Marsh'")
marsh_rule.symbols.append(marsh_fill_sym)
marsh_rule.symbols.append(marsh_line_sym)

# Create the atlas style and add the water and marsh rules.
atlas_style = mapnik.Style()
atlas_style.rules.append(water_rule)
atlas_style.rules.append(marsh_rule)

# Add the style and layer to the map.
m.append_style('atlas', atlas_style)
atlas_lyr.styles.append('atlas')

# Comment out this line to get the layers in the right order.
m.layers.append(atlas_lyr)

# # To get the layers in the right order, uncomment this. (See the
# # lines to comment out above).
# m.layers.append(atlas_lyr)
# m.layers.append(tiger_lyr)

# Save the map.
mapnik.render_to_file(m, r'd:\temp\nola2.png')
