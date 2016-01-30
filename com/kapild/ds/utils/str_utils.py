__author__ = 'kdalwani'

import re
def remove_space_lower_case(input):
    return re.sub("\s+", "_", input).lower()