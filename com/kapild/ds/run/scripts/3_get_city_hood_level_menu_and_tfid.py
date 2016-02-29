from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ds.GeoJson.shapely_utils import get_contained_shape
from shapely.geometry import shape, Point
from sklearn.feature_extraction.text import CountVectorizer
import string


import numpy as np
from sklearn import preprocessing
import os
from ds.foursquare.cities.cities_bounding_box import sf_bb, manhattan_bb, chicago_bb, austin_bb, atlanta_bb
from ds.run.scripts import data_directory
from ds.utils.str_utils import remove_space_lower_case

base_dir = os.path.dirname(os.path.realpath(__file__))
import json


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
            menu_str += menu[key] + " "
    return menu_str

class HOOD():
    def __init__(self, params):
        self.name = params["name"]
        self.menu = params["menu"]
        self.REGIONID = params["REGIONID"]

class SIM_HOOD():
    def __init__(self, params):
        self.name = params["name"]
        self.value = params["value"]
        self.REGIONID = params["REGIONID"]

def get_hood_top_menu_items(hood_index, is_normalize, menu_count_list, top_n_items, vocab):
    hood_count = menu_count_list[hood_index]
    if is_normalize is True:
        hood_count = normalize_row(hood_count)
    vocab_array = hood_count.toarray()[0]
    sorted_indix = get_decreasing_sort_index(vocab_array, top_n_items)
    return get_hood_menu_items(sorted_indix, vocab_array, vocab)


def set_similar_hoods(hood_menu_list):
    hood_cosine_matrix = get_similarity_matrix(hood_menu_list)
    top_similar = 10
    for index in range(0, len(hood_menu_list)):
        hood = hood_menu_list[index]
        print "Printing similar hood for: %s" % hood.get("name")
        hood_similar_items = get_similar_hood_items(hood_cosine_matrix, hood_menu_list, index, top_similar)
        hood["similar_hood"] = hood_similar_items
    return hood_menu_list


def set_menu_items_data(hood_menu_list_with_similar_hoods):
    vocab, menu_count_list = get_menu_items_vocab(hood_menu_list_with_similar_hoods)
    # assert menu_count_list.length() hood_menu_list.length()
    top_n_items = 100
    is_normalize = True
    for hood_index in range(0, len(hood_menu_list_with_similar_hoods)):
        hood = hood_menu_list_with_similar_hoods[hood_index]
        print "Printing for hood:%s" % hood.get("name")
        hood_top_menu_items = get_hood_top_menu_items(hood_index, is_normalize, menu_count_list, top_n_items, vocab)
        hood["menu_items"] = hood_top_menu_items
    return hood_menu_list_with_similar_hoods


def get_city_hood_level_menu_tfid_and_similarities(city_hood_level_menu_file):
    hood_menu_dict = json.load(open(city_hood_level_menu_file))
    hood_menu_data = hood_menu_dict["features"]

    hood_menu_list = []
    index = -1

    for hood_data in hood_menu_data:
        index += 1
        if "menu" not in hood_data:
            print "%s: Ignoring: %s" % (index, hood_data["properties"]["NAME"])
            continue
        else:
            print "%s: Processing: %s" % (index, hood_data["properties"]["NAME"])

        menu_lists_list = hood_data["menu"]
        menu_text = ""
        for menus_list in menu_lists_list:
            for menu in menus_list:
                # should not concatenate the menu text here. find n-grams separately and then combine.
                # print get_menu_str(menu)
                menu_text += get_menu_str(menu)
        current_hood = dict({
            "menu" : menu_text,
            "name" : get_hood_name(hood_data),
            "REGIONID" : hood_data["properties"]["REGIONID"]
        })
        hood_menu_list.append(current_hood)
    print "Total hoods %s:, total loaded:%s" % (len(hood_menu_list), len(hood_menu_data))

    # get similarity matrix
    hood_menu_list_with_similar_hoods = set_similar_hoods(hood_menu_list)

    # get cloud data
    hood_sim_and_menu_items = set_menu_items_data(hood_menu_list_with_similar_hoods)

    # sets the pair wise menu items between hoods
    set_sim_hood_common_top_menu_items(hood_sim_and_menu_items)

    # sets the hood similarity data in the geo data.
    set_sim_hood_data(hood_menu_data, hood_sim_and_menu_items)

    sim_out_file = city_hood_level_menu_file + "_sim"
    f_write = open(sim_out_file, "w")
    f_write.write(json.dumps(hood_menu_dict, sort_keys=False, indent=4, separators=(',', ': ')))
    f_write.close()

    print sim_out_file
    # top_features = [features[i] for i in indices[:top_n]]
    # print top_features

def set_sim_hood_data(hood_menu_data, hood_menu_list):
    menu_hood_region_id_dict = {}
    for hood_data in hood_menu_list:
        try:
            hood_data.pop("menu", None)
        except AttributeError:
            True
        menu_hood_region_id_dict[hood_data.get("REGIONID")] = hood_data

    for menu_hood_geo in hood_menu_data:
        region_id = menu_hood_geo["properties"]["REGIONID"]
        if region_id in menu_hood_region_id_dict:
            # menu_hood_geo["sim"] = json.dumps(menu_hood_region_id_dict[region_id], sort_keys=False, indent=4, separators=(',', ': '))
            menu_hood_geo.pop("menu", None)

            menu_hood_geo["sim"] = menu_hood_region_id_dict[region_id]

    return hood_menu_data

def set_sim_hood_common_top_menu_items(hood_sim_and_menu_items):
    region_id_menu_item_map = dict()
    for hood in hood_sim_and_menu_items:
        region_id_menu_item_map[hood.get("REGIONID")] = hood

    for hood_l_key in region_id_menu_item_map.keys():
        hood_left = region_id_menu_item_map[hood_l_key]
        for hood_right in hood_left["similar_hood"]:
            hood_r_key = hood_right["REGIONID"]
            # if hood_l_key != hood_r_key:
            top_items, top_distinct_items = get_hood_common_top_menu_items(
                hood_left.get("menu_items"), region_id_menu_item_map[hood_r_key]["menu_items"])
            # print "Between " + hood_left.get("name") + " and, " + hood_right.get("name")
            hood_right["menu_items"] = top_items
            hood_right["menu_items_distinct"] = top_distinct_items
            # for items in top_items:
            #     print items


def get_hood_name(hood):
    return hood["properties"]["NAME"]

def get_similarity_matrix(menu_hood_list):

    menu_X = []
    menu_Y = []
    for hood in menu_hood_list:
        menu_X.append(hood.get("menu"))
        menu_Y.append(hood.get("name"))

    print "Total X:%s Y:%s:" % (len(menu_X), len(menu_Y))

    print "Running vectorizer TfidfVectorizer.."
    vectorizer = TfidfVectorizer(min_df=2,  strip_accents = 'unicode', lowercase=True, stop_words="english",
                        ngram_range=(1,2), norm='l2', smooth_idf=True, sublinear_tf=False, use_idf=True)

    menu_tfidf_list = vectorizer.fit_transform(menu_X)
    hood_cosine_matrix = cosine_similarity(menu_tfidf_list, menu_tfidf_list)
    print hood_cosine_matrix

    return hood_cosine_matrix

def get_similar_hood_items(hood_cosine_matrix, hood_menu_list, index, top_similar=10):
    hood_similary = hood_cosine_matrix[index]
    sorted_similar_index = sorted(range(len(hood_similary)), key = hood_similary.__getitem__, reverse=True)

    hood_similar_items = []
    for top_index in range(0, top_similar):
        sim_index = sorted_similar_index[top_index]
        hood = hood_menu_list[sim_index]
        similar_hood = dict({
            "name" : hood.get("name"),
            "REGIONID" : hood.get("REGIONID"),
            "value" : hood_similary[sim_index]
        })
        hood_similar_items.append(similar_hood)
        # print "\t" + similar_hood.get("name") + ":" + str(similar_hood.get("value") )
    return hood_similar_items


def get_menu_item_vocab_tfid(menu_hood_list):
    menu_X = []
    menu_Y = []
    for hood in menu_hood_list:
        menu_X.append(hood.menu)
        menu_Y.append(hood.name)

    print "Total X:%s Y:%s:" % (len(menu_X), len(menu_Y))

    print "Running counter CountVectorizer.."

    vectorizer = TfidfVectorizer(min_df=2,  strip_accents = 'unicode', lowercase=True, stop_words="english",
                        ngram_range=(1,2), norm='l2', smooth_idf=True, sublinear_tf=False, use_idf=True)

    menu_tfidf_list = vectorizer.fit_transform(menu_X)

    #     indices_increasing_sorted = np.argsort(vectorizer.idf_)
    # double colon means start, end, skip. -1 for reverse
    top_n = 100
    # print 'low value features'
    # for i in indices_increasing_sorted[0:top_n]:
    #     print "Idf %s, value: %s" % (features[i], idf_[i])
    # print 'high value features'
    # for i in indices_increasing_sorted[-top_n:]:
    #     print "Idf %s, value: %s" % (features[i], idf_[i])
    vocab = vectorizer.get_feature_names()
    return vocab, menu_tfidf_list

def get_menu_items_vocab(menu_hood_list):

    menu_X = []
    menu_Y = []
    for hood in menu_hood_list:
        menu_X.append(hood.get("menu"))
        menu_Y.append(hood.get("name"))

    print "Total X:%s Y:%s:" % (len(menu_X), len(menu_Y))

    print "Running counter CountVectorizer.."

    vectorizer = CountVectorizer(min_df=1,  ngram_range=(1,2), stop_words="english")
    menu_count_list = vectorizer.fit_transform(menu_X)
    vocab = vectorizer.get_feature_names()

    return vocab, menu_count_list
    # double colon means start, end, skip. -1 for reverse


def get_hood_menu_items(sorted_indix, vocab_array, vocab):

    hood_top_menu_items = []
    for top_index in sorted_indix:
        row_cloud = dict()
        row_cloud["menu_item"] = vocab[top_index]
        row_cloud["value"] = vocab_array[top_index]
        hood_top_menu_items.append(row_cloud)
        # print "\t" + str(vocab[top_index]) + " " + str(vocab_array[top_index])
    return hood_top_menu_items

def get_hood_common_top_menu_items(menu_items_this, menu_items_that, top=50):
    menu_items_left = menu_items_this[:top]
    menu_items_right = menu_items_that[:top]

    menu_items_right_set = set()
    for menu_item in menu_items_right:
        menu_items_right_set.add(menu_item["menu_item"])

    menu_items_left_set = set()
    for menu_item in menu_items_left:
        menu_items_left_set.add(menu_item["menu_item"])

    u = menu_items_right_set & menu_items_left_set
    d = menu_items_left_set - menu_items_right_set
    common_top_menu_items = []
    distinct_top_menu_items = []
    for menu_item in menu_items_left:
        if menu_item["menu_item"] in menu_items_right_set:
            common_top_menu_items.append(menu_item)
        else:
            distinct_top_menu_items.append(menu_item)

    # for menu_item in menu_items_right:
    #     if menu_item["menu_item"] in menu_items_left_set:
    #         pass
    #     else:
    #         distinct_top_menu_items.append(menu_item)

    return common_top_menu_items, distinct_top_menu_items

def lower_and_remove_space(text):
    return string.lower(text).replace(" ", "_")

def normalize_row(array):
    return preprocessing.normalize(array.astype(float))

def get_decreasing_sort_index(array, top_k):
    return np.argsort(array)[::-1][:top_k]

def print_top_n_features(vectorizer, indices, top_n = 20):
    features = vectorizer.get_feature_names()
    top_features = [features[i] for i in indices[:top_n]]
    print top_features

if __name__ == "__main__":
    # city_bb = austin_bb
    # city_bb = atlanta_bb
    city_bb = sf_bb

    file_ext = ".json"
    city_venue_menu_hood_input_file = remove_space_lower_case(data_directory + city_bb.name + "_hood" + file_ext)
    get_city_hood_level_menu_tfid_and_similarities(city_venue_menu_hood_input_file)