__author__ = 'kdalwani'


class CityBB():
    def __init__(self, params):
        self.name = params["name"]
        self.nw = params["bb"][0]
        self.se = params["bb"][1]


sf_bb = CityBB({
    "name" : "San Francisco",
    "bb" : ["37.811954,-122.363148", "37.705689,-122.528629"]
})

# ny_bb = CityBB({
#         "name" : "New York",
#         "bb" : [ "40.856252,-73.928973", "40.696209,-74.017416"]
#
# })

manhattan_bb = CityBB({
        "name" : "manhattan",
        "bb" : [ "40.856252,-73.928973", "40.696209,-74.017416"]

})

chicago_bb = CityBB({
    "name" : "chicago",
    "bb" : [ "42.023131,-87.524044", "41.644335,-87.940267"]
})

austin_bb = CityBB({
    "name" : "austin",
    "bb" : [ "30.516805,-97.5612", "30.098668,-97.938787"]
})

atlanta_bb = CityBB({
    "name" : "Atlanta",
    "bb" : [ "33.885338,-84.289389", "33.647808,-84.551819"]
})
#
# la = City({
#     "name" : "Los Angeles",
#     "ll" : "34.019,-118.4"
# })
#
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
#
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
#
# miami = City({
#     "name" : "Miami",
#     "ll" : "25.7752,-80.208"
# })

def get_top_cities_bb():

    famous_cities = [
        sf_bb,
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