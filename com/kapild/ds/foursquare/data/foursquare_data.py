
from ds.backend.redis.foursquare_redis import FoursquareRedisBackend
from ds.foursquare.foursquare_wrap import FourSquareWrap

import json
import logging

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
