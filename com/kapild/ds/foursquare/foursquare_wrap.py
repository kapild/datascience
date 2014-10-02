__author__ = 'kdalwani'

import logging

from utils import get_foursquare_client
class FourSquareWrap():

    def __init__(self):
        logging.info("Init Foursquare wrapper")
        self.api = get_foursquare_client()


    """
    https://developer.foursquare.com/docs/explore#req=users/self/lists%3Fgroup%3Dcreated
    """
    def get_user_saved_list(self, user_id='self', limit='All', attr=['id', 'name']):
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