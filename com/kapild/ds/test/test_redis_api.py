__author__ = 'kdalwani'


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

def test_get_user_like_venue(user_id='self'):

    fs = Foursquare(redis_dict)
    for venue in fs.get_users_liked_venue(user_id):
        print venue

def test_get_user_friend_list(user_id='self'):

    fs = Foursquare(redis_dict)
    for venue in fs.get_users_friend(user_id):
        continue
        # print venue

if __name__ == "__main__":
    test_get_user_friend_list(40083285)