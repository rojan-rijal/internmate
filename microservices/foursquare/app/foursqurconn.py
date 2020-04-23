
import foursquare
import os

#Construct the client object

<<<<<<< HEAD
client = foursquare.Foursquare(client_id= os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'))

def findVenue(city, state):
=======
client = foursquare.Foursquare(client_id= os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'), redirect_uri='http://fondu.com/oauth/authorize')


def findVenue(city, state, offset):
>>>>>>> c1cbb615600d6150f6660fb59b720230027e314a

    venues = []
    location = city+', '+state

    #grab data from an foursquare API
<<<<<<< HEAD
    data = client.venues.search(params={'near': location , 'intent':'browse', 'limit':'10', 'categoryid':'4d4b7104d754a06370d81259, 4d4b7105d754a06373d81259, 4d4b7105d754a06376d8125'}) 
=======
    data = client.venues.search(params={'near': location , 
                                                'intent':'browse', 
                                                'limit':'{offset}'.format(offset=offset), 
                                                'categoryid':'4d4b7104d754a06370d81259, 4d4b7105d754a06373d81259, 4d4b7105d754a06376d8125'}) 
>>>>>>> c1cbb615600d6150f6660fb59b720230027e314a
    
    for venue in data['venues']:
        venueInfo = {}      
       
        venueInfo['categoryName']= venue['categories'][0]['name'] 
        venueInfo['name']= venue['name']
        
        #address
        address = '' 
        for addressElem in venue['location']['formattedAddress']:
            address = address+addressElem+' '
        
        venueInfo['address'] = address
       
        #append dictionary to list
        venues.append(venueInfo)
        
    return venues
<<<<<<< HEAD
~                 
=======
>>>>>>> c1cbb615600d6150f6660fb59b720230027e314a
