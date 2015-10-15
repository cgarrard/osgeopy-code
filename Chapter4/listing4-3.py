# Script to make a webmap from WFS data. The first part of this is the same
# as listing 4.2, since you need it for the whole thing to work.

import os
import urllib
from osgeo import ogr
import folium


def get_bbox(geom):
    """Return the bbox based on a geometry envelope."""
    return '{0},{2},{1},{3}'.format(*geom.GetEnvelope())

def get_center(geom):
    """Return the center point of a geometry."""
    centroid = geom.Centroid()
    return [centroid.GetY(), centroid.GetX()]

def get_state_geom(state_name):
    """Return the geometry for a state."""
    ds = ogr.Open(r'D:\osgeopy-data\US\states.geojson')
    if ds is None:
        raise RuntimeError(
            'Could not open the states dataset. Is the path correct?')
    lyr = ds.GetLayer()
    lyr.SetAttributeFilter('state = "{0}"'.format(state_name))
    feat = next(lyr)
    return feat.geometry().Clone()

def save_state_gauges(out_fn, bbox=None):
    """Save stream gauge data to a geojson file."""
    url = 'http://gis.srh.noaa.gov/arcgis/services/ahps_gauges/' + \
          'MapServer/WFSServer'
    parms = {
        'version': '1.1.0',
        'typeNames': 'ahps_gauges:Observed_River_Stages',
        'srsName': 'urn:ogc:def:crs:EPSG:6.9:4326',
    }
    if bbox:
        parms['bbox'] = bbox
    try:
        request = 'WFS:{0}?{1}'.format(url, urllib.urlencode(parms))
    except:
        request = 'WFS:{0}?{1}'.format(url, urllib.parse.urlencode(parms))
    wfs_ds = ogr.Open(request)
    if wfs_ds is None:
        raise RuntimeError('Could not open WFS.')
    wfs_lyr = wfs_ds.GetLayer(0)

    driver = ogr.GetDriverByName('GeoJSON')
    if os.path.exists(out_fn):
        driver.DeleteDataSource(out_fn)
    json_ds = driver.CreateDataSource(out_fn)
    json_ds.CopyLayer(wfs_lyr, '')



########## This is the new code from listing 4.3.

colors = {
    'action': '#FFFF00',
    'low_threshold': '#734C00',
    'major': '#FF00C5',
    'minor': '#FFAA00',
    'moderate': '#FF0000',
    'no_flooding': '#55FF00',
    'not_defined': '#B2B2B2',
    'obs_not_current': '#B2B2B2',
    'out_of_service': '#4E4E4E'
}

def get_popup(attributes):
    """Return popup text for a feature."""
    template = '''{location}, {waterbody}</br>
                  {observed} {units}</br>
                  {status}'''
    return template.format(**attributes)

def add_markers(fmap, json_fn):
    ds = ogr.Open(json_fn)
    lyr = ds.GetLayer()
    for row in lyr:
        geom = row.geometry()
        color = colors[row.GetField('status')]
        fmap.circle_marker([geom.GetY(), geom.GetX()],
                           line_color=color,
                           fill_color=color,
                           radius=5000,
                           popup=get_popup(row.items()))

def make_map(state_name, json_fn, html_fn, **kwargs):
    """Make a folium map."""
    geom = get_state_geom(state_name)
    save_state_gauges(json_fn, get_bbox(geom))
    fmap = folium.Map(location=get_center(geom), **kwargs)
    add_markers(fmap, json_fn)
    fmap.create_map(path=html_fn)


# Top-level code. Don't forget to change the directory.
# Try other options for the tiles parameter. Options are:
# 'OpenStreetMap', 'Mapbox Bright', 'Mapbox Control Room',
# 'Stamen Terrain', 'Stamen Toner'
os.chdir(r'D:\Dropbox\Public\webmaps2')
make_map('Oklahoma', 'ok2.json', 'ok2.html',
         zoom_start=7, tiles='Stamen Toner')


# You can look at the capabilities output for this WFS here:
# http://gis.srh.noaa.gov/arcgis/services/ahps_gauges/MapServer/WFSServer?request=GetCapabilities

# And info for all services from this site here:
# http://gis.srh.noaa.gov/arcgis/rest/services
