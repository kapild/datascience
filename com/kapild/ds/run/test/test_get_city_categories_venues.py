from ds.backend.redis.Redis import RedisStoreImpl
from ds.foursquare.cities.cities import get_top_cities_ll

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

def filter_category(name="Food"):
    cat = None
    for category in get_fsq_categories():
        if category['name'] == name:
            cat = category

    list_a = []
    fs.get_child_category_first(cat, list_a)
    location_list = get_top_cities_ll()[0:1]
    category_list = list_a

    try:
        for location in location_list:
            for category in category_list:
                print location.name + ", " + (category["name"])
                params = {}
                params['is_fresh']  = True
                params['category_id'] = category['id']
                params['loc'] = location
                for venue in fs.get_venues_search(params):
                    continue
                    # print location["name"] + "," + category["name"] + "," + venue['name']
    except foursquare.RateLimitExceeded:
        time.sleep(60 * 40)

def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies

if __name__ == "__main__":
    filter_category()
