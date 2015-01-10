from ds.backend.redis.Redis import RedisStoreImpl
from ds.foursquare.cities.cities import get_top_cities_ll
from ds.foursquare.cities.cities_bounding_box import get_top_cities_bb, sf_bb, \
    chicago_bb, manhattan_bb, austin_bb, atlanta_bb
from ds.foursquare.cities.geo_utils import get_bb_grid

import foursquare
import time
from ds.foursquare.data.foursquare_data import Foursquare
import time
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

# Does a bounding box search for a given location and list of al categories.
def get_bb_box_venue_search(location, category_list):

    cat_length = len(category_list)
    index = 0
    is_complete = False
    is_time_out_error = False

    print "running for:" + location.name + " bounding box:" + str(location.nw) + ", " + str(location.se)
    while is_complete == False:
        for category in category_list:
            index += 1
            print location.name + ", " + (category["name"])
            params = dict()
            params['is_fresh'] = False
            params['categoryId'] = category['id']
            params['name'] = location.name
            city_bb = location
            for location_bb_tuple in get_bb_grid(city_bb.nw, city_bb.se, num=4):
                params['num'] = location_bb_tuple[0]
                params['ne'] = location_bb_tuple[1]
                params['sw'] = location_bb_tuple[2]
                try:
                    for venue in fs.get_venues_search(params):
                        continue
                    # print location["name"] + "," + category["name"] + "," + venue['name']
                except foursquare.RateLimitExceeded:
                    is_time_out_error = True
                    print "Sleeping due to rate"
                    print "done:" + str(index) + ", total:" + str(cat_length)
                    time.sleep(60 * 10)
        if is_time_out_error == False:
            is_complete = True


def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies



def run_san_francisco():
    run_city(sf_bb)

def run_chicago():
    run_city(chicago_bb)

def run_manhattan():
    run_city(manhattan_bb)

def run_austin():
    run_city(austin_bb)

def run_atlanta():
    run_city(atlanta_bb)

def run_city(city_bb):
    name = "Food"
    cat = None
    for category in get_fsq_categories():
        if category['name'] == name:
            cat = category
    list_a = []
    fs.get_child_category_first(cat, list_a)
    category_list = list_a
    get_bb_box_venue_search(city_bb, category_list)

if __name__ == "__main__":
# gets the data from foursquare for a given a bounding box of a city and list of all categories.
    run_austin()
    run_atlanta()
