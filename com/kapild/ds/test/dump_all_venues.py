from ds.backend.redis.Redis import RedisStoreImpl

__author__ = 'kdalwani'

import json
from ds.foursquare.data.foursquare_data import Foursquare
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

fs = Foursquare(redis_dict)
redis = RedisStoreImpl(redis_dict)



def dump_venue():
    f_write = open("fsq.venues", mode='w')
    for venue_key in fs.get_venue_keys():
        for venue in fs.get_venue_details(venue_key):
            f_write.write(json.dumps(venue) + "\n")

    f_write.close()

if __name__ == "__main__":
    dump_venue()



