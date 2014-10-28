from ds.backend.redis.Redis import RedisStoreImpl
from ds.backend.redis.utils import get_fsq_city_name, get_fsq_city_bb_name
from ds.foursquare.cities.cities import get_top_cities_ll
from ds.foursquare.cities.cities_bounding_box import get_top_cities_bb, CityBB, sf_bb
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

def get_city_level_menu_api(city_bb=sf_bb, dump_attr=["name", "location", "menus_list"]):

    index = 0
    is_complete = False
    f_write = open(sf_bb.name + "_menu.json", mode='w')

    params = {'is_fresh': False}
    city_venues_menu = []
    while not is_complete:
        for venue in fs.get_city_level_venues(city_bb):
            venue_menu_list = []
            print "%s:Getting menu for:%s" % (index, venue["name"])
            try:
                for venue_menu in fs.get_menu_for_venue(venue, params):
                    venue_menu_list.append(venue_menu)
                if len(venue_menu_list) == 0:
                    continue
                venue["menus_list"] = venue_menu_list
                is_complete = True
                venue_dict = {}
                for key in dump_attr:
                    if key in venue:
                        venue_dict[key] = venue[key]
                index += 1
                city_venues_menu.append(venue_dict)
            except foursquare.RateLimitExceeded:
                print "Sleeping due to rate"
                print "done:" + str(index)
                f_write.write(json.dumps(city_venues_menu, sort_keys=True, indent=4, separators=(',', ': ')))
                f_write.close()
                print "done dumping"
                time.sleep(60 * 10)

    # f_write.write(json.dumps(venue))
    # f_write.close()

def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies

if __name__ == "__main__":
    get_city_level_menu_api(sf_bb)

    # params = {'is_fresh': False}
    # venue = {"id" : "49baae38f964a52094531fe3", "name": "kk"}
    # for menu in fs.get_menu_for_venue(venue, params):
    #     print menu