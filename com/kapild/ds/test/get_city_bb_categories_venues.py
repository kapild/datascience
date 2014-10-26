from ds.backend.redis.Redis import RedisStoreImpl
from ds.foursquare.cities.cities import get_top_cities_ll
from ds.foursquare.cities.cities_bounding_box import get_top_cities_bb
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

def get_save_cities_with_bb(name="Food"):

    cat = None
    for category in get_fsq_categories():
        if category['name'] == name:
            cat = category

    list_a = []
    fs.get_child_category_first(cat, list_a)
    location_list = get_top_cities_bb()[0:1]
    category_list = list_a
    cat_length = len(category_list)

    index = 0
    is_complete = False
    while(not is_complete):
        for location in location_list:
            for category in category_list:
                index = index + 1
                print location.name + ", " + (category["name"])
                params = {}
                params['is_fresh']  = False
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
                        print "Sleeping due to rate"
                        print "done:" + str(index) + ", total:" + str(cat_length)
                        time.sleep(60 * 10)
        is_complete = True


def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies

if __name__ == "__main__":
    get_save_cities_with_bb()
