import foursquare
import os

#Construct the client object
client = foursquare.Foursquare(client_id= 'CID', client_secret='CSK', redirect_uri='http://fondu.com/oauth/authorize')


def findVenue(city, state):

    venueInfo = {}
    venues = []
    location = city+', '+state

    #grab data from an foursquare API
    data = client.venues.search(params={'near': location , 'intent':'browse', 'limit':'2', 'categoryid':'4d4b7104d754a06370d81259, 4d4b7105d754a06373d81259, 4d4b7105d754a06376d8125'}) 

    for venue in data['venues']:
        venueInfo['name']= venue['name']
    
        #address
        address = '' 
        for addressElem in venue['location']['formattedAddress']:
            address = address+addressElem+' '

        venueInfo['address'] = address
        
        venues.append(venueInfo)

    return venues 
