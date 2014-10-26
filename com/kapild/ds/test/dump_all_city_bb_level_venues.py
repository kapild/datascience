from ds.backend.redis.Redis import RedisStoreImpl
from ds.backend.redis.utils import get_fsq_city_name
from ds.foursquare.cities.cities_bounding_box import sf_bb

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



def dump_city_bb_level_venues(bb_city):
    f_write = open(bb_city.name + "_bb_fsq.venues", mode='w')
    total_venue = 0
    venue_id_set = set()


    all_venues_list = {}
    for venue_hash_key in fs.get_city_bb_hash_keys(bb_city):
        hash_name = get_fsq_city_name(bb_city.name)
        venue_items_json = redis.get_hash_item(hash_name, venue_hash_key)
        venue_items = json.loads(venue_items_json)
        if len(venue_items) > 0:
            for venue in venue_items:
                venue_id = venue['id']
                if venue_id not in venue_id_set:
                    name = venue["name"]
                    lat_lng = []
                    lat_lng.append(venue["location"]["lng"])
                    lat_lng.append(venue["location"]["lat"])
                    venue_id_set.add(venue_id)
                    total_venue += 1
                    all_venues_list[name[0:10]] = lat_lng
                    f_write.write(json.dumps(venue) + "\n")

    print json.dumps(all_venues_list)
    print str(total_venue)

    f_write.close()

if __name__ == "__main__":
    dump_city_bb_level_venues(sf_bb)



