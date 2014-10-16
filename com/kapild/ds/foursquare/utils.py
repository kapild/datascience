__author__ = 'kdalwani'

import logging
import json
import foursquare
def get_foursquare_client():
    access_token = 'VXIVQI3LOIDSLIZOHH12EJXIHY5DMBQHOJA0DAAHFJKITB4Y'
    client = foursquare.Foursquare(access_token=access_token, version='20140901')
    return client


def my_log(_logger, level, kwargs):
    log_message = "Following key/values:"
    for key in kwargs:
        log_message += " " + str(key) + ":" + json.dumps(kwargs[key]) + " "

    if level == logging.INFO:
        _logger.info(log_message)
    elif level == logging.DEBUG:
        _logger.debug(log_message)