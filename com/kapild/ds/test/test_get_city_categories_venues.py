from ds.backend.redis.Redis import RedisStoreImpl
from ds.foursquare.cities.cities import get_top_cities_ll

import foursquare

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

fs = Foursquare(redis_dict)
redis = RedisStoreImpl(redis_dict)


def filter_category(name="Food"):
    cat = None
    for category in get_fsq_categories():
        if category['name'] == name:
            cat = category

    list_a = []
    fs.get_child_category_first(cat, list_a)
    location_list = get_top_cities_ll()[0:2]
    category_list = list_a[0:2]

    for category in category_list:
        for location in location_list:
            params = {}
            params['category_id'] = category['category_id']
            params['loc'] = location
            venue = fs.get_venues_search(params)
            print venue
def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies

if __name__ == "__main__":
    filter_category()
