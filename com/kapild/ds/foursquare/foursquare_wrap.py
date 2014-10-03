__author__ = 'kdalwani'

import logging

from utils import get_foursquare_client
class FourSquareWrap():

    def __init__(self):
        logging.info("Init Foursquare wrapper")
        self.api = get_foursquare_client()



    '''
    get category location search
    '''

    def get_category_location_venue_explore(self, category="coffee", location="37.7833,-122.41",
                                           attr=['name', 'hasMenu']):
        logging.info("Getting venue search for category\'s: %s lat,lng:%s" % (category, location))
        limit = 500
        offset = 0
        has_more_results = True
        while has_more_results:
            params = {
                'll' : location,
                'query' : category,
                'intent' : 'browse',
                'limit' : limit,
                'offset' : offset,
                'radius' : 100000

            }
            search_venues = self._get_api_venue_explore(params)
            if 'groups' in search_venues and 'items' in search_venues['groups'][0]:
                venues_items = search_venues['groups'][0]['items']
                count = search_venues['totalResults']
                logging.info("Total venues %s" % len(venues_items))
                for venue_item in venues_items:
                    venue = venue_item['venue']
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            logging.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                offset += len(venues_items)
                if offset >= count:
                    logging.info("No more venues:...")
                    has_more_results = False
            else:
                has_more_results = False



    '''
    get users likes venues
    '''

    def get_users_likes_venues(self, user_id="self", limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        logging.info("Getting user\'s: %s liked venue list:" + user_id)
        limit = 500
        offset = 0
        has_more_results = True

        while has_more_results:
            liked_venues = self._get_api_uaers_liked_venues(user_id, 0, 300)
            if 'venues' in liked_venues and 'items' in liked_venues['venues']:
                liked_venue = liked_venues['venues']
                count = liked_venue['count']
                logging.info("Total venues %s" % count)
                liked_venue_list = liked_venue['items']
                print ("Iterating over next %s venues, offset:%s " % (len(liked_venue_list), offset))
                logging.info("Iterating over next %s venues, offset:%s " % (
                    len(liked_venue_list), offset)
                )
                for venue in liked_venue_list:
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            logging.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                offset += len(liked_venue_list)
                if offset >= count:
                    logging.info("No more venues:...")
                    has_more_results = False
            else:
                has_more_results = False

    '''
    get venue ids and other attributes for a list id from anyone
    '''
    def get_lists_items(self, list_id, limit='All', attr=['id', 'location', 'name', 'categories', 'hasMenu']):
        logging.info("Getting list\'s saved item:" + list_id)
        limit = 500
        offset = 0
        has_more_results = True
        while has_more_results:
            lists_items = self._get_api_lists_venues(list_id, offset, limit)
            if 'list' in lists_items and 'listItems' in lists_items['list']:
                lists_items = lists_items['list']['listItems']
                count = lists_items['count']
                logging.info("Total venues %s" % count)
                lists_items_list = lists_items['items']
                print ("Iterating over next %s venues, offset:%s " % (len(lists_items_list), offset))
                logging.info("Iterating over next %s venues, offset:%s " % (
                    len(lists_items_list), offset)
                )
                for venues in lists_items_list:
                    venue = venues['venue']
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            logging.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                offset += len(lists_items_list)
                if offset >= count:
                    logging.info("No more venues:...")
                    has_more_results = False
            else:
                has_more_results = False


    """
    https://developer.foursquare.com/docs/explore#req=users/self/lists%3Fgroup%3Dcreated
    """
    def get_user_saved_list(self, user_id='self', limit='All', attr=['id', 'name', 'location', 'hasMenu']):
        logging.info("Getting user\'s saved list:" + user_id)
        limit = 500
        offset = 0
        has_more_results = True
        while has_more_results:
            for group_type in ['created', 'followed', 'friends']:
                users_lists = self._get_api_users_lists(user_id, offset, limit, group_type)
                if 'lists' in users_lists and 'items' in users_lists['lists']:
                    for items in users_lists['lists']['items']:
                        list_dict = {}
                        for key in attr:
                            if key in items:
                                logging.debug("Getting venue attribute %s, value:%s" % (key, items[key]))
                                list_dict[key] = items[key]
                        yield list_dict
            has_more_results = False

    """
    https://developer.foursquare.com/docs/explore#req=users/self/venuehistory
    """
    def get_self_checkins(self,  limit='All', attr=['id', 'name']):
        logging.info("Getting user\'s checkins:" + 'self')
        limit = 500
        offset = 0
        has_more_results = True
        while has_more_results:
            my_check_ins = self._get_api_users_venue_history(offset, limit)
            if 'venues' in my_check_ins and 'items' in my_check_ins['venues']:
                venues_checked = my_check_ins['venues']
                count = venues_checked['count']
                logging.info("Total venues %s" % count)
                venues_checked_list = venues_checked['items']
                logging.info("Iterating over next %s venues, offset " %
                             (len(venues_checked_list)), offset)
                for checkins in venues_checked_list:
                    venue = checkins['venue']
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            logging.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                offset += len(venues_checked_list)
                if offset >= count:
                    logging.info("No more venues:...")
                    has_more_results = False
            else:
                has_more_results = False

    def get_users_friends(self, user_id='self', limit='All', attr=['id', 'firstName']):

        logging.info("Getting user\'s friends:" + user_id)
        limit = 500
        offset = 0
        users_friends = self._get_api_users_friends(user_id, offset, limit)

        # check if the object returned has friends, items and counts
        if 'friends' in users_friends and 'items' in users_friends['friends'] \
                and 'count' in users_friends['friends']:
            friends = users_friends['friends']
            counts = friends['count']
            logging.debug("Found %s: friends" % counts)
            friends_list = friends['items']
            for friend in friends_list:
                friend_dict = {}
                for key in attr:
                    if key in friend:
                        logging.debug("Getting attribute %s, value:%s" % (key, friend[key]))
                        friend_dict[key] = friend[key]
                yield friend_dict


    def _get_api_uaers_liked_venues(self, user_id, offset, limit):
        return self.api.users.venuelikes(
            user_id,
            params={
            'limit': limit,
            'offset' : offset,
        })

    def _get_api_lists_venues(self, list_id, offset, limit):
        return self.api.lists(
            list_id,
            params={
            'limit': limit,
            'offset' : offset,
        })

    def _get_api_users_lists(self, user_id, offset, limit, group_type):
        return self.api.users.lists(
            user_id,
            params={
            'limit': limit,
            'offset' : offset,
            'group' : group_type
        })

    """
    """
    def _get_api_users_venue_history(self, offset, limit):
        return self.api.users.venuehistory(params={
            'limit': limit,
            'offset' : offset,
        })

    """
    response: {
        friends: {
            count: 82
            items: [
            ]
        }
    }
    """
    def _get_api_users_friends(self, user_id, offset, limit=500,):
        return self.api.users.friends(
            user_id,
            params={
            'limit': limit,
            'offset' : offset
        })


    def _get_api_venue_explore(self, params):
        return self.api.venues.explore(
            params=params
        )

    def _get_api_venue_search(self, params):
        return self.api.venues.search(
            params=params
        )
