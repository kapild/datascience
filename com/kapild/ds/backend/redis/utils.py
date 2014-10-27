


def get_user_liked_key(user_id):
    return "user_liked_venues",  user_id

def get_users_friends_key(user_id):
    return "user_friends",  user_id

def get_users_saved_list(user_id):
    return "user_lists",  user_id

def get_lists_saved_list(list_id):
    return "lists_items",  list_id

def get_venue_hash():
    return "fsq_venue"

def get_fsq_categories():
    return "fsq", "categories"

def get_fsq_city_name(city_name):
    return "fsq_city_bb_" + city_name

def get_venue_location_categories(city_nane, category_id):
    return get_fsq_city_name(city_nane), category_id

def get_venue_details(list_id):
    return get_venue_hash(),  list_id

def get_venue_menu(venue_id):
    return "menu_details", venue_id

