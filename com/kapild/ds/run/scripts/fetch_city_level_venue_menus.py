from sklearn.feature_extraction.text import TfidfVectorizer
from ds.GeoJson.shapely_utils import get_contained_shape
from ds.backend.redis.Redis import RedisStoreImpl
from shapely.geometry import shape, Point
from ds.foursquare.cities.cities_bounding_box import sf_bb, chicago_bb, manhattan_bb, atlanta_bb, austin_bb
import foursquare
from ds.foursquare.data.foursquare_data import Foursquare
import time
import numpy as np
redis_dict = {
    "read": {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 0,
    },
    "write": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
    }
}

import json
fs = Foursquare(redis_dict)
redis = RedisStoreImpl(redis_dict)

    # params['category_id'] = "4bf58dd8d48988d10f941735"
    # params['loc'] = {"ll" : "37.7751,-122.41", "name": "SF"}


def dump_city_neighborhood_level_menu_data(city_shp_json, city_venue_menu_file, city_venue_menu_hood_output_file):
    city_shp = json.load(open(city_shp_json))
    city_venues_menu = json.load(open(city_venue_menu_file))

    f_write = open(city_venue_menu_hood_output_file, "w")
    for venue in city_venues_menu:
        lng = venue["location"]["lng"]
        lat = venue["location"]["lat"]
        point = Point(lng, lat)
        hood_shape = get_contained_shape(point, city_shp)
        if hood_shape is None:
            continue
        if 'menu' not in hood_shape:
            hood_shape['menu'] = []
        hood_shape['menu'].append(venue["menus_list"])
        print "Adding venue %s to neighborhood:%s" %(venue["name"], hood_shape["properties"]["NAME"])

    print "writing to file:" + city_venue_menu_hood_output_file

    f_write.write(json.dumps(city_shp, sort_keys=False, indent=4, separators=(',', ': ') ))
    f_write.close()

def get_city_level_menu_api(city_bb, city_menu_file_output, dump_attr=["name", "location", "menus_list", "categories"]):

    index = 0
    is_complete = False
    f_write = open(city_menu_file_output, mode='w')

    params = {'is_fresh': False}
    city_venues_menu = []
    while not is_complete:
        for venue in fs.get_city_level_venues(city_bb):
            venue_menu_list = []
            for venue_menu in fs.get_menu_for_venue(venue, params):
                venue_menu_list.append(venue_menu)
            if len(venue_menu_list) == 0:
                continue
            print "%s:Getting menu for:%s" % (index, venue["name"])
            index += 1
            venue["menus_list"] = venue_menu_list
            is_complete = True
            venue_dict = {}
            for key in dump_attr:
                if key in venue:
                    venue_dict[key] = venue[key]
            city_venues_menu.append(venue_dict)

    print "writing to file:" + city_menu_file_output

    f_write.write(json.dumps(city_venues_menu))
    # f_write.write(json.dumps(city_venues_menu, sort_keys=False, indent=4, separators=(',', ': ')))
    f_write.close()



def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies


data_directory = "/Users/kdalwani/code/workspace/datascience/data/"

def run_chicago():
    run_city(
        chicago_bb,
         "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/GeoJson/chicago_county.json"
    )

def run_manhattan():
    run_city(
        manhattan_bb,
        "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/GeoJson/manhattan_county.json"
    )

def run_sf():
    run_city(
        sf_bb,
         "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/GeoJson/sf_geojson.json"
    )

def run_austin():
    run_city(
        austin_bb,
         "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/GeoJson/austin.json"
    )

def run_atlanta():
    run_city(
        atlanta_bb,
         "/Users/kdalwani/code/workspace/datascience/com/kapild/ds/GeoJson/atlanta.json"
    )

def run_city(city_bb, city_geojson_file):
    file_ext = ".json"
    city_menu_file_output = data_directory + city_bb.name + "_menu" + file_ext

    # fetches and dumps menus for all the venues in a city from foursquare
    get_city_level_menu_api(city_bb, city_menu_file_output)

    city_venue_menu_hood_output_file = data_directory + city_bb.name + "_hood" + file_ext
    dump_city_neighborhood_level_menu_data(
         city_geojson_file,
         city_menu_file_output,
         city_venue_menu_hood_output_file
    )

if __name__ == "__main__":
    # run_atlanta()
    # run_austin()
    run_sf()

