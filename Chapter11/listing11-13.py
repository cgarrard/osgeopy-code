# Script to draw a topo map with mapnik.

import mapnik
srs = '+proj=utm +zone=10 +ellps=GRS80 +datum=NAD83 +units=m +no_defs'
m = mapnik.Map(1200, 1200, srs)
m.zoom_to_box(mapnik.Box2d(558800, 5112200, 566600, 5120500))

# Add a GDAL datasource.
topo_lyr = mapnik.Layer('Topo', srs)
topo_raster = mapnik.Gdal(
    file=r'D:\osgeopy-data\Washington\dem\st_helens.tif')
topo_lyr.datasource = topo_raster

# Use a raster symbolizer.
topo_sym = mapnik.RasterSymbolizer()
topo_rule = mapnik.Rule()
topo_rule.symbols.append(topo_sym)
topo_style = mapnik.Style()
topo_style.rules.append(topo_rule)

m.append_style('topo', topo_style)
topo_lyr.styles.append('topo')

m.layers.append(topo_lyr)
mapnik.render_to_file(m, r'd:\temp\helens.png')
