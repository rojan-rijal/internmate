import airbnb
api = airbnb.Api(randomize = True)


def findApt(city,state):
    
    apts = []
    location = city+", "+state
    data = api.get_homes(location, offset = 1, items_per_grid = 10)

    #print (data)

    for k in data['explore_tabs'][0]['sections'][0]['listings']:
        aptInfo= {} 

        aptInfo['urls'] = k['listing']['picture_urls']
        aptInfo['guests']=  k['listing']['guest_label'].split(' ')[0]
        aptInfo['homeType']= k['listing']['bedroom_label'] 
        aptInfo['numOfBaths'] = k['listing']['bathroom_label'].split(' ')[0]
        numBedRooms = k['listing']['bed_label'].split(' ')[0]
        aptInfo['numBedroom']= k['listing']['bed_label'].split(' ')[0]
        aptInfo['rate']= k['pricing_quote']['rate_with_service_fee']['amount_formatted'].split('$')[1]
        apts.append(aptInfo)

    return apts

