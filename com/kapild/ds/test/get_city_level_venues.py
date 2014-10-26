from ds.backend.redis.Redis import RedisStoreImpl
import ds.foursquare.cities.cities as cities
from ds.foursquare.cities.cities import get_top_cities_ll

import foursquare
import json
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

    # params['category_id'] = "4bf58dd8d48988d10f941735"
    # params['loc'] = {"ll" : "37.7751,-122.41", "name": "SF"}

def get_city_level_venue(city):
    indx = 0
    all_venues_list = {}
    for venue in fs.get_cities_all_cat_venues_list(city):
        indx = indx + 1
        name = venue["name"]
        lat_lng = []
        lat_lng.append(venue["location"]["lng"])
        lat_lng.append(venue["location"]["lat"])
        all_venues_list[name[0:10]] = lat_lng
        # get_menu_for_venue(venue)
    print json.dumps(all_venues_list)

        # print venue["name"] + "     by           " + (address)
    print str(indx)


def get_menu_for_venue(venue):
    params = {}
    params['is_fresh'] = False

    for menu in fs.get_menu_for_venue(venue, params):
        print menu

if __name__ == "__main__":
    get_city_level_venue(cities.sf)
