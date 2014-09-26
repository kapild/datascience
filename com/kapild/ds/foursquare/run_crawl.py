'''
Created on Sep 21, 2014

@author: kdalwani
'''

import foursquare
from crawl import user_checkin_crawl
access_token = 'VXIVQI3LOIDSLIZOHH12EJXIHY5DMBQHOJA0DAAHFJKITB4Y'
client = foursquare.Foursquare(access_token=access_token, version='20140901')

id_list = []
id_list.append("49ed2342f964a520cb671fe3")    
id_list.append("52f4747d11d2e8fa8b2e5394")
def run_crawl():
    
#     venue_ids = Dummy_List_Crawl().get_venue_ids()
    user_crwal = user_checkin_crawl.UserCheckinsCrwal(api=client, counts=50)
    id_list = user_crwal.get_venue_ids()
    indx = 0
    for venue_id in id_list:
        menu = client.venues.menu(venue_id)

        if(menu['menu']['menus'] and 'items' in menu['menu']['menus']):
            import pdb
            pdb.set_trace()
            print str(indx)
            indx = indx + 1
            # print(menu['menu']['menus']['items'])
#         client.Venues.menu(venue, {}, False)
    
if __name__ == '__main__':
    run_crawl()