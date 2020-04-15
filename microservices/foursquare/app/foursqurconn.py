
import foursquare
import os

#Construct the client object

client = foursquare.Foursquare(client_id= os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'), redirect_uri='http://fondu.com/oauth/authorize')


def findVenue(city, state):
	venueInfo = {}
	venues = []
	location = city+', '+state

	data = client.venues.search(params={'near': location , 'intent':'browse', 'limit':'10', 'categoryid':'4d4b7104d754a06370d81259'}) 

	for venue in data['venues']:
		venueInfo['name']= venue['name']
        #address
		address = '' 
		for addressElem in venue['location']['formattedAddress']:
			address = address+addressElem+' '
		venueInfo['address'] = address
		venues.append(venueInfo)

	return venues 
