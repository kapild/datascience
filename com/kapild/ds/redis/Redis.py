

import logging
import redis

_logger = logging.getLogger("FoursquareRedisStore")
class RedisApiBase(object):


    def contains_key(self, key):
        raise NotImplementedError


    def get(self, key):
        raise NotImplementedError


    def set_add(self, set_name, value):
        raise NotImplementedError

    def set_members(self, set_name):
        raise NotImplementedError

class FoursquareRedisStore(RedisApiBase):

    def __init__(self, conn_args=None):
        conn_args = conn_args
        reader_dict = conn_args.get('read')
        self.__reader = None
        self.__writer = None
        if reader_dict:
            self.__reader = redis.Redis(**reader_dict)
        else:
            _logger.info("No reader connection available. exit().")

        writer_dict = conn_args.get('write')
        if writer_dict:
            self.__writer = redis.Redis(**writer_dict)
        else:
            _logger.info("No writer connection available. exit().")

        _logger.info("Foursquare redis connection saved.")


    def contains_key(self, key):
        if not self.__reader:
            return False
        return self.__reader.exists(key)

    def get(self, key):
        return self.__reader.get(key, 0, -1)

    def set_add(self, set_name, value):
        return self.__writer.sadd(set_name, value)

    def set_members(self, set_name):
        return self.__reader.smembers(set_name)