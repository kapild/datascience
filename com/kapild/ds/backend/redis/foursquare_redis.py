


import logging
from ds.backend.redis.Redis import RedisStoreImpl
from ds.backend.redis.utils import (
    get_user_liked_key,
    get_users_friends_key,
)
import json

class FoursquareRedisBackend:


    def __init__(self, redis_dict):
        self.__Logger = logging.getLogger(__name__)
        self.__Logger.setLevel(logging.INFO)
        self.__Logger.info("staring FoursquareRedisBackend store")
        self.fsq_redis = RedisStoreImpl(redis_dict)


    def get_users_likes_venues(self, user_id="self", limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting users liked venues from redis")
        liked_venue_tuple = get_user_liked_key(user_id)
        self.__Logger.info("Checking hash: %s with user_id: %s" % (liked_venue_tuple[0], liked_venue_tuple[1]))
        liked_venues = self.fsq_redis.get_hash_item(liked_venue_tuple[0], liked_venue_tuple[1])
        if liked_venues is not None:
            liked_venues_list = json.loads(liked_venues)
            self.__Logger.info("Found %s venues" % len(liked_venues_list))
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
            self.__Logger.info("Added users liked venue total status:", status_code )

    def add_users_friend_list(self, user_id="self", venue_list=None, limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Adding users friend list to redis")
        user_friend_tuple = get_users_friends_key(user_id)
        self.__Logger.info("Adding key: %s with user_id: %s" % (user_friend_tuple[0], user_friend_tuple[1]))
        status_code = self.fsq_redis.put_hash_item(user_friend_tuple[0], user_friend_tuple[1], venue_list)
        if status_code:
            self.__Logger.info("Added users liked venue total status:", status_code )

    def get_users_friends(self, user_id='self', limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting users friend from redis: %s" % user_id)
        user_friend_tuple = get_users_friends_key(user_id)
        self.__Logger.info("Checking hash: %s with user_id: %s" % (user_friend_tuple[0], user_friend_tuple[1]))
        user_friends = self.fsq_redis.get_hash_item(user_friend_tuple[0], user_friend_tuple[1])
        if user_friends is not None:
            user_friends_list = json.loads(user_friends)
            self.__Logger.info("Found %s friends:", len(user_friends_list))
            return user_friends_list
        else:
            self.__Logger.info("No friends found for user %s", user_id)
            return None



