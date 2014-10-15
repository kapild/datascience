from ds.backend.redis.Redis import RedisStoreImpl

__author__ = 'kdalwani'

import foursquare

from ds.foursquare.data.foursquare_data import Foursquare
import time
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


def test_get_user_like_venue(user_id='self'):

    for venue in fs.get_users_liked_venue(user_id):
        print venue

def test_get_user_friend_list(user_id='self'):

    for venue in fs.get_users_friend(user_id):
        continue
        # print venue
def test_get_lists_items(listid):
    kwargs = {'is_fresh' : False}
    for user_list in fs.get_lists_items(listid, **kwargs):
        print user_list

def test_get_users_saved_list(user_id='self'):
    kwargs = {'is_fresh' : True}
    for user_list in fs.get_users_saved_list(user_id, **kwargs):
        print user_list['name']

def test_get_venue_details(venue_id, **kwargs):
    kwargs = {'is_fresh' : False}
    for venue_detail in fs.get_venue_details(venue_id, **kwargs):
        print venue_detail

def run():

    venue_set = set()
    user_stack = []
    user_set = set()
    user_stack.append('self')
    kwargs = {'is_fresh' : False}

    while len(user_stack) > 0:
        try:
            user_id = user_stack.pop()
            print("Starting processing for user:%s" % user_id)

            user_liked_venues = fs.get_users_liked_venue(user_id, **kwargs)
            for user_liked_venue in user_liked_venues:
                for venue in fs.get_venue_details(user_liked_venue['id']):
                    venue_set.add(venue['id'])

            print("Done user liked venues for user:%s" % user_id)
            user_saved_lists = fs.get_users_saved_list(user_id, **kwargs)
            for user_saved_list in user_saved_lists:
                user_list = fs.get_lists_items(user_saved_list['id'], **kwargs)
                print("Getting venues for user_id:%s, saved list is:%s" % (user_id, user_saved_list['id']))
                for list_venue in user_list:
                    for venue in fs.get_venue_details(list_venue['id'], **kwargs):
                        venue_set.add(venue['id'])

            print("Getting users friends:%s" % user_id)
            for friends in fs.get_users_friend(user_id, **kwargs):
                friend_id = friends['id']
                if friend_id not in user_set:
                    user_stack.append(friend_id)
                    user_set.add(friend_id)

            print("Done processing for user:%s" % user_id)
        except foursquare.RateLimitExceeded:
            print "len(user_set):" + str(len(user_set))
            print "len(venue_set):" + str(len(venue_set))
            print "error"
            time.sleep(60 * 60)

def get_venue_keys():
    for venue_key in fs.get_venue_keys():
        for venue in fs.get_venue_details(venue_key):
            print venue


if __name__ == "__main__":
    # test_get_users_saved_list(40083285) #4e4be62f18a808fd11036118
    # test_get_lists_items('4e4be62f18a808fd11036118')
 #   test_get_venue_details('4b7591a7f964a520dc142ee3')

    get_venue_keys()



