# Script to draw a topo map with a hillshade underneath.

import mapnik
srs = '+proj=utm +zone=10 +ellps=GRS80 +datum=NAD83 +units=m +no_defs'
m = mapnik.Map(1200, 1200, srs)
m.zoom_to_box(mapnik.Box2d(558800, 5112200, 566600, 5120500))

hillshade_lyr = mapnik.Layer('Hillshade', srs)
hillshade_raster = mapnik.Gdal(
    file=r'D:\osgeopy-data\Washington\dem\sthelens_hillshade.tif')
hillshade_lyr.datasource = hillshade_raster

hillshade_rule = mapnik.Rule()
hillshade_rule.symbols.append(mapnik.RasterSymbolizer())
hillshade_style = mapnik.Style()
hillshade_style.rules.append(hillshade_rule)

m.append_style('hillshade', hillshade_style)
hillshade_lyr.styles.append('hillshade')

topo_lyr = mapnik.Layer('Topo', srs)
topo_raster = mapnik.Gdal(
    file=r'D:\osgeopy-data\Washington\dem\st_helens.tif')
topo_lyr.datasource = topo_raster

topo_sym = mapnik.RasterSymbolizer()
topo_sym.opacity = 0.6                                                   #A
topo_rule = mapnik.Rule()
topo_rule.symbols.append(topo_sym)
topo_style = mapnik.Style()
topo_style.rules.append(topo_rule)

m.append_style('topo', topo_style)
topo_lyr.styles.append('topo')

m.layers.append(hillshade_lyr)                                           #B
m.layers.append(topo_lyr)                                                #B
mapnik.render_to_file(m, r'd:\temp\helens2.png')
