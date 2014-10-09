
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

    def get_users_liked_venue(self, user_id='self'):
        self.__Logger.info("Getting users liked venue")
        liked_venue_redis = self.fsq_redis.get_users_likes_venues(user_id)
        if liked_venue_redis is None:
            self.__Logger.info("No users liked venue from Redis")
            liked_venue_redis = []
            self.__Logger.info("Getting data from Foursquare API.")
            for api_liked_venus in self.fsq_api.get_users_likes_venues(user_id):
                liked_venue_redis.append(api_liked_venus)
            self.__Logger.info("Redis Users liked venue adding data.")
            self.fsq_redis.add_users_likes_venues(user_id, json.dumps(liked_venue_redis))
        self.__Logger.info("Returning users liked venue")
        for venue in liked_venue_redis:
            yield venue

    def get_users_friend(self, user_id='self'):
        self.__Logger.info("Getting users friends list")
        users_friend_list = self.fsq_redis.get_users_friends(user_id)
        if users_friend_list is None:
            self.__Logger.info("No users friend found from Redis")
            users_friend_list = []
            self.__Logger.info("Getting data from Foursquare API.")
            for user_friend in self.fsq_api.get_users_friends(user_id):
                users_friend_list.append(user_friend)
            self.__Logger.info("Redis Users friend list adding data.")
            self.fsq_redis.add_users_friend_list(user_id, json.dumps(users_friend_list))

        self.__Logger.info("Returning user_id:%s total:%s friends" % (user_id, len(users_friend_list)))
        self.__Logger.info("Returning users friend list")
        for friend in users_friend_list:
            yield friend