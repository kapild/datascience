
'''
Created on Sep 21, 2014

@author: kdalwani
'''

from crawl import list_venue_crawl
class UsersList:


    def __init__(self, api, user_id='self', counts=200):
        self.api = api
        self.counts = counts
        self.user_id = user_id
        self.limit = 20

    def get_all_venue_ids(self):

        venue_set = set()

        isMoreList = True
        offset = 0
        print 'getting venues from list of user:' + str(self.user_id)
        while offset < self.counts and isMoreList == True:
            users_lists = self._get_user_lists(self.api, self.user_id,  offset, self.limit)
            if 'lists' in users_lists and 'groups' in users_lists['lists']:
                list_groups = users_lists['lists']['groups']
                for list_group in list_groups:
                    group_list_ids = self._get_id_from_lists_group(list_group)
                    for list_id in group_list_ids:
                        print 'grup_id:' + str(list_group['name']) + ", list id:" + str(list_id)
                        ids = list_venue_crawl.ListVenueCrawl(self.api, list_id).get_venue_ids()
                        venue_set |=  set(ids)
                        offset = len(venue_set)
                isMoreList = False
                # import pdb; pdb.set_trace()

        return list(venue_set)

    def _get_id_from_lists_group(self, list_group):
        lists_id = []
        for items in list_group['items']:
            lists_id.append(items['id'])
        return lists_id

    def _get_user_lists(self, api, user_id, offset, limit):
        return self.api.users.lists(
            user_id,
            params={
            'limit': limit,
            'offset' : offset,
        })
