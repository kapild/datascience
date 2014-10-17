__author__ = 'kdalwani'


class City():
    def __init__(self, params):
        self.name = params["name"]
        self.ll = params["ll"]


sf = City({
    "name" : "San Francisco",
    "ll" : "37.7751,-122.41"
})


ny = City({
        "name" : "New York",
        "ll" : "40.66,-73.93"
})

la = City({
    "name" : "Los Angeles",
    "ll" : "34.019,-118.4"
})

chicago = City({
    "name" : "Chicago",
    "ll" : "41.8376,-87.6818"
})

houston = City({
    "name" : "Houston",
    "ll" : "29.780,-95.386"
})

philadephia = City({
    "name" : "Philadelphia",
    "ll" : "40.0094,-75.13"
})

san_dieogo = City({
    "name" : "San Diego",
    "ll" : "32.8153,-117.1350"
})

austin = City({
    "name" : "Austin",
    "ll" : "30.3072,97.7560"
})

seattle = City({
    "name" : "Seattle",
    "ll" : "47.6205,-122.350"
})

denver = City({
    "name" : "Denver",
    "ll" : "39.7618,-104.880"
})

boston = City({
    "name" : "Boston",
    "ll" : "42.3320,-71.02"
})

atlanta = City({
    "name" : "Atlanta",
    "ll" : "33.7629,-84.4"
})

miami = City({
    "name" : "Miami",
    "ll" : "25.7752,-80.208"
})

def get_top_cities_ll():
    famous_cities = []


    famous_cities.append(
        sf,
        ny,
        la,
        chicago,
        houston,
        philadephia,
        san_dieogo,
        austin,
        seattle,
        denver,
        boston,
        atlanta,
        miami
    )
    return famous_cities

