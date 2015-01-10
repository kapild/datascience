
from ds.backend.redis.foursquare_redis import FoursquareRedisBackend
from ds.backend.redis.utils import get_fsq_city_name, get_venue_location_categories, get_venue_menu, \
    get_fsq_city_bb_name
from ds.foursquare.foursquare_wrap import FourSquareWrap

import json
import logging
from ds.foursquare.utils import my_log


class Foursquare:

    def __init__(self, redis_dict):
        self.__Logger = logging.getLogger(__name__)
        self.__Logger.setLevel(logging.INFO)

        self.fsq_api = FourSquareWrap()
        self.fsq_redis = FoursquareRedisBackend(redis_dict)

    def get_users_saved_list(self, user_id='self', **kwargs):
        self.__Logger.debug("Getting users saved list.")
        is_fresh = kwargs.get("is_fresh", False)
        user_list_lists = None
        if not is_fresh:
            user_list_lists = self.fsq_redis.get_users_saved_list(user_id)

        if user_list_lists is None:
            self.__Logger.debug("No users saved list from Redis")
            user_list_lists = []
            self.__Logger.debug("Getting Users list from Foursquare API.")
            for api_user_list in self.fsq_api.get_user_saved_list(user_id):
                user_list_lists.append(api_user_list)
            self.__Logger.debug("Adding Users saved list to Redis.")
            self.fsq_redis.add_users_saved_list(user_id, json.dumps(user_list_lists))
        self.__Logger.info("Returning users saved list.")
        for user_list in user_list_lists:
            yield user_list

    def get_users_liked_venue(self, user_id='self', **kwargs):
        self.__Logger.debug("Getting users liked venue")
        is_fresh = kwargs.get("is_fresh", False)
        if not is_fresh:
            liked_venue_redis = self.fsq_redis.get_users_likes_venues(user_id)
        if liked_venue_redis is None:
            self.__Logger.info("No users liked venue from Redis")
            liked_venue_redis = []
            self.__Logger.info("Getting data from Foursquare API.")
            for api_liked_venus in self.fsq_api.get_users_likes_venues(user_id):
                liked_venue_redis.append(api_liked_venus)
            self.__Logger.debug("Redis Users liked venue adding data.")
            self.fsq_redis.add_users_likes_venues(user_id, json.dumps(liked_venue_redis))
        self.__Logger.debug("Returning users liked venue")
        for venue in liked_venue_redis:
            yield venue

    def get_users_friend(self, user_id='self', **kwargs):
        self.__Logger.info("Getting users friends list")
        is_fresh = kwargs.get("is_fresh", False)
        if not is_fresh:
            users_friend_list = self.fsq_redis.get_users_friends(user_id)
        if users_friend_list is None:
            self.__Logger.info("No users friend found from Redis")
            users_friend_list = []
            self.__Logger.info("Getting data from Foursquare API.")
            for user_friend in self.fsq_api.get_users_friends(user_id):
                users_friend_list.append(user_friend)
            self.__Logger.debug("Redis Users friend list adding data.")
            self.fsq_redis.add_users_friend_list(user_id, json.dumps(users_friend_list))

        self.__Logger.info("Returning user_id:%s total:%s friends" % (user_id, len(users_friend_list)))
        self.__Logger.debug("Returning users friend list")
        for friend in users_friend_list:
            yield friend

    def get_lists_items(self, list_id, **kwargs):
        self.__Logger.info("Getting list_id:%s items", list_id)
        is_fresh = kwargs.get("is_fresh", False)
        lists_item_list = None
        if not is_fresh:
            lists_item_list = self.fsq_redis.get_lists_items(list_id)
        if lists_item_list is None:
            self.__Logger.debug("No lists items found in Redis")
            lists_item_list = []
            self.__Logger.debug("Getting data from Foursquare API.")
            for list_item in self.fsq_api.get_lists_items(list_id):
                lists_item_list.append(list_item)
            self.__Logger.debug("Redis adding lists items.")
            self.fsq_redis.add_lists_item_list(list_id, json.dumps(lists_item_list))

        self.__Logger.info("Returning list_id:%s total:%s items" % (list_id, len(lists_item_list)))
        self.__Logger.debug("Returning users list")
        for item in lists_item_list:
            yield item

    def get_venue_details(self, venue_id, **kwargs):
        self.__Logger.info("Getting venue_id:%s details", venue_id)
        is_fresh = kwargs.get("is_fresh", False)
        venue_item = None
        if not is_fresh:
            venue_item = self.fsq_redis.get_venue_detail(venue_id)
        if venue_item is None:
            self.__Logger.debug("No venue details found in Redis")
            self.__Logger.debug("Getting data from Foursquare API.")
            venue_item = self.fsq_api.get_venue_item_details(venue_id)
            self.__Logger.debug("Redis adding lists items.")
            self.fsq_redis.add_venue_detail(venue_id, json.dumps(venue_item))

        self.__Logger.debug("Returning venue_id:%s details" % (venue_id))
        yield venue_item

    def get_venue_categories_lists(self, **kwargs):
        self.__Logger.info("Getting venue categories ")
        is_fresh = kwargs.get("is_fresh", False)
        categories_list = None
        if not is_fresh:
            categories_list = self.fsq_redis.get_all_categories_list()
        if categories_list is None:
            self.__Logger.debug("No venue categories found in Redis")
            categories_list = []
            self.__Logger.debug("Getting data from Foursquare API.")
            for category in self.fsq_api.get_venue_categories():
                categories_list.append(category)
            self.__Logger.debug("Redis adding lists items.")
            self.fsq_redis.add_all_categories_list(categories_list)

        self.__Logger.debug("Returning categories list:%s size" % len(categories_list))
        for item in categories_list:
            yield item


    def get_city_level_venues(self, city_bb):
        city_name = city_bb.name
        city_hash_name = get_fsq_city_bb_name(city_name)
        city_hash_keys = self.fsq_redis.get_all_hash_keys(city_hash_name)
        venue_id_set = set()
        for hash_key in city_hash_keys:
            venue_items_json = self.fsq_redis.get_hash_item(city_hash_name, hash_key)
            venue_items = json.loads(venue_items_json)
            if len(venue_items) > 0:
                for venue in venue_items:
                    venue_id = venue['id']
                    if venue_id not in venue_id_set:
                        venue_id_set.add(venue_id)
                        yield venue


    def get_venue_keys(self, **kwargs):
        venue_keys = self.fsq_redis.get_venue_keys()
        if venue_keys is not None:
            for venue_key in venue_keys:
                yield venue_key
        else:
            yield None

    def get_cities_all_cat_venues_list(self, city):
        city_name = city.name
        self.__Logger.info("Getting venues for city:%s" % city_name)
        fsq_city_hash_name = get_fsq_city_name(city_name)
        city_category_keys = self.fsq_redis.get_all_hash_keys(fsq_city_hash_name)

        venue_id_hash = set()
        if city_category_keys is not None and len(city_category_keys) > 0:
            self.__Logger.info("found %s keys for hash:%s" % (len(city_category_keys), fsq_city_hash_name))
            for category_key in city_category_keys:
                city_category_tuple = get_venue_location_categories(city_name, category_key)
                list_venue_json = self.fsq_redis.get_hash_item(city_category_tuple[0], category_key)
                list_venue = json.loads(list_venue_json)
                for venue in list_venue:
                    venue_id = venue["id"]
                    if venue_id not in  venue_id_hash:
                        venue_id_hash.add(venue_id)
                        yield venue

    def get_menu_for_venue(self, venue, kwargs):
        venue_name = venue["name"]
        venue_id = venue["id"]
        is_fresh = kwargs.get("is_fresh", False)

        fsq_venue_menu_tuple = get_venue_menu(venue_id)
        menu_list = None
        if not is_fresh:
            self.__Logger.info("Getting menu for venue:%s, %s" % (venue_name, venue_id))
            menu_list_str = self.fsq_redis.get_hash_item(fsq_venue_menu_tuple[0], fsq_venue_menu_tuple[1])
            if menu_list_str is not None:
                menu_list = json.loads(menu_list_str)

        if menu_list is None:
            self.__Logger.debug("No Menu found in Redis %s keys for hash:%s" % (fsq_venue_menu_tuple, fsq_venue_menu_tuple))
            menu_list = []
            for menu in self.fsq_api.get_menu_details(venue_id, kwargs):
                menu_list.append(menu)
            self.__Logger.debug("Redis Venue search adding data.")
            self.fsq_redis.put_hash_item(fsq_venue_menu_tuple[0], fsq_venue_menu_tuple[1], json.dumps(menu_list))
        for menu in menu_list:
            yield menu

    def get_venues_search(self, kwargs):
        # my_log(self.__Logger, logging.INFO, kwargs)
        is_fresh = kwargs.get("is_fresh", False)
        venues_search = None
        category_id = kwargs.get("categoryId")
        city_name = kwargs.get("name")
        category_key = category_id + "_" + kwargs["num"]
        if not is_fresh:
            venues_search = self.fsq_redis.get_venue_search(category_key, city_name)
        if venues_search is None:
            self.__Logger.debug("No venues search from Redis for: " + category_key + "," + city_name)
            venues_search = []
            self.__Logger.debug("Getting venues search data from Foursquare API.")
            for venue in self.fsq_api.get_category_location_venue_search(kwargs):
                venues_search.append(venue)
            self.__Logger.debug("Redis Venue search adding data.")
            self.fsq_redis.add_venue_search(city_name, category_key, json.dumps(venues_search))
        self.__Logger.debug("Returning venue search for category_id:%s, city_name=%s" %(category_key, city_name))
        for venue in venues_search:
            yield venue


    def get_city_bb_level_venue_hash_keys(self, city):
        city_name = city.name
        city_hash_name = get_fsq_city_name(city_name)
        city_hash_keys = self.fsq_redis.get_all_hash_keys(city_hash_name)
        for hash_key in city_hash_keys:
            yield hash_key

    def get_child_category_first(self, category_tree, cat_list):

        if 'categories' in category_tree and len(category_tree['categories']) == 0:
            cat_list.append(self._get_cat_dict(category_tree))
            return

        if 'categories' in category_tree and len(category_tree['categories']) > 0:
            for categories in category_tree['categories']:
                   self.get_child_category_first(categories, cat_list)

        cat_list.append(self._get_cat_dict(category_tree))

    @staticmethod
    def _get_cat_dict(category_tree, attr=['id', 'name']):
        category_dict = {}
        for key in attr:
            category_dict[key] = category_tree[key]
        return category_dict
