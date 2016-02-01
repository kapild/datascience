from ds.backend.redis.Redis import RedisStoreImpl
from ds.foursquare import MoreThanMaxResultsExceptions
from ds.foursquare.cities.cities_bounding_box import get_top_cities_bb, sf_bb, \
    chicago_bb, manhattan_bb, austin_bb, atlanta_bb
from ds.foursquare.cities.geo_utils import get_bb_grid
from ds.utils.str_utils import remove_space_lower_case

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

fs = Foursquare(redis_dict)
redis = RedisStoreImpl(redis_dict)

category_more_results = ['4bf58dd8d48988d14e941735', '4bf58dd8d48988d145941735', '4bf58dd8d48988d142941735']

# Does a bounding box search for a given location and list of al categories.
def get_bb_box_venue_search(location, category_list):

    cat_length = len(category_list)
    index = 0
    is_complete = False
    is_time_out_error = False
    total_venus = 0
    print "running for:" + location.name + " bounding box:" + str(location.nw) + ", " + str(location.se)
    for category in category_list:
        run_category_venue_search(location, category)

    print "total venu for the city:" + location.name +  "is :" + str(total_venus)

def run_category_venue_search(location, category):
    if category['id'] in category_more_results:
        num_num = 12
    try:
        run_category_bb_venue_search(location, category, num_num)
    except foursquare.RateLimitExceeded:
        print "Sleeping due to rate"
        time.sleep(60 * 10)
        print "Recursive calling run_category_venue_search"
        run_category_venue_search(location, category)

def run_category_bb_venue_search(location, category, num_num):
    total_venue = 0
    print location.name + ", " + (category["name"])
    params = dict()
    params['is_fresh'] = False
    params['categoryId'] = category['id']
    params['name'] = location.name
    params['cat_name'] = category["name"]
    for location_bb_tuple in get_bb_grid(location.nw, location.se, num=num_num):
        params['num'] = location_bb_tuple[0]
        params['ne'] = location_bb_tuple[1]
        params['sw'] = location_bb_tuple[2]
        try:
            for venue in fs.get_venues_search(params):
                total_venue += 1
            print "total venus so far:" + str(total_venue)
        except MoreThanMaxResultsExceptions:
            delete_venue_search_key(category["name"], category["id"], num_num, location)
            run_category_bb_venue_search(location, category, num_num + 2)
        except foursquare.RateLimitExceeded:
            print "Sleeping due to rate"
            time.sleep(60 * 10)
            print "Recursive calling run_category_bb_venue_search"
            run_category_bb_venue_search(location, category, num_num)

def delete_venue_search_key(cat_name, category_id, num_num, city_bb):
    print "Deleting key for category:" + category_id + ",num:" + str(num_num) + ",city" + city_bb.name
    params = dict()
    params['categoryId'] = category_id
    params['cat_name'] = cat_name
    for location_tuple in get_bb_grid(city_bb.nw, city_bb.se, num=num_num):
        params['num'] = location_tuple[0]
        params['ne'] = location_tuple[1]
        params['sw'] = location_tuple[2]
        fs.delete_venues_search(params)

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
    run_san_francisco()
    # run_austin()
    # run_atlanta()
