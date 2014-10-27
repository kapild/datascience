
import json
from shapely.geometry import shape, Point


def get_contained_shape(point, shape_json):
    # check each polygon to see if it contains the point
    for feature in shape_json['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            # print 'Found containing polygon:', feature
            return feature
    return None

