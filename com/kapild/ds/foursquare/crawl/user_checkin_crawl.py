'''
Created on Sep 21, 2014

@author: kdalwani
'''
from ICrawl import ICrawl
from crawl_type import user_check_in

id_list = []
id_list.append("52f4747d11d2e8fa8b2e5394")
id_list.append("52a659800000000000000009")    

class UserCheckinsCrwal(ICrawl):

    
    def __init__(self, api, counts=40):
        self.api = api
        self.counts = counts
        self.limit = 20
        
    def get_type(self):
        return user_check_in

    def get_venue_ids(self):

        venue_id = []
        
        offset = 0
        while offset < self.counts:
            checks_in = self._get_user_checkins_page(self.api, offset, self.limit)
            if (checks_in and checks_in['checkins'] and checks_in['checkins']['items']):
                for items in checks_in['checkins']['items']:
                    venue_id.append(items['venue']['id'])
            offset = len(venue_id)
        return venue_id

    def _get_user_checkins_page(self, api, offset, limit):
        return self.api.users.checkins(params={
            'limit': limit,
            'offset' : offset,
        })
