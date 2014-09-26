'''
Created on Sep 21, 2014

@author: kdalwani
'''
from ICrawl import ICrawl
from crawl_type import user_check_in


class ListVenueCrawl(ICrawl):

    
    def __init__(self, api, list_id, counts=40):
        self.api = api
        self.counts = counts
        self.list_id = list_id
        self.limit = 20
        
    def get_type(self):
        return user_check_in

    def get_venue_ids(self):

        venue_id = []
        
        offset = 0
        print 'getting venues for list id:' + str(self.list_id)
        isMoreResults = True
        while offset < self.counts and isMoreResults == True:
            lists = self._get_venues_for_list(self.api, self.list_id,  offset, self.limit)
            if 'list' in lists and 'listItems' in lists['list']:
                for lisititems in lists['list']['listItems']['items']:
                    venue_id.append(lisititems['venue']['id'])

                isMoreResults = len(lists['list']['listItems']['items']) > 0

            offset = len(venue_id)
            # print str(offset)

        return venue_id

    def _get_venues_for_list(self, api, list_id, offset, limit):
        return self.api.lists(
            list_id,
            params={
            'limit': limit,
            'offset' : offset,
        })
