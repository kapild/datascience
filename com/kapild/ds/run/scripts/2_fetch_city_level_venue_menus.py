from sklearn.feature_extraction.text import TfidfVectorizer
from ds.GeoJson.shapely_utils import get_contained_shape
from ds.backend.redis.Redis import RedisStoreImpl
from shapely.geometry import shape, Point
from ds.foursquare.cities.cities_bounding_box import sf_bb, chicago_bb, manhattan_bb, atlanta_bb, austin_bb
from ds.run.scripts import data_directory
from ds.utils.str_utils import remove_space_lower_case

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

total_venues = 0
total_menus_items = 0
venue_id_set = dict()
venue_id_set_with_menus = dict()
def dump_city_neighborhood_level_menu_data(input_city_shp_json, input_city_venue_menu_file,
                                           output_city_venue_menu_hood_file):
    city_shp = json.load(open(input_city_shp_json))
    city_venues_menu = json.load(open(input_city_venue_menu_file))
    venue_hood_count = dict()
    menu_count = dict()
    f_write = open(output_city_venue_menu_hood_file, "w")
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
        key = hood_shape["properties"]["NAME"]
        count = menu_count.get(key, 0)
        venue_count = venue_hood_count.get(key, 0)
        venue_hood_count[key] = venue_count + 1
        menu_count[key] = count + len(venue["menus_list"])

    print "Hood:" + str(venue_hood_count)
    print "Menus" + str(menu_count)
    print "writing to file:" + output_city_venue_menu_hood_file

    f_write.write(json.dumps(city_shp, sort_keys=False, indent=4, separators=(',', ': ') ))
    f_write.close()

def load_dump_city_level_menu_api(city_bb, city_menu_file_output, dump_attr=["name", "location", "menus_list", "categories"]):
    global total_venues
    global total_menus_items
    global venue_id_set
    index = 0
    is_complete = False
    f_write = open(city_menu_file_output, mode='w')

    params = {'is_fresh': False}
    city_venues_menu = []
    while not is_complete:
        for venue in fs.get_city_level_venues(city_bb):
            total_venues += 1
            if venue['id'] not in venue_id_set:
                venue_id_set[venue["id"]] = 1
                venue_menu_list = []
                for venue_menu in fs.get_menu_for_venue(venue, params):
                    venue_menu_list.append(venue_menu)
                total_menus_items += len(venue_menu_list)
                if len(venue_menu_list) == 0:
                    continue
                # print "%s:Got menu for:%s" % (index, venue["name"])
                # print "Total menus so far:" + str(total_menus_items)
                index += 1
                venue_id_set_with_menus[venue["id"]] = 1
                venue["menus_list"] = venue_menu_list
                is_complete = True
                venue_dict = {}
                for key in dump_attr:
                    if key in venue:
                        venue_dict[key] = venue[key]
                city_venues_menu.append(venue_dict)

    print "venue total: " + str(total_venues)
    print "unique venue total: " + str(len(venue_id_set))
    print "unique venue total with one menu: " + str(len(venue_id_set_with_menus))
    print "menus total: " + str(total_menus_items)
    print "writing to file:" + city_menu_file_output

    f_write.write(json.dumps(city_venues_menu))
    # f_write.write(json.dumps(city_venues_menu, sort_keys=False, indent=4, separators=(',', ': ')))
    f_write.close()



def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies


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

def run_city(city_bb, input_city_geojson_file):
    file_ext = ".json"
    city_menu_file_output = (remove_space_lower_case(data_directory + city_bb.name + "_menu" + file_ext))

    # 1. fetches and dumps menus for all the venues in a city from foursquare
    load_dump_city_level_menu_api(city_bb, (city_menu_file_output))

    # 2.
    city_venue_menu_hood_output_file = data_directory + city_bb.name + "_hood" + file_ext
    dump_city_neighborhood_level_menu_data(
         input_city_geojson_file,
         city_menu_file_output,
         remove_space_lower_case(city_venue_menu_hood_output_file)
    )

if __name__ == "__main__":
    # run_atlanta()
    run_austin()
    # run_sf()

