__author__ = 'kdalwani'

import logging

from utils import get_foursquare_client
class FourSquareWrap():

    def __init__(self):
        self.api = get_foursquare_client()

        self.__Logger = logging.getLogger(__name__)
        self.__Logger.setLevel(logging.INFO)


    def get_venue_categories(self, attr=['name', 'id', 'categories']):
        self.__Logger.info("Getting venue categories")
        venue_categories = self._get_api_venue_categories()
        if 'categories' in venue_categories:
            categories = venue_categories['categories']
            self.__Logger.info("Total categories %s" % len(categories))
            for category in categories:
                category_dict = {}
                for key in attr:
                    if key in category:
                        category_dict[key] = category[key]
                yield category_dict




    '''
    get category location search
    '''
    def get_category_location_venue_search(self,
        category_id,
        ll,
        attr=['name', 'hasMenu', 'id', 'location', 'categories', 'menu']
    ):
        self.__Logger.info("Getting venue search for category_id: %s lat,lng:%s" % (category_id, ll))
        limit = 50
        has_more_results = True
        params = {
            'll' : ll,
            'query': category_id,
            'intent': 'browse',
            'limit': limit,
            'radius': 100000
        }

        while has_more_results:
            search_venues = self._get_api_venue_search(params)
            if 'venues' in search_venues:
                venues_items = search_venues['venues']
                count = len(venues_items)
                self.__Logger.info("Total venues %s" % count)
                for venue in venues_items:
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            self.__Logger.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                has_more_results = False
            else:
                has_more_results = False

    def get_venue_item_details(self, venue_id):
        venue_item = self._get_api_venue_item(venue_id, 0, 300)
        return venue_item['venue'] if 'venue' in venue_item else None

    '''
    get users likes venues
    '''
    def get_users_likes_venues(self, user_id="self", limit='All', attr=['id', 'location', 'name', 'hasMenu']):
        self.__Logger.info("Getting user\'s: %s liked venue list:" + user_id)
        limit = 500
        offset = 0
        has_more_results = True

        while has_more_results:
            liked_venues = self._get_api_uaers_liked_venues(user_id, 0, 300)
            if 'venues' in liked_venues and 'items' in liked_venues['venues']:
                liked_venue = liked_venues['venues']
                count = liked_venue['count']
                self.__Logger.info("Total venues %s" % count)
                liked_venue_list = liked_venue['items']
                self.__Logger.info("Iterating over next %s venues, offset:%s " % (
                    len(liked_venue_list), offset)
                )
                for venue in liked_venue_list:
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            self.__Logger.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                offset += len(liked_venue_list)
                if offset >= count:
                    self.__Logger.info("No more venues:...")
                    has_more_results = False
            else:
                has_more_results = False

    '''
    get venue ids and other attributes for a list id from anyone
    '''
    def get_lists_items(self, list_id, limit='All', attr=['id', 'location', 'name', 'categories', 'hasMenu']):
        self.__Logger.info("Getting list\'s saved item:" + list_id)
        limit = 500
        offset = 0
        has_more_results = True
        while has_more_results:
            lists_items = self._get_api_lists_venues(list_id, offset, limit)
            if 'list' in lists_items and 'listItems' in lists_items['list']:
                lists_items = lists_items['list']['listItems']
                count = lists_items['count']
                self.__Logger.info("Total venues %s" % count)
                lists_items_list = lists_items['items']
                self.__Logger.info("Iterating over next %s venues, offset:%s " % (
                    len(lists_items_list), offset)
                )
                for venues in lists_items_list:
                    venue = venues['venue']
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            self.__Logger.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                offset += len(lists_items_list)
                if offset >= count:
                    self.__Logger.info("No more venues:...")
                    has_more_results = False
            else:
                has_more_results = False


    """
    https://developer.foursquare.com/docs/explore#req=users/self/lists%3Fgroup%3Dcreated
    """
    def get_user_saved_list(self, user_id='self', limit='All', attr=['id', 'name', 'location', 'hasMenu']):
        self.__Logger.info("Getting user:%s saved list:" % user_id)
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
                                self.__Logger.debug("Getting venue attribute %s, value:%s" % (key, items[key]))
                                list_dict[key] = items[key]
                        yield list_dict
            has_more_results = False

    """
    https://developer.foursquare.com/docs/explore#req=users/self/venuehistory
    """
    def get_self_checkins(self,  limit='All', attr=['id', 'name']):
        self.__Logger.info("Getting user\'s checkins:" + 'self')
        limit = 500
        offset = 0
        has_more_results = True
        while has_more_results:
            my_check_ins = self._get_api_users_venue_history(offset, limit)
            if 'venues' in my_check_ins and 'items' in my_check_ins['venues']:
                venues_checked = my_check_ins['venues']
                count = venues_checked['count']
                self.__Logger.info("Total venues %s" % count)
                venues_checked_list = venues_checked['items']
                self.__Logger.info("Iterating over next %s venues, offset " %
                             (len(venues_checked_list)), offset)
                for checkins in venues_checked_list:
                    venue = checkins['venue']
                    venues_dict = {}
                    for key in attr:
                        if key in venue:
                            self.__Logger.debug("Getting venue attribute %s, value:%s" % (key, venue[key]))
                            venues_dict[key] = venue[key]
                    yield venues_dict
                offset += len(venues_checked_list)
                if offset >= count:
                    self.__Logger.info("No more venues:...")
                    has_more_results = False
            else:
                has_more_results = False

    def get_users_friends(self, user_id='self', limit='All', attr=['id', 'firstName']):

        self.__Logger.info("Getting user %s friends:" , user_id)
        limit = 500
        offset = 0
        users_friends = self._get_api_users_friends(user_id, offset, limit)

        # check if the object returned has friends, items and counts
        if 'friends' in users_friends and 'items' in users_friends['friends'] \
                and 'count' in users_friends['friends']:
            friends = users_friends['friends']
            counts = friends['count']
            self.__Logger.debug("Found %s: friends" % counts)
            friends_list = friends['items']
            for friend in friends_list:
                friend_dict = {}
                for key in attr:
                    if key in friend:
                        self.__Logger.debug("Getting attribute %s, value:%s" % (key, friend[key]))
                        friend_dict[key] = friend[key]
                yield friend_dict


    def _get_api_uaers_liked_venues(self, user_id, offset, limit):
        return self.api.users.venuelikes(
            user_id,
            params={
            'limit': limit,
            'offset' : offset,
        })

    def _get_api_venue_item(self, venue_id, offset, limit):
        return self.api.venues(
            venue_id)

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

    def _get_api_venue_categories(self):
        return self.api.venues.categories()
