# Script to create an xml file to describe the National Atlas
# hydrography layer.

import mapnik

m = mapnik.Map(0, 0)

water_rule = mapnik.Rule()
water_rule.filter = mapnik.Expression(
    "[Feature]='Canal' or [Feature]='Lake'")
water_rule.symbols.append(
    mapnik.PolygonSymbolizer(mapnik.Color(165, 191, 221)))

marsh_rule = mapnik.Rule()
marsh_rule.filter = mapnik.Expression("[Feature]='Swamp or Marsh'")
marsh_color = mapnik.Color('#66AA66')
marsh_rule.symbols.append(mapnik.PolygonSymbolizer(marsh_color))
marsh_rule.symbols.append(mapnik.LineSymbolizer(marsh_color, 2))

atlas_style = mapnik.Style()
atlas_style.rules.append(water_rule)
atlas_style.rules.append(marsh_rule)
m.append_style('atlas', atlas_style)

lyr = mapnik.Layer('National Atlas Hydro',
                   "+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs")
lyr.datasource = mapnik.Shapefile(file=r'D:\osgeopy-data\US\wtrbdyp010')
lyr.styles.append('atlas')
m.layers.append(lyr)

mapnik.save_map(m, r'D:\osgeopy-data\US\national_atlas_hydro.xml')
