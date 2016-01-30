__author__ = 'kdalwani'

import logging
import foursquare
import time
from utils import get_foursquare_client
class FourSquareWrap():

    def __init__(self):
        self.api = get_foursquare_client()

        self.__Logger = logging.getLogger(__name__)
        self.__Logger.setLevel(logging.ERROR)


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



    def get_menu_details(self, venue_id, kwargs):

        self.__Logger.info("Getting menu details for venue_id: %s" % venue_id)
        limit = 50
        has_more_results = True
        params = {
            'limit': limit,
        }

        while has_more_results:
            menu = self._get_api_menu_details(venue_id, params)
            if 'menu' in menu and 'menus' in menu['menu'] and "items" in menu["menu"]["menus"]:
                len_menu = menu['menu']['menus']
                menu_items = menu["menu"]["menus"]["items"]
                self.__Logger.info("Total menus %s" % len_menu)
                for menu_item in menu_items:
                    venues_dict = {}
                    name = menu_item["name"]
                    if "entries" not in menu_item:
                        continue
                    sub_sec = menu_item["entries"]
                    if "items" not in sub_sec:
                        continue
                    sub_sec_items_list = sub_sec["items"]
                    for sub_sec_items in sub_sec_items_list:
                        name = sub_sec_items["name"]
                        if "entries" not in sub_sec_items or "items" not in sub_sec_items["entries"]:
                            continue
                        menu_items_sub = sub_sec_items["entries"]["items"]
                        for menu_sub in menu_items_sub:
                            # print_str = ""
                            # if "name" in menu_sub:
                            #     print_str+=menu_sub["name"]
                            # if "price" in menu_sub:
                            #     print_str+=menu_sub["price"]
                            # print print_str
                            yield  menu_sub
                    # yield venues_dict
                has_more_results = False
            else:
                has_more_results = False

    '''
    get category location search
    '''
    def get_category_location_venue_search(self,
        params,
        attr=['name', 'hasMenu', 'id', 'location', 'categories', 'menu']
    ):

        # intents = ["checkin", "browse"]
        intents = ["browse"]

        for intent in intents:
            for venue in self._get_category_location_venue_search_intent(
                params, intent
            ):
                yield venue

    def _get_category_location_venue_search_intent(self,
        params,
        intent,
        attr=['name', 'hasMenu', 'id', 'location', 'categories', 'menu']
    ):

        self.__Logger.debug("Getting venue search for category_id: %s" % (params["categoryId"]))
        limit = 50
        has_more_results = True
        params = {
            'ne' :params["ne"],
            'sw' :params["sw"],
            'categoryId': params["categoryId"],
            'intent': intent,
            'limit': limit,
            # 'radius': 10000
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
        venue = None
        while venue is None or self.api is None:
            try:
               venue = self.api.venues.search(
                    params=params
                )
            except AttributeError:
                self.api = self.get_new_api_client_or_sleep()
            except foursquare.RateLimitExceeded:
                self.api = self.get_new_api_client_or_sleep()
            except foursquare.ServerError:
                self.api = self.get_new_api_client_or_sleep()
            except Exception:
                self.api = self.get_new_api_client_or_sleep()
        return venue


    def _get_api_menu_details(self, venue_id, params):

        return_menus = None
        while return_menus is None or self.api is None:
            try:
                return_menus = self.api.venues.menu(
                    venue_id,
                    params=params
                )
            except AttributeError:
                self.api = self.get_new_api_client_or_sleep()
            except foursquare.RateLimitExceeded:
                self.api = self.get_new_api_client_or_sleep()
            except foursquare.ServerError:
                self.api = self.get_new_api_client_or_sleep()
            except foursquare.Other:
                return_menus = []
            except Exception as e:
                print e
                self.api = self.get_new_api_client_or_sleep()

        return return_menus


    def get_new_api_client_or_sleep(self):
        loop_true = True
        time_start = time.time()
        while loop_true:
            api_new = get_foursquare_client()
            if api_new is None:
                print "Sleeping due to rate."
                time.sleep(10 * 60)
                print "Trying again, time elapse  sec."

                # print "Trying again, time elapsed:" + str(time.time() - time_start)/60 + " sec."
            else:
                loop_true = False
        # print "Total  time elapsed:" + str((time.time() - time_start)/60) + " sec."
        return api_new

    def _get_api_venue_categories(self):
        return self.api.venues.categories()
