
import logging
from ds.backend.redis.Redis import RedisStoreImpl
from ds.backend.redis.utils import (
    get_user_liked_key,
    get_users_friends_key,
    get_users_saved_list,
    get_lists_saved_list,
    get_venue_details,
)
import json


class FoursquareRedisBackend:


    def __init__(self, redis_dict):
        logging.basicConfig()
        self.__Logger = logging.getLogger(__name__)
        self.__Logger.setLevel(logging.INFO)
        self.__Logger.info("staring FoursquareRedisBackend store")
        self.fsq_redis = RedisStoreImpl(redis_dict)


    def get_users_likes_venues(self, user_id="self", limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting users liked venues from redis")
        liked_venue_tuple = get_user_liked_key(user_id)
        self.__Logger.debug("Checking hash: %s with user_id: %s" % (liked_venue_tuple[0], liked_venue_tuple[1]))
        liked_venues = self.fsq_redis.get_hash_item(liked_venue_tuple[0], liked_venue_tuple[1])
        if liked_venues is not None:
            liked_venues_list = json.loads(liked_venues)
            self.__Logger.debug("Found %s venues" % len(liked_venues_list))
            return liked_venues_list
        else:
            self.__Logger.info("No like venue found for user %s venues", user_id)
            return None

    def add_users_likes_venues(self, user_id="self", venue_list=None, limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Adding users liked venues from redis")
        liked_venue_tuple = get_user_liked_key(user_id)
        self.__Logger.info("Adding key: %s with user_id: %s" % (liked_venue_tuple[0], liked_venue_tuple[1]))
        status_code = self.fsq_redis.put_hash_item(liked_venue_tuple[0], liked_venue_tuple[1], venue_list)
        if status_code:
            self.__Logger.debug("Added users liked venue total status:", status_code )

    def add_users_saved_list(self, user_id="self", venue_list=None, limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Adding users saved list to redis")
        user_saved_lists_tuple = get_users_saved_list(user_id)
        self.__Logger.info("Adding key: %s with user_id: %s" % (user_saved_lists_tuple[0], user_saved_lists_tuple[1]))
        status_code = self.fsq_redis.put_hash_item(user_saved_lists_tuple[0], user_saved_lists_tuple[1], venue_list)
        if status_code:
            self.__Logger.debug("Added users saved list total status:", status_code )

    def add_users_friend_list(self, user_id="self", venue_list=None, limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Adding users friend list to redis")
        user_friend_tuple = get_users_friends_key(user_id)
        self.__Logger.info("Adding key: %s with user_id: %s" % (user_friend_tuple[0], user_friend_tuple[1]))
        status_code = self.fsq_redis.put_hash_item(user_friend_tuple[0], user_friend_tuple[1], venue_list)
        if status_code:
            self.__Logger.debug("Added users liked venue total status:", status_code )

    def get_users_friends(self, user_id='self', limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting users friend from redis: %s" % user_id)
        user_friend_tuple = get_users_friends_key(user_id)
        self.__Logger.debug("Checking hash: %s with user_id: %s" % (user_friend_tuple[0], user_friend_tuple[1]))
        user_friends = self.fsq_redis.get_hash_item(user_friend_tuple[0], user_friend_tuple[1])
        if user_friends is not None:
            user_friends_list = json.loads(user_friends)
            self.__Logger.debug("Found %s friends:", len(user_friends_list))
            return user_friends_list
        else:
            self.__Logger.debug("No friends found for user %s", user_id)
            return None

    def get_users_saved_list(self, user_id='self', limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting users saved list from redis: %s" % user_id)
        user_friend_tuple = get_users_saved_list(user_id)
        self.__Logger.debug("Checking hash: %s with user_id: %s" % (user_friend_tuple[0], user_friend_tuple[1]))
        user_save_list = self.fsq_redis.get_hash_item(user_friend_tuple[0], user_friend_tuple[1])
        if user_save_list is not None:
            user_save_list_lists = json.loads(user_save_list)
            self.__Logger.debug("Found %s lists:", len(user_save_list_lists))
            return user_save_list_lists
        else:
            self.__Logger.info("No lists found for user:%s in Redis", user_id)
            return None


    def get_lists_items(self, list_id, imit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting Lists saved list from redis: %s" % list_id)
        lists_item_tuple = get_lists_saved_list(list_id)
        self.__Logger.debug("Checking hash: %s with list_id: %s" % (lists_item_tuple[0], lists_item_tuple[1]))
        lists_saved_items = self.fsq_redis.get_hash_item(lists_item_tuple[0], lists_item_tuple[1])
        if lists_saved_items is not None:
            lists_saved_items_lists = json.loads(lists_saved_items)
            self.__Logger.info("Found %s lists:", len(lists_saved_items_lists))
            return lists_saved_items_lists
        else:
            self.__Logger.info("No lists found for user:%s in Redis", list_id)
            return None

    def add_lists_item_list(self, list_id, lists_item_list):
        self.__Logger.debug("Adding Lists item list id:%s to redis", list_id)
        lists_item_tuple = get_lists_saved_list(list_id)
        self.__Logger.info("Adding key: %s with list: %s" % (lists_item_tuple[0], lists_item_tuple[1]))
        status_code = self.fsq_redis.put_hash_item(lists_item_tuple[0], lists_item_tuple[1], lists_item_list)
        if status_code:
            self.__Logger.debug("Added users liked venue total status:", status_code )


    def get_venue_detail(self, venue_id,  attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting details for Venue id:%s from redis" % venue_id)
        venue_details_tuple = get_venue_details(venue_id)
        self.__Logger.debug("Checking hash: %s with venue_id: %s" % (venue_details_tuple[0], venue_details_tuple[1]))
        venue_details = self.fsq_redis.get_hash_item(venue_details_tuple[0], venue_details_tuple[1])
        if venue_details is not None and venue_details != 'null':
            venue_details = json.loads(venue_details)
            self.__Logger.debug("Found details for venue id:%s:", venue_id)
            return venue_details
        else:
            self.__Logger.debug("No venue details found for venue id:%s in Redis", venue_id)
            return None

    def add_venue_detail(self, venue_id, venue_detail):
        self.__Logger.debug("Adding Venue id:%s to redis", venue_id)
        venue_item_tuple = get_venue_details(venue_id)
        self.__Logger.info("Adding key: %s with venue_id: %s" % (venue_item_tuple[0], venue_item_tuple[1]))
        status_code = self.fsq_redis.put_hash_item(venue_item_tuple[0], venue_item_tuple[1], venue_detail)
        if status_code:
            self.__Logger.info("Added venue details, status:", status_code )
