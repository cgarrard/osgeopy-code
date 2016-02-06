# Script to make a webmap from WFS data. Import listing4-3 so you can reuse
# some of the functions in there.

import os
from osgeo import ogr
import folium
import listing4_3


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

# Because this version of make_map was defined after the version in
# listing4_3 (since it was already imported and evaluated), then this is
# the version that will be used. Unlike in the book text, the first two
# lines of the function here have been changed to reference get_state_geom,
# save_state_gauges, get_bbox, and get_center from the listing4_3 module.
def make_map(state_name, json_fn, html_fn, **kwargs):
    """Make a folium map."""
    geom = listing4_3.get_state_geom(state_name)
    listing4_3.save_state_gauges(json_fn, listing4_3.get_bbox(geom))
    fmap = folium.Map(location=listing4_3.get_center(geom), **kwargs)
    add_markers(fmap, json_fn)
    fmap.create_map(path=html_fn)


# Top-level code. Don't forget to change the directory.
# Try other options for the tiles parameter. Options are:
# 'OpenStreetMap', 'Mapbox Bright', 'Mapbox Control Room',
# 'Stamen Terrain', 'Stamen Toner'
os.chdir(r'D:\Dropbox\Public\webmaps')
make_map('Oklahoma', 'ok2.json', 'ok2.html',
         zoom_start=7, tiles='Stamen Toner')

