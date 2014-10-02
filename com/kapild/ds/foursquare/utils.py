__author__ = 'kdalwani'


import foursquare
def get_foursquare_client():
    access_token = 'VXIVQI3LOIDSLIZOHH12EJXIHY5DMBQHOJA0DAAHFJKITB4Y'
    client = foursquare.Foursquare(access_token=access_token, version='20140901')
    return client
