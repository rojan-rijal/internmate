#Module Name:           Foursquare Flask API
#Date of code:          4/19/20
#Programmer's Name:     Janeen Yamak, Rojan Rijal
#Brief decription:      This file is the Flask API for the Foursquare API.Given a curl post request this file will vall the `findVenue` function and return a list of venues in that given area
#Data Structure:        input: city, state, offset in a dictionary object output: should return a json object of venues
#Algorithm:             No algorithm is being used except a json should be returned

from flask_api import FlaskAPI
from flask import request, json, Flask, jsonify
from foursqurconn import findVenue 
from flask_cors import CORS
import os

app =FlaskAPI(__name__)
CORS(app)

#creating the an API endpoint
@app.route('/foursquare', methods = ['POST'])
def foursquare():
        #if the header content-type is equal to application/json
	if request.headers['Content-Type'] == 'application/json':
		cityState= request.json #data being passed in through curl request
		return jsonify(findVenue(cityState["city"],cityState["state"], cityState['offset'])) #returns a json object of venues

if __name__ == '__main__':
	app.run(port=80, threaded=True)

