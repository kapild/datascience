

import logging
import redis

class IRedisApiBase(object):


    def contains_key(self, key):
        raise NotImplementedError


    def get(self, key):
        raise NotImplementedError


    def set_add(self, set_name, value):
        raise NotImplementedError

    def set_members(self, set_name):
        raise NotImplementedError

class RedisStoreImpl(IRedisApiBase):

    def __init__(self, conn_args=None):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

        conn_args = conn_args
        reader_dict = conn_args.get('read')
        self.__reader = None
        self.__writer = None
        if reader_dict:
            self.__reader = redis.Redis(**reader_dict)
        else:
            self._logger.info("No reader connection available. exit().")

        writer_dict = conn_args.get('write')
        if writer_dict:
            self.__writer = redis.Redis(**writer_dict)
        else:
            self._logger.info("No writer connection available. exit().")

        self._logger.info("Foursquare redis connection saved.")


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

    def get_hash_item(self, hash_name, hash_key):
        values = self.__reader.hget(hash_name, hash_key)
        return values

    def put_hash_item(self, hash_name, hash_key, hash_value):
        self.__reader.hset(hash_name, hash_key, hash_value)
