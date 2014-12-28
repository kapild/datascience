from ds.GeoJson.shapely_utils import get_contained_shape
from ds.backend.redis.Redis import RedisStoreImpl
from ds.backend.redis.utils import get_fsq_city_name
from ds.foursquare.cities.cities_bounding_box import sf_bb, ny_bb
from shapely.geometry import shape, Point
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



def join_sf_shape_sf_venue_data(bb_city, city_shp_json):

    city_shp = json.load(open(city_shp_json))


    f_write = open(bb_city.name + "_bb_fsq.venues", mode='w')
    total_venue = 0
    venue_id_set = set()


    hood_venue_map = {}
    all_venues_list = {}
    for venue_hash_key in fs.get_city_bb_level_venue_hash_keys(bb_city):
        hash_name = get_fsq_city_name(bb_city.name)
        venue_items_json = redis.get_hash_item(hash_name, venue_hash_key)
        venue_items = json.loads(venue_items_json)
        if len(venue_items) > 0:
            for venue in venue_items:
                venue_id = venue['id']
                if venue_id not in venue_id_set:
                    name = venue["name"]
                    lat_lng = []
                    lng = venue["location"]["lng"]
                    lat = venue["location"]["lat"]
                    lat_lng.append(lng)
                    lat_lng.append(lat)
                    venue_id_set.add(venue_id)
                    total_venue += 1
                    all_venues_list[name[0:10]] = lat_lng

                    point = Point(lng, lat)
                    hood_shape = get_contained_shape(point, city_shp)
                    if hood_shape is None:
                        continue
                    if 'venues' not in hood_shape:
                        hood_shape['venues'] = []
                    hood_shape['venues'].append(venue)
                    print "Adding venue %s to neighborhood:%s" %( venue["name"], hood_shape["properties"]["NAME"])

    f_write.write(json.dumps(city_shp, sort_keys=True, indent=4, separators=(',', ': ') ))

    # print json.dumps(all_venues_list)
    print str(total_venue)

    f_write.close()



def dump_city_bb_level_venues(bb_city):
    f_write = open(bb_city.name + "_bb_fsq.venues", mode='w')
    total_venue = 0
    venue_id_set = set()


    all_venues_list = {}
    for venue_hash_key in fs.get_city_bb_level_venue_hash_keys(bb_city):
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
                    # f_write.write(json.dumps(venue) + "\n")

    # print json.dumps(all_venues_list, sort_keys=True,
    #              indent=4, separators=(',', ': '))
    # print json.dumps(all_venues_list)
    f_write.write(json.dumps(all_venues_list) + "\n")

    print str(total_venue)

    f_write.close()

if __name__ == "__main__":
    # dump_city_bb_level_venues(ny_bb)
    join_sf_shape_sf_venue_data(ny_bb,
                            "/Users/kdalwani/code/workspace/FourquarePyCharmCrawl/com/kapild/ds/GeoJson/ny_manhattan_hood.json"
    )
#

