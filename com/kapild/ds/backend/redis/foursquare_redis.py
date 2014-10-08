

import logging
from ds.backend.redis.Redis import RedisStoreImpl
from ds.backend.redis.utils import get_user_liked_key


class FoursquareRedisBackend:


    def __init__(self, redis_dict):
        self.__Logger = logging.getLogger("FoursquareRedisBackend")
        self.__Logger.info("staring FoursquareRedisBackend store")
        self.fsq_redis = RedisStoreImpl(redis_dict)


    def get_users_likes_venues(self, user_id="self", limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.debug("Getting users liked venues from redis")
        liked_venue_tuple = get_user_liked_key(user_id)
        self.__Logger.info("Checking hash: %s with user_id: %s" % (liked_venue_tuple[0], liked_venue_tuple[1]))
        liked_venues = self.fsq_redis.get_hash_item(liked_venue_tuple[0], liked_venue_tuple[1])
        if liked_venues is not None:
            self.__Logger.info("Found %s venues:%" (len(str(liked_venues))))
        else:
            self.__Logger.info("No like venue found for user %s venues:%" (str(user_id)))
        return liked_venues






