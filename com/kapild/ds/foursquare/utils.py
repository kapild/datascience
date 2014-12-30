from access_tokens import access_tokens

__author__ = 'kdalwani'

import logging
import json
import foursquare

index = 0
def get_foursquare_client():
    for try_index in range(0, len(access_tokens)):
        access_token = access_tokens[try_index]
        client = foursquare.Foursquare(access_token=access_token, version='20140901')
        if is_rate_fine(client):
            return client
    return None


def is_rate_fine(client):
    try:
        str(client.venues('40a55d80f964a52020f31ee3'))
        print 'No rate error'
        return True
    except foursquare.RateLimitExceeded:
        print 'rate error'
        return False
def my_log(_logger, level, kwargs):
    log_message = "Following key/values:"
    # for key in kwargs:
    #     log_message += " " + str(key) + ":" + json.dumps(kwargs[key]) + " "

    if level == logging.INFO:
        _logger.info(log_message)
    elif level == logging.DEBUG:
        _logger.debug(log_message)


if __name__ == "__main__":
    get_foursquare_client()