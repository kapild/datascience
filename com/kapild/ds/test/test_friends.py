__author__ = 'kdalwani'




from ds.foursquare.foursquare_wrap import FourSquareWrap

fsq_wrap = FourSquareWrap()

def test_venues():
    for venue in fsq_wrap.get_self_checkins():
        print venue

def test_friends():
    for friend_id in fsq_wrap.get_users_friends():
        print friend_id

def test_user_lists():
    for friend_id in fsq_wrap.get_user_saved_list():
        print friend_id


if __name__ == '__main__':
    test_user_lists()