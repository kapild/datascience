__author__ = 'kdalwani'


class CityBB():
    def __init__(self, params):
        self.name = params["name"]
        self.nw = params["bb"][0]
        self.se = params["bb"][1]


sf_bb = CityBB({
    "name" : "San Francisco",
    "bb" : ["37.8324,-122.3553", "37.6040,-123.0137"]
})

ny_bb = CityBB({
        "name" : "New York",
        "bb" : [ "40.9176,-73.7004", "40.4766,-74.2589"]
})
#
# la = City({
#     "name" : "Los Angeles",
#     "ll" : "34.019,-118.4"
# })
#
# chicago = City({
#     "name" : "Chicago",
#     "ll" : "41.8376,-87.6818"
# })
#
# houston = City({
#     "name" : "Houston",
#     "ll" : "29.780,-95.386"
# })
#
# philadephia = City({
#     "name" : "Philadelphia",
#     "ll" : "40.0094,-75.13"
# })
#
# san_dieogo = City({
#     "name" : "San Diego",
#     "ll" : "32.8153,-117.1350"
# })
#
# austin = City({
#     "name" : "Austin",
#     "ll" : "30.3072,97.7560"
# })
#
# seattle = City({
#     "name" : "Seattle",
#     "ll" : "47.6205,-122.350"
# })
#
# denver = City({
#     "name" : "Denver",
#     "ll" : "39.7618,-104.880"
# })
#
# boston = City({
#     "name" : "Boston",
#     "ll" : "42.3320,-71.02"
# })
#
# atlanta = City({
#     "name" : "Atlanta",
#     "ll" : "33.7629,-84.4"
# })
#
# miami = City({
#     "name" : "Miami",
#     "ll" : "25.7752,-80.208"
# })

def get_top_cities_bb():
    famous_cities = []


    famous_cities = [sf_bb,
        ny_bb,
        # la,
        # chicago,
        # houston,
        # philadephia,
        # san_dieogo,
        # austin,
        # seattle,
        # denver,
        # boston,
        # atlanta,
        # miami
    ]

    return famous_cities

