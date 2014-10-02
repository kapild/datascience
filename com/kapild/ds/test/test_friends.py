__author__ = 'kdalwani'




from ds.foursquare.foursquare_wrap import FourSquareWrap

fsq_wrap = FourSquareWrap()

def test_venues():
    for venue in fsq_wrap.get_self_checkins():
        print venue

def test_friends():
    for friend_id in fsq_wrap.get_users_friends():
        print friend_id
    # {'id': u'32364183', 'firstName': u'Payel'}
    # {'id': u'9797450', 'firstName': u'Jasvinder'}
    # {'id': u'94929', 'firstName': u'Priyesh'}
    # {'id': u'19933233', 'firstName': u'Harman'}

def test_user_lists():
    for friend_id in fsq_wrap.get_user_saved_list('19933233'):
        print friend_id
    # {'id': u'19933233/todos', 'name': u"Harman's to-do list"}
    # {'id': u'52e0502811d2ada1a94d8763', 'name': u'Neighborhood Dives / Early Morning Bars'}
    # {'id': u'519d75e1498e68459e65063e', 'name': u'Drink'}

def test_lists_venues():
    for friend_id in fsq_wrap.get_lists_items('19933233/todos'):
        print friend_id

def test_users_venues_like():
    for friend_id in fsq_wrap.get_users_likes_venues():
        print friend_id


if __name__ == '__main__':
    test_users_venues_like()