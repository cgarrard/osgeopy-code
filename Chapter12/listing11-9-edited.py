# Script demonstrating how to xml in a mapnik map.

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

# All of the code for the atlas layer is now gone...

# Add the atlas layer using the xml.
mapnik.load_map(m, r'D:\osgeopy-data\US\national_atlas_hydro.xml')
m.layers.append(tiger_lyr)

# Save the map.
mapnik.render_to_file(m, r'd:\temp\nola5.png')
