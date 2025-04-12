from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

def to_geojson_from_wkb(wkb_element):
    """
    Converts WKB geometry to GeoJSON format using Shapely.
    """
    shape_obj = to_shape(wkb_element)
    return mapping(shape_obj)

