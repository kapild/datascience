


def get_user_liked_key(user_id):
    return "user_liked_venues",  user_id

def get_users_friends_key(user_id):
    return "user_friends",  user_id

def get_users_saved_list(user_id):
    return "user_lists",  user_id

def get_lists_saved_list(list_id):
    return "lists_items",  list_id

def get_venue_details(list_id):
    return "fsq_venue",  list_id
