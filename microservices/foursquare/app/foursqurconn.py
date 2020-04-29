#Module Name:           Foursquare API client for Python
#Date of the code:      4/27/20
#Programmers name:      Janeen Yamak
#Breif description:     This file is a client for the Foursquare api. A user will input a city,state, and an offset and it will return the venues located new that area.
#Data structure:        A list of Dictionaries 
#Algorithm:             I parse through a json list

import foursquare
import os

#Construct the client object
client = foursquare.Foursquare(client_id= os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'), redirect_uri='http://fondu.com/oauth/authorize')


def findVenue(city, state, offset):
        
    venues = []
    location = city+', '+state

    #grab data from an foursquare API
    data = client.venues.search(params={'near': location , 
                                                'intent':'browse', 
                                                'limit':'{offset}'.format(offset=offset), 
                                                'categoryid':'4d4b7104d754a06370d81259, 58daa1558bbb0b01f18ec1d6, 4bf58dd8d48988d173941735, 4bf58dd8d48988d1ff931735, 52e81612bcbc57f1066b7a32, 4e0e22f5a56208c4ea9a85a0, 4bf58dd8d48988d171941735, 4eb1daf44b900d56c88a4600, 4bf58dd8d48988d126941735, 4bf58dd8d48988d12f941735, 5e189d71eee47d000759b7e2, 4bf58dd8d48988d196941735, 4bf58dd8d48988d194941735, 5744ccdfe4b0c0459246b4d9, 4e52adeebd41615f56317744, 4bf58dd8d48988d13b941735, 52e81612bcbc57f1066b7a33, 4bf58dd8d48988d131941735, 4d4b7105d754a06376d81259'}) 

    #parse through the json file and grab the data we need and insert then into a dictionary    
    for venue in data['venues']:
        venueInfo = {}      
        
        venueInfo['id'] = venue['categories'][0]['id']
        venueInfo['icon']= venue['categories'][0]['icon']['prefix']
        venueInfo['fileType']=venue['categories'][0]['icon']['suffix']
        venueInfo['categoryName']= venue['categories'][0]['name'] 
        venueInfo['name']= venue['name']
        
        #address
        address = '' 
        for addressElem in venue['location']['formattedAddress']:
            address = address+addressElem+' '
        
        venueInfo['address'] = address
       
        #append dictionary to list
        venues.append(venueInfo)
       
    #return a list of venues to the api
    return venues
