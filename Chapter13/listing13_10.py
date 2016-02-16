# Script to add the roads and city outline to the mapnik map.

#####################  The first part is from listing 13.9.

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

# Create the atlas layer.
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


#####################  Here's the new stuff.

# Specify the road layer's SRS because it has a different one
# than the map.
roads_lyr = mapnik.Layer('Roads', "+init=epsg:4326")
road_shp = mapnik.Shapefile(file=r'D:\osgeopy-data\Louisiana\roads')
roads_lyr.datasource = road_shp

# Create the roads rules and style.
roads_color = mapnik.Color(170, 170, 127)

roads_primary_rule = mapnik.Rule()
roads_primary_rule.filter = mapnik.Expression("[fclass]='primary'")
roads_primary_sym = mapnik.LineSymbolizer(roads_color, 1.5)
roads_primary_rule.symbols.append(roads_primary_sym)

roads_secondary_rule = mapnik.Rule()
roads_secondary_rule.filter = mapnik.Expression(
    "[fclass]='secondary' or [fclass]='tertiary'")
roads_secondary_sym = mapnik.LineSymbolizer(roads_color, 0.5)
roads_secondary_rule.symbols.append(roads_secondary_sym)

roads_style = mapnik.Style()
roads_style.rules.append(roads_primary_rule)
roads_style.rules.append(roads_secondary_rule)

# Add the roads style to the map and roads layer.
m.append_style('roads style', roads_style)
roads_lyr.styles.append('roads style')

# Create the city layer.
city_lyr = mapnik.Layer('City Outline')
city_shp = mapnik.Shapefile(file=r'D:\osgeopy-data\Louisiana\NOLA')
city_lyr.datasource = city_shp

# Create a black dashed line.
city_color = mapnik.Color('black')
city_sym = mapnik.LineSymbolizer(city_color, 2)
city_sym.stroke.add_dash(4, 2)
city_rule = mapnik.Rule()
city_rule.symbols.append(city_sym)
city_style = mapnik.Style()
city_style.rules.append(city_rule)

m.append_style('city style', city_style)
city_lyr.styles.append('city style')

# Add all of the layers to the map.
m.layers.append(atlas_lyr)
m.layers.append(tiger_lyr)
m.layers.append(roads_lyr)
m.layers.append(city_lyr)

# Save the map.
mapnik.render_to_file(m, r'd:\temp\nola3.png')

# This saves an xml file describing the map. It's used in a later
# example in the book.
mapnik.save_map(m, r'd:\temp\nola_map.xml')
