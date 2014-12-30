from sklearn.feature_extraction.text import TfidfVectorizer
from ds.GeoJson.shapely_utils import get_contained_shape
from ds.backend.redis.Redis import RedisStoreImpl
from shapely.geometry import shape, Point
from ds.foursquare.cities.cities_bounding_box import sf_bb
from sklearn.feature_extraction.text import CountVectorizer
import foursquare
from ds.foursquare.data.foursquare_data import Foursquare
import time
import string


import numpy as np
from sklearn import preprocessing
import os
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



base_dir = os.path.dirname(os.path.realpath(__file__))
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

    f_write.write(json.dumps(city_shp, sort_keys=False, indent=4, separators=(',', ': ') ))
    f_write.close()

def get_menu_str(menu, append=['name']):
    menu_str = ''
    for key in append:
        if key in menu:
            menu_str+= menu[key] + " "
    return menu_str

def get_top_tfid_menu_words_per_hood(file_json):
    hood_menu_file = json.load(open(file_json))["features"]

    menu_hood_list = []
    index = -1

    for menu_hood in hood_menu_file:
        hood_dict = {}
        index+=1
        if "menu" not in menu_hood:
            print "%s: Ignoring: %s" % (index, menu_hood["properties"]["NAME"])
            continue
        else:
            print "%s: Processing: %s" % (index, menu_hood["properties"]["NAME"])

        menu_lists_list = menu_hood["menu"]
        menu_name = ""
        for menus_list in menu_lists_list:
            for menu in menus_list:
                # print get_menu_str(menu)
                menu_name += get_menu_str(menu)
        hood_dict["menu"]  = menu_name
        hood_dict["name"] = get_hood_name(menu_hood)
        menu_hood_list.append(hood_dict)
        # menu_hood_list.append([menu_hood, menu_name])
    print "Total hoods %s:" % (len(menu_hood_list))

    _run_tfid_vectorizer(menu_hood_list)
    # top_features = [features[i] for i in indices[:top_n]]
    # print top_features

def get_hood_name(hood):
    return hood["properties"]["NAME"]

def _run_tfid_vectorizer(menu_hood_list):

    X = []
    hood_name_list = []
    for x_all in menu_hood_list:
        X.append(x_all["menu"])
        hood_name_list.append(x_all["name"])

    print "Total X:%s Y:%s:" % (len(X), len(hood_name_list))

    print "Running vectorizer TfidfVectorizer.."
    vectorizer = TfidfVectorizer(min_df=2,  strip_accents = 'unicode', lowercase=True, stop_words="english",
                        ngram_range=(1,2), norm='l2', smooth_idf=True, sublinear_tf=False, use_idf=True)

    menu_tfidf_list = vectorizer.fit_transform(X)
    hood_sim_matrix = (menu_tfidf_list * menu_tfidf_list.T).todense()
    indices_increasing_sorted = []
    idf_ = []
    if vectorizer.idf_ is not None:
        indices_increasing_sorted = np.argsort(vectorizer.idf_)
        idf_ = vectorizer.idf_
    features = vectorizer.get_feature_names()

    # double colon means start, end, skip. -1 for reverse
    top_n = 100
    # print 'low value features'
    # for i in indices_increasing_sorted[0:top_n]:
    #     print "Idf %s, value: %s" % (features[i], idf_[i])
    # print 'high value features'
    # for i in indices_increasing_sorted[-top_n:]:
    #     print "Idf %s, value: %s" % (features[i], idf_[i])

    top_n = 30
    is_normalize = False
    print_similar_hood(hood_sim_matrix, menu_hood_list)
    for hood_index in range(0, len(X)):
        hood_name = hood_name_list[hood_index]
        print "Printing for hood:%s" % hood_name
        hood_tfidf = menu_tfidf_list[hood_index]
        if is_normalize is True:
            hood_tfidf = normalize_row(hood_tfidf)
        sorted_indix = get_decreasing_sort_index(hood_tfidf.toarray()[0], top_n)
        similar_hoods = menu_hood_list[hood_index]["similar_hood"]
        print_cloud_json(hood_name, sorted_indix, hood_tfidf, features, similar_hoods)
        # for top_index in sorted_indix:
        #     hood_1d = hood_tfidf.toarray()[0]
        #     print "\t" + str(hood_1d[top_index]) + " " + features[top_index]

def print_similar_hood(hood_sim_matrix, menu_hood_list, top_match = 3):
    for hood_index in range(0, len(menu_hood_list)):
        hood_dict = menu_hood_list[hood_index]
        hood_name = hood_dict["name"]
        print "Similar hood:%s" % hood_name
        hood_similary = hood_sim_matrix[hood_index]
        sorted_indix = get_decreasing_sort_index(hood_similary[0], top_match)
        hood_similar_items = []
        for top_index in range(2, 5):
            hood_sim = dict()
            sim_index = sorted_indix.tolist()[0][-top_index]
            similar_hood = menu_hood_list[sim_index]["name"]
            sim_val = hood_similary[0].tolist()[0][sim_index]
            hood_sim["name"] = similar_hood
            hood_sim["value"] = sim_val
            hood_similar_items.append(hood_sim)
            print "\t" + similar_hood + ":" + str(sim_val )
        hood_dict["similar_hood"] = hood_similar_items


def _get_count_data(menu_hood_list):

    X = []
    Y = []
    for x_all in menu_hood_list:
        X.append(x_all[1])
        Y.append(x_all[0])

    print "Total X:%s Y:%s:" % (len(X), len(Y))

    print "Running counter CountVectorizer.."

    vectorizer = CountVectorizer(min_df=1,  ngram_range=(1,2), stop_words="english")
    menu_count_list = vectorizer.fit_transform(X)
    features = vectorizer.get_feature_names()

    # double colon means start, end, skip. -1 for reverse

    top_n = 30
    is_normalize = True
    for hood_index in range(0, len(X)):
        hood_prop = Y[hood_index]["properties"]["NAME"]
        print "Printing for hood:%s" % hood_prop
        hood_count = menu_count_list[hood_index]
        # import pdb
        # pdb.set_trace()
        if is_normalize is True:
            hood_count = normalize_row(hood_count)
        sorted_indix = get_decreasing_sort_index(hood_count.toarray()[0], top_n)

        print_cloud_json(hood_prop, sorted_indix, hood_count, features)
        # for top_index in sorted_indix:
        #     hood_1d = hood_count.toarray()[0]
        #     print "\t" + str(hood_1d[top_index]) + " " + features[top_index]

def print_cloud_json(hood_name, sorted_indix, hood_count, features, similar_hood):

    file_loc = base_dir + "/gen_data/" + lower_and_remove_space(hood_name) + ".json"
    fwrite = open(file_loc, "w")
    hood_json_list = []
    for top_index in sorted_indix:
        hood_1d = hood_count.toarray()[0]
        row_cloud = []
        row_cloud.append(features[top_index])
        row_cloud.append(hood_1d[top_index])
        hood_json_list.append(row_cloud)
        # print "\t" + str(hood_1d[top_index]) + " " + features[top_index]
    fwrite.write(json.dumps(
        {
            "tfidf" :hood_json_list,
            "similar_hoods" : similar_hood
        }, sort_keys=False, indent=4, separators=(',', ': ')
    ))
    fwrite.close()
    # print json.dumps(hood_json_list)

def lower_and_remove_space(text):
    return string.lower(text).replace(" ", "_")

def normalize_row(array):
    return preprocessing.normalize(array.astype(float))

def get_decreasing_sort_index(array, top_k):
    return np.argsort(array)[::-1][:top_k]
def get_city_level_menu_api(city_bb=sf_bb, dump_attr=["name", "location", "menus_list"]):

    index = 0
    total = 0
    is_complete = False
    f_write = open(sf_bb.name + "_menu.json", mode='w')

    params = {'is_fresh': False}
    city_venues_menu = []
    while not is_complete:
        for venue in fs.get_city_level_venues(city_bb):
            venue_menu_list = []
            print "%s:%s, Getting menu for:%s" % (index, total, venue["name"])
            try:
                total+=1
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

    # f_write.write(json.dumps(city_venues_menu))

    f_write.write(json.dumps(city_venues_menu, sort_keys=False, indent=4, separators=(',', ': '))
    )
    f_write.close()

def get_fsq_categories():
    kwargs = {'is_fresh' : False}
    for categroies in fs.get_venue_categories_lists(**kwargs):
        yield categroies

if __name__ == "__main__":
    # get_city_level_menu_api(sf_bb)

    # params = {'is_fresh': False}
    # venue = {"id" : "49baae38f964a52094531fe3", "name": "kk"}
    # for menu in fs.get_menu_for_venue(venue, params):
    #     print menu

    city_bb = sf_bb
    # dump_city_neighborhood_level_menu_data(
    #      "/Users/kdalwani/code/workspace/FourquarePyCharmCrawl/com/kapild/ds/GeoJson/sf_geojson.json",
    #      city_bb.name + "_menu.json"
    # )

    get_top_tfid_menu_words_per_hood(city_bb.name + "_menu.json" + "_hood")
