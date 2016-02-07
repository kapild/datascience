from ds.backend.redis.Redis import RedisStoreImpl
from ds.foursquare import MoreThanMaxResultsExceptions
from ds.foursquare.cities.cities_bounding_box import get_top_cities_bb, sf_bb, \
    chicago_bb, manhattan_bb, austin_bb, atlanta_bb, CityBB
from ds.foursquare.cities.geo_utils import get_bb_grid
from ds.utils.str_utils import remove_space_lower_case

import foursquare
import time
import copy
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

default_num = 6
total_venue = 0

# Does a bounding box search for a given location and list of al categories.
def get_bb_box_venue_search(location, category_list):

    print "running for:" + location.name + " bounding box:" + str(location.nw) + ", " + str(location.se)
    for category in category_list:
        run_category_venue_search(location, category)

    print "total venue for the city:" + location.name +  "is :" + str(total_venue)

def run_category_venue_search(location, category, num_num=default_num):

    if category['id'] in category_more_results:
        num_num = 12
    try:
        params = dict()
        params['is_fresh'] = False
        params['categoryId'] = category['id']
        params['loc_name'] = location.name
        params['cat_name'] = category["name"]
        run_category_bb_venue_search(location, params, num_num)
    except foursquare.RateLimitExceeded:
        print "Sleeping due to rate"
        time.sleep(60 * 10)
        print "Recursive calling run_category_venue_search"
        run_category_venue_search(location, category, num_num)

def run_category_bb_venue_search(location, params, num_num, is_new=True):
    print location.name + ", " + (params["loc_name"])
    for location_bb_tuple in get_bb_grid(location.nw, location.se, num=num_num):
        params['ne'] = location_bb_tuple[1]
        params['sw'] = location_bb_tuple[2]
        key = category_tuple_key(location_bb_tuple[0], params, is_new)
        new_params = copy.deepcopy(params)
        new_params['key'] = key
        run_category_search_tuple(new_params, num_num, location)
        print "done for loop bb.." + key

def run_category_search_tuple(params, num_num, location):
    global total_venue
    try:
        for venue in fs.get_venues_search(params):
            total_venue += 1
        print "total venus so far:" + str(total_venue)
    except MoreThanMaxResultsExceptions:
        delete_venue_search_key(params)
        new_location = get_new_location(params)
        # new_params = copy.deepcopy(params)
        run_category_bb_venue_search(new_location, params, default_num, False)
        print "done recursive calling.." + params["key"]
    except foursquare.RateLimitExceeded:
        print "Sleeping due to rate"
        time.sleep(60 * 10)
        print "Recursive calling run_category_search_tuple"
        run_category_search_tuple(params, num_num, location)

def get_new_location(params):
    location = CityBB({
        "name" : params["loc_name"],
        "bb" : [params["ne"], params["sw"]]
    })
    return location

def category_tuple_key(num_num, params, is_new):
    tuple_key = ""
    if not is_new and num_num != "":
        tuple_key = "_" + num_num + "_"

    if "key" in params:
        prev_key = params["key"]
    else:
        category_id = params.get("categoryId")
        cat_name = params.get('cat_name')
        cat_num = num_num
        prev_key = remove_space_lower_case(cat_name) + "_" + category_id + "_" + cat_num

    x = prev_key + tuple_key
    return x

def delete_venue_search_key(params):
    print "Deleting key:" + params['key']
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
