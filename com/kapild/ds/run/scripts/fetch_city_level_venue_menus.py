from sklearn.feature_extraction.text import TfidfVectorizer
from ds.GeoJson.shapely_utils import get_contained_shape
from ds.backend.redis.Redis import RedisStoreImpl
from shapely.geometry import shape, Point
from ds.foursquare.cities.cities_bounding_box import sf_bb
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


def dump_city_neighborhood_level_menu_data(city_shp_json, city_venue_menu_file):
    city_shp = json.load(open(city_shp_json))
    city_venues_menu = json.load(open(city_venue_menu_file))

    f_write = open(city_venue_menu_file + "_hood", "w")
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

    f_write.write(json.dumps(city_shp, sort_keys=True, indent=4, separators=(',', ': ') ))
    f_write.close()


def get_top_tfid_menu_words_per_hood(file_json):
    hood_menu_file = json.load(open(file_json))["features"]

    menu_hood_list = []
    for menu_hood in hood_menu_file:
        menu_str = ""
        if "menu" not in menu_hood:
            continue
        menu_lists_list = menu_hood["menu"]
        for menus_list in menu_lists_list:
            for menu in menus_list:
                menu_name = menu["name"]
                menu_str = menu_str + " " + menu_name
        menu_hood_list.append(menu_str)

    print menu_hood_list[0][0:100]
    print menu_hood_list[1][0:100]

    vectorizer = TfidfVectorizer(min_df=2, stop_words = 'english',  strip_accents = 'unicode', lowercase=True,
                        ngram_range=(1,2), norm='l2', smooth_idf=True, sublinear_tf=False, use_idf=True)
    menu_tfidf = vectorizer.fit_transform(menu_hood_list)
    indices = np.argsort(vectorizer.idf_)[::1]
    features = vectorizer.get_feature_names()
    top_n = 20
    top_features = [features[i] for i in indices[:top_n]]
    print top_features

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

    # fetches menus for all the venues in a city
    get_city_level_menu_api(sf_bb)

    # params = {'is_fresh': False}
    # venue = {"id" : "49baae38f964a52094531fe3", "name": "kk"}
    # for menu in fs.get_menu_for_venue(venue, params):
    #     print menu

    city_bb = sf_bb

    # dump the menus for the city into a file.
    dump_city_neighborhood_level_menu_data(
         "/Users/kdalwani/code/workspace/FourquarePyCharmCrawl/com/kapild/ds/GeoJson/sf_geojson.json",
         city_bb.name + "_menu.json"
    )

    get_top_tfid_menu_words_per_hood(city_bb.name + "_menu.json" + "_hood")
