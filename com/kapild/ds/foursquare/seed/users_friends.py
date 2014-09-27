
'''
Created on Sep 21, 2014

@author: kdalwani
'''

from seed import user_lists
class UsersFriends:


    def __init__(self, api, user_id='self', counts=200):
        self.api = api
        self.counts = counts
        self.user_id = user_id
        self.limit = 20

    def get_all_venue_ids(self):

        venue_set = set()

        isMoreList = True
        offset = 0
        print 'getting venues from list of users friends:' + str(self.user_id)
        while offset < self.counts and isMoreList == True:
            users_friends = self._get_users_friends(self.api, self.user_id,  offset, self.limit)
            if 'friends' in users_friends and 'items' in users_friends['friends']:
                friends_list = users_friends['friends']['items']
                for friend in friends_list:
                    friend_id = friend['id']
                    print 'getting venues for friend:' + str(friend_id)
                    friends_venue_id = user_lists.UsersList(self.api, friend_id).get_all_venue_ids()
                    venue_set |=  set(friends_venue_id)
                    offset = len(venue_set)
                isMoreList = False
                # import pdb; pdb.set_trace()
        return list(venue_set)


    def _get_users_friends(self, api, user_id, offset, limit):
        return self.api.users.friends(
            user_id,
            params={
            'limit': limit,
            'offset' : offset,
        })
