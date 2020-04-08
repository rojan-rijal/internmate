import airbnb
api = airbnb.Api(randomize = True)


def findApt(city,state):
    aptInfo= {}
    apts = []
    location = city+", "+state
    data = api.get_homes(location, offset = 1, items_per_grid = 1)

    for k in data['explore_tabs'][0]['sections'][0]['listings']:
        aptInfo['urls'] = k['listing']['picture_urls']
        numOfBaths = k['listing']['bathroom_label']
        
        aptInfo['numbedroom']= k['listing']['bed_label']
        aptInfo['rate']= k['pricing_quote']['rate_with_service_fee']['amount_formatted']
        apts.append(aptInfo)

    return apts

