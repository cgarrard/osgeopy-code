import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np

try:
    numeric_types = (int, float, long)
except NameError:
    numeric_types = (int, float)

class SimpleVectorPlotter(object):
    """Plots vector data represented as lists of coordinates."""

    _graphics = {}

    def __init__(self, interactive, ticks=False, figsize=None, limits=None):
        """Construct a new SimpleVectorPlotter.

        interactive - boolean flag denoting interactive mode
        ticks       - boolean flag denoting whether to show axis tickmarks
        figsize     - optional figure size
        limits      - optional geographic limits (x_min, x_max, y_min, y_max)
        """
        if figsize:
            plt.figure(num=1, figsize=figsize)
        self.interactive = interactive
        if interactive:
            plt.ion()
        else:
            plt.ioff()
        if limits is not None:
            self.set_limits(*limits)
        if not ticks:
            self.no_ticks()
        plt.axis('equal')

    def adjust_markers(self):
        figsize = plt.gcf().get_size_inches()
        r = min(figsize[0] / 8, figsize[1] / 6)
        mpl.rcParams['lines.markersize'] = 6 * r
        mpl.rcParams['lines.markeredgewidth'] = 0.5 * r
        mpl.rcParams['lines.linewidth'] = r
        mpl.rcParams['patch.linewidth'] = r

    def axis_on(self, on):
        """Turn the axes and labels on or off."""
        if on:
            plt.axis('on')
        else:
            plt.axis('off')

    def clear(self):
        """Clear the plot area."""
        plt.cla()
        self._graphics = {}

    def close(self):
        """Close the plot."""
        self.clear()
        plt.close()

    def draw(self):
        """Draw a non-interactive plot."""
        plt.show()

    def hide(self, name):
        """Hide the layer with the given name."""
        try:
            graphics = self._graphics[name]
            graphic_type = type(graphics[0])
            if graphic_type is mpl.lines.Line2D:
                for graphic in graphics:
                    plt.axes().lines.remove(graphic)
            elif graphic_type is mpl.patches.Polygon or graphic_type is mpl.patches.PathPatch:
                for graphic in graphics:
                    plt.axes().patches.remove(graphic)
            else:
                raise RuntimeError('{} not supported'.format(graphic_type))
        except (KeyError, ValueError):
            pass

    def plot_line(self, data, symbol='', name='', **kwargs):
        """Plot a line.

        data   - list of (x, y) tuples
        symbol - optional pyplot symbol to draw the line with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        graphics = self._plot_line(data, symbol, **kwargs)
        self._set_graphics(graphics, name, symbol or kwargs)

    def plot_multiline(self, data, symbol='', name='', **kwargs):
        """Plot a multiline.

        data   - list of lines, each of which is a list of (x, y) tuples
        symbol - optional pyplot symbol to draw the lines with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        has_symbol = symbol or kwargs
        symbol = symbol or self._line_symbol()
        graphics = self._plot_multiline(data, symbol, **kwargs)
        self._set_graphics(graphics, name, has_symbol)

    def plot_multipoint(self, data, symbol='', name='', **kwargs):
        """Plot a multipoint.

        data   - list of (x, y) tuples
        symbol - optional pyplot symbol to draw the points with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        has_symbol = symbol or kwargs
        symbol = symbol or self._point_symbol()
        graphics = self._plot_multipoint(data, **kwargs)
        self._set_graphics(graphics, name, has_symbol)

    def plot_multipolygon(self, data, color='', name='', **kwargs):
        """Plot a multipolygon.

        data   - list of polygons, each of which is a list of rings, each of
                 which is a list of (x, y) tuples
        color  - optional pyplot color to draw the polygons with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        has_symbol = bool(color or kwargs)
        if not ('facecolor' in kwargs or 'fc' in kwargs):
            kwargs['fc'] = color or self._next_color()
        graphics = self._plot_multipolygon(data, **kwargs)
        self._set_graphics(graphics, name, has_symbol)

    def plot_point(self, data, symbol='', name='', **kwargs):
        """Plot a point.

        data   - (x, y) tuple
        symbol - optional pyplot symbol to draw the point with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        has_symbol = symbol or kwargs
        symbol = symbol or self._point_symbol()
        graphics = self._plot_point(data, symbol, **kwargs)
        self._set_graphics(graphics, name, has_symbol)

    def plot_polygon(self, data, color='', name='', **kwargs):
        """Plot a polygon.

        data   - list of rings, each of which is a list of (x, y) tuples
        color  - optional pyplot color to draw the polygon with
        name   - optional name to assign to layer so can access it later
        kwargs - optional pyplot drawing parameters
        """
        has_symbol = bool(color or kwargs)
        if not ('facecolor' in kwargs or 'fc' in kwargs):
            kwargs['fc'] = color or self._next_color()
        graphics = self._plot_polygon(data, **kwargs)
        self._set_graphics(graphics, name, has_symbol)

    def save(self, fn, dpi=300):
        plt.savefig(fn, dpi=dpi, bbox_inches='tight', pad_inches=0.02)

    def set_limits(self, x_min, x_max, y_min, y_max):
        """Set geographic limits for plotting."""
        self.x_lim = x_min, x_max
        self.y_lim = y_min, y_max
        self._set_limits()

    def show(self, name):
        """Show the layer with the given name."""
        try:
            graphics = self._graphics[name]
            graphic_type = type(graphics[0])
            if graphic_type is mpl.lines.Line2D:
                for graphic in graphics:
                    plt.axes().add_line(graphic)
            elif graphic_type is mpl.patches.Polygon or graphic_type is mpl.patches.PathPatch:
                for graphic in graphics:
                    plt.axes().add_patch(graphic)
            else:
                raise RuntimeError('{} not supported'.format(graphic_type))
        except KeyError:
            pass

    def no_ticks(self):
        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])

    def _clockwise(self, data):
        """Determine if points are in clockwise order."""
        total = 0
        x1, y1 = data[0]
        for x, y in data[1:]:
            total += (x - x1) * (y + y1)
            x1, y1 = x, y
        x, y = data[0]
        total += (x - x1) * (y + y1)
        return total > 0

    def _codes(self, data):
        """Get a list of codes for creating a new PathPatch."""
        codes = np.ones(len(data), dtype=np.int) * Path.LINETO
        codes[0] = Path.MOVETO
        return codes

    def _line_symbol(self):
        """Get a default line symbol."""
        return self._next_color() + '-'

    def _next_color(self):
        """Get the next color in the rotation."""
        return next(plt.gca()._get_lines.color_cycle)

    def _order_vertices(self, data, clockwise=True):
        """Order vertices in clockwise or counter-clockwise order."""
        self._clockwise(data) != clockwise or data.reverse()
        if data[0] != data[-1]:
            data.append(data[0])
        return data

    def _plot_line(self, data, symbol, **kwargs):
        """Plot a line."""
        try:
            x, y = zip(*data)
        except:
            x, y, z = zip(*data)
        return plt.plot(x, y, symbol, **kwargs)

    def _plot_multiline(self, data, symbol, **kwargs):
        """Plot a multiline."""
        graphics = []
        for line in data:
            graphics += self._plot_line(line, symbol, **kwargs)
        return graphics

    def _plot_multipoint(self, data, symbol, **kwargs):
        """Plot a multipoint."""
        graphics = []
        for point in data:
            graphics += self._plot_point(point, symbol, **kwargs)
        return graphics

    def _plot_multipolygon(self, data, **kwargs):
        """Plot a multipolygon."""
        graphics = []
        for poly in data:
            graphics += self._plot_polygon(poly, **kwargs)
        return graphics

    def _plot_point(self, data, symbol, **kwargs):
        """Plot a point."""
        return plt.plot(data[0], data[1], symbol, **kwargs)

    def _plot_polygon(self, data, **kwargs):
        """Plot a polygon."""
        outer = self._order_vertices(data[0], True)
        inner = [self._order_vertices(d, False) for d in data[1:]]
        vertices = np.concatenate(
            [np.asarray(outer)] + [np.asarray(i) for i in inner])
        codes = np.concatenate(
            [self._codes(outer)] + [self._codes(i) for i in inner])
        patch = PathPatch(Path(vertices, codes), **kwargs)
        plt.axes().add_patch(patch)
        return [patch]

    def _point_symbol(self):
        """Get a default point symbol."""
        return self._next_color() + 'o'

    def _same_type(self, graphic1, graphic2):
        """Determine if two graphics are of the same type."""
        if type(graphic1) is not type(graphic2):
            return False
        if type(graphic1) is mpl.patches.Polygon: ## huh?
            return True
        if len(graphic1.get_xdata()) == len(graphic2.get_xdata()):
            return True
        return len(graphic1.get_xdata()) > 1 and len(graphic2.get_xdata()) > 1

    def _set_graphics(self, graphics, name, has_symbol):
        """Add graphics to plot."""
        name = name or len(self._graphics)
        if name in self._graphics:
            self.hide(name)
            if not has_symbol and self._same_type(graphics[0], self._graphics[name][0]):
                styled_graphic = self._graphics[name][0]
                for graphic in graphics:
                    graphic.update_from(styled_graphic)
        self._graphics[name] = graphics
        plt.axis('equal')

    def _set_limits(self):
        """Set axis limits."""
        plt.xlim(*self.x_lim)
        plt.ylim(*self.y_lim)
        plt.axes().set_aspect('equal')
