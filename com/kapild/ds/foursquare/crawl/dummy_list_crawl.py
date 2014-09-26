'''
Created on Sep 21, 2014

@author: kdalwani
'''
import com.kapild.ds.foursquare.crawl
from com.kapild.ds.foursquare.crawl.crawl_type import dummy_venue_list

id_list = []
id_list.append("52f4747d11d2e8fa8b2e5394")
id_list.append("52a659800000000000000009")    

class Dummy_List_Crawl(com.kapild.ds.foursquare.crawl.ICrawl):
    def get_type(self):
        return dummy_venue_list

    def get_venue_ids(self):
        return id_list