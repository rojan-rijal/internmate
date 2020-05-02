#Module Name:           Airbnb API Client for Python
#Date of the code:      4/19/20
#Programer(s) Name:     Janeen Yamak, Brittany Kraemer, Rojan Rijal
#Brief description:     This file is a client for the Airbnb api. A user shall input the city, state, and offset and it shall return a list of apartments located in the near area
#Data Structure:        A list of Dictionaries
#Algorithm:             Parsing through a json list

import airbnb
api = airbnb.Api(randomize = True)


def findApt(city,state):
    
    apts = []
    location = city+", "+state

    #should return a json object of apartments in the given location
    data = api.get_homes(location, offset = 1, items_per_grid = 10)

    #parse through the json file and grab the data we need and insert that data into a dictionary
    for k in data['explore_tabs'][0]['sections'][0]['listings']:
        aptInfo= {} 
        aptInfo['name'] = k['listing']['name']
        aptInfo['id'] = k['listing']['id']
        aptInfo['urls'] = k['listing']['picture_urls']
        aptInfo['guests']=  k['listing']['guest_label'].split(' ')[0]
        aptInfo['homeType']= k['listing']['bedroom_label'] 
        aptInfo['numOfBaths'] = k['listing']['bathroom_label'].split(' ')[0]
        numBedRooms = k['listing']['bed_label'].split(' ')[0]
        aptInfo['numBedroom']= k['listing']['bed_label'].split(' ')[0]
        aptInfo['rate']= k['pricing_quote']['rate_with_service_fee']['amount_formatted'].split('$')[1]

        #append a dictionary to the list
        apts.append(aptInfo)
    #return a list of apartments to the api
    return apts

