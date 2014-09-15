import os

from osgeo import ogr

def copy_datasource(source_fn, target_fn):
    """Copy an ogr data source."""
    ds = ogr.Open(source_fn, 0)
    if ds is None:
        raise OSError('Could not open {0} for copying.'.format(source_fn))
    if os.path.exists(target_fn):
        ds.GetDriver().DeleteDataSource(target_fn)
    ds.GetDriver().CopyDataSource(ds, target_fn)

def get_shp_geom(fn):
    """Convenience function to get the first geometry from a shapefile."""
    lyr, ds = _get_layer(fn)
    feat = lyr.GetNextFeature()
    return feat.geometry().Clone()

def has_spatialite():
    """Determine if the current GDAL is built with SpatiaLite support."""
    use_exceptions = ogr.GetUseExceptions()
    ogr.UseExceptions()
    try:
        ds = ogr.GetDriverByName('Memory').CreateDataSource('memory')
        sql = '''SELECT sqlite_version(), spatialite_version()'''
        lyr = ds.ExecuteSQL(sql, dialect='SQLite')
        return True
    except Exception as e:
        return False
    finally:
        if not use_exceptions:
            ogr.DontUseExceptions()

def print_attributes(lyr_or_fn, n=None, fields=None, geom=True, reset=True):
    """Print attribute values in a layer.

    lyr_or_fn - OGR layer object or filename to datasource (will use 1st layer)
    n         - optional number of features to print; default is all
    fields    - optional list of case-sensitive field names to print; default
                is all
    geom      - optional boolean flag denoting whether geometry type is printed;
                default is True
    reset     - optional boolean flag denoting whether the layer should be reset
              - to the first record before printing; default is True
    """
    lyr, ds = _get_layer(lyr_or_fn)
    if reset:
        lyr.ResetReading()

    n = n or lyr.GetFeatureCount()
    geom = geom and lyr.GetGeomType() != ogr.wkbNone
    fields = fields or [field.name for field in lyr.schema]
    data = [['FID'] + fields]
    if geom:
        data[0].insert(1, 'Geometry')
    feat = lyr.GetNextFeature()
    while feat and len(data) <= n:
        data.append(_get_atts(feat, fields, geom))
        feat = lyr.GetNextFeature()
    lens = map(lambda i: max(map(lambda j: len(str(j)), i)), zip(*data))
    format_str = ''.join(map(lambda x: '{{:<{}}}'.format(x + 4), lens))
    for row in data:
        try:
            print(format_str.format(*row))
        except UnicodeEncodeError:
            e = sys.stdout.encoding
            print(codecs.decode(format_str.format(*row).encode(e, 'replace'), e))
    print('{0} of {1} features'.format(min(n, lyr.GetFeatureCount()), lyr.GetFeatureCount()))
    if reset:
        lyr.ResetReading()

def print_capabilities(item):
    """Print capabilities for a driver, datasource, or layer."""
    if isinstance(item, ogr.Driver):
        _print_capabilites(item, 'Driver', 'ODrC')
    elif isinstance(item, ogr.DataSource):
        _print_capabilites(item, 'DataSource', 'ODsC')
    elif isinstance(item, ogr.Layer):
        _print_capabilites(item, 'Layer', 'OLC')
    else:
        print('Unsupported item')

def print_drivers():
    """Print a list of available drivers."""
    for i in range(ogr.GetDriverCount()):
        driver = ogr.GetDriver(i)
        writeable = driver.TestCapability(ogr.ODrCCreateDataSource)
        print('{0} ({1})'.format(driver.GetName(),
                                 'read/write' if writeable else 'readonly'))

def print_layers(fn):
    """Print a list of layers in a data source.

    fn - path to data source
    """
    ds = ogr.Open(fn, 0)
    if ds is None:
        raise OSError('Could not open {}'.format(fn))
    for i in range(ds.GetLayerCount()):
        lyr = ds.GetLayer(i)
        print('{0}: {1} ({2})'.format(i, lyr.GetName(),
                                      _geom_constants[lyr.GetGeomType()]))

def _geom_str(geom):
    """Get a geometry string for printing attributes."""
    if geom.GetGeometryType() == ogr.wkbPoint:
        return 'POINT ({:.3f}, {:.3f})'.format(geom.GetX(), geom.GetY())
    else:
        return geom.GetGeometryName()

def _get_atts(feature, fields, geom):
    """Get attribute values from a feature."""
    data = [feature.GetFID()]
    geometry = feature.geometry()
    if geom and geometry:
        data.append(_geom_str(geometry))
    values = feature.items()
    data += [values[field] for field in fields]
    return data

def _get_layer(lyr_or_fn):
    """Get the datasource and layer from a filename."""
    if type(lyr_or_fn) is str:
        ds = ogr.Open(lyr_or_fn)
        if ds is None:
            raise OSError('Could not open {0}.'.format(lyr_or_fn))
        return ds.GetLayer(), ds
    else:
        return lyr_or_fn, None

def _print_capabilites(item, name, prefix):
    """Print capabilities for a driver, datasource, or layer.

    item   - item to test
    name   - name of the type of item
    prefix - prefix of the ogr constants to use for testing
    """
    print('*** {0} Capabilities ***'.format(name))
    for c in filter(lambda x: x.startswith(prefix), dir(ogr)):
        print('{0}: {1}'.format(c, item.TestCapability(ogr.__dict__[c])))

_geom_constants = {}
_ignore = ['wkb25DBit', 'wkb25Bit', 'wkbXDR', 'wkbNDR']
for c in filter(lambda x: x.startswith('wkb'), dir(ogr)):
    if c not in _ignore:
        _geom_constants[ogr.__dict__[c]] = c[3:]
