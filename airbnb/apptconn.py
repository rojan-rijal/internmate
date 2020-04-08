import airbnb
api = airbnb.Api(randomize = True)


def findapt(city,state):
    aptinfo= {}
    apts = []
    citystate = city+", "+state
    data = api.get_homes(citystate, offset = 1, items_per_grid = 1)

    for k in data['explore_tabs'][0]['sections'][0]['listings']:
        aptinfo['urls'] = k['listing']['picture_urls']
        # aptinfo['numbathroom']=  k['listing']['bathroom_label']
        numofbaths = k['listing']['bathroom_label']
        
        aptinfo['numbedroom']= k['listing']['bed_label']
        aptinfo['rate']= k['pricing_quote']['rate_with_service_fee']['amount_formatted']
        apts.append(aptinfo)

    return apts

