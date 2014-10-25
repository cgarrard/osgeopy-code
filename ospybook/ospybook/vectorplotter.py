from osgeo import ogr

import ospybook as pb
from ospybook.simplevectorplotter import SimpleVectorPlotter

point_types = [ogr.wkbPoint, ogr.wkbPoint25D,
               ogr.wkbMultiPoint, ogr.wkbMultiPoint25D]
line_types = [ogr.wkbLineString, ogr.wkbLineString25D,
              ogr.wkbMultiLineString, ogr.wkbMultiLineString25D]
polygon_types = [ogr.wkbPolygon, ogr.wkbPolygon25D,
                 ogr.wkbMultiPolygon, ogr.wkbMultiPolygon25D]

class VectorPlotter(SimpleVectorPlotter):
    """Plots vector data represented as OGR layers and geometries."""

    def __init__(self, interactive, ticks=False, figsize=None, limits=None):
        """Construct a new VectorPlotter.

        interactive - boolean flag denoting interactive mode
        ticks       - boolean flag denoting whether to show axis tickmarks
        figsize     - optional figure size
        limits      - optional geographic limits (x_min, x_max, y_min, y_max)
        """
        super(VectorPlotter, self).__init__(interactive, ticks, figsize, limits)

    def plot(self, geom_or_lyr, symbol='', name='', **kwargs):
        """Plot a geometry or layer.
        geom_or_lyr - geometry, layer, or filename
        symbol      - optional pyplot symbol to draw the geometries with
        name        - optional name to assign to layer so can access it later
        kwargs      - optional pyplot drawing parameters
        """
        if type(geom_or_lyr) is str:
            lyr, ds = pb._get_layer(geom_or_lyr)
            self.plot_layer(lyr, symbol, name, **kwargs)
        elif type(geom_or_lyr) is ogr.Geometry:
            self.plot_geom(geom_or_lyr, symbol, name, **kwargs)
        elif type(geom_or_lyr) is ogr.Layer:
            self.plot_layer(geom_or_lyr, symbol, name, **kwargs)
        else:
            raise RuntimeError('{} is not supported.'.format(type(geom_or_lyr)))

    def plot_geom(self, geom, symbol='', name='', **kwargs):
        """Plot a geometry.
        geom   - geometry
        symbol - optional pyplot symbol to draw the geometry with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        geom_type = geom.GetGeometryType()
        if not symbol:
            if geom_type in point_types:
                symbol = self._point_symbol()
            elif geom_type in line_types:
                symbol = self._line_symbol()
        if geom_type in polygon_types and not self._kwargs_has_color(**kwargs):
            kwargs['fc'] = symbol or self._next_color()
        graphics = self._plot_geom(geom, symbol, **kwargs)
        self._set_graphics(graphics, name, symbol or kwargs)

    def plot_layer(self, lyr, symbol='', name='', **kwargs):
        """Plot a layer.
        geom   - layer
        symbol - optional pyplot symbol to draw the geometries with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        geom_type = lyr.GetLayerDefn().GetGeomType()
        if geom_type == ogr.wkbUnknown:
            feat = lyr.GetFeature(0)
            geom_type = feat.geometry().GetGeometryType()
        if not symbol:
            if geom_type in point_types:
                symbol = self._point_symbol()
            elif geom_type in line_types:
                symbol = self._line_symbol()
        if geom_type in polygon_types and not self._kwargs_has_color(**kwargs):
            kwargs['fc'] = symbol or self._next_color()
        lyr.ResetReading()
        graphics = []
        for feat in lyr:
            graphics += self._plot_geom(feat.geometry(), symbol, **kwargs)
        self._set_graphics(graphics, name, symbol or kwargs)
        lyr.ResetReading()

    def _plot_geom(self, geom, symbol='', **kwargs):
        """Plot a geometry."""
        geom_name = geom.GetGeometryName()
        if geom_name == 'POINT':
            symbol = symbol or self._point_symbol()
            return self._plot_point(self._get_point_coords(geom), symbol, **kwargs)
        elif geom_name == 'MULTIPOINT':
            symbol = symbol or self._point_symbol()
            return self._plot_multipoint(self._get_multipoint_coords(geom), symbol, **kwargs)
        elif geom_name == 'LINESTRING':
            return self._plot_line(self._get_line_coords(geom), symbol, **kwargs)
        elif geom_name == 'MULTILINESTRING':
            return self._plot_multiline(self._get_multiline_coords(geom), symbol, **kwargs)
        elif geom_name == 'POLYGON':
            return self._plot_polygon(self._get_polygon_coords(geom), **kwargs)
        elif geom_name == 'MULTIPOLYGON':
            return self._plot_multipolygon(self._get_multipolygon_coords(geom), **kwargs)
        elif geom_name == 'GEOMETRYCOLLECTION':
            graphics = []
            for i in range(geom.GetGeometryCount()):
                graphics += self._plot_geom(geom.GetGeometryRef(i), symbol, **kwargs)
            return graphics
        else:
            raise RuntimeError('{} not supported'.format(geom_name))

    def _get_line_coords(self, geom):
        """Get line coordinates as a list of (x, y) tuples."""
        return [coords[:2] for coords in geom.GetPoints()]

    def _get_point_coords(self, geom):
        """Get point coordinates as an (x, y) tuple."""
        return (geom.GetX(), geom.GetY())

    def _get_polygon_coords(self, geom):
        """Get polygon coordinates as a list of lists of (x, y) tuples."""
        coords = []
        for i in range(geom.GetGeometryCount()):
            coords.append(self._get_line_coords(geom.GetGeometryRef(i)))
        return coords

    def _get_multiline_coords(self, geom):
        """Get multiline coordinates as a list of lists of (x, y) tuples."""
        coords = []
        for i in range(geom.GetGeometryCount()):
            coords.append(self._get_line_coords(geom.GetGeometryRef(i)))
        return coords

    def _get_multipoint_coords(self, geom):
        """Get multipoint coordinates as a list of (x, y) tuples."""
        coords = []
        for i in range(geom.GetGeometryCount()):
            coords.append(self._get_point_coords(geom.GetGeometryRef(i)))
        return coords

    def _get_multipolygon_coords(self, geom):
        """Get multipolygon coordinates as a list of lists rings."""
        coords = []
        for i in range(geom.GetGeometryCount()):
            coords.append(self._get_polygon_coords(geom.GetGeometryRef(i)))
        return coords

    def _kwargs_has_color(self, **kwargs):
        """Check if kwargs dictionary has a facecolor entry."""
        return 'fc' in kwargs or 'facecolor' in kwargs
