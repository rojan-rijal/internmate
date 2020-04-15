from flask_api import FlaskAPI
from flask import request, json, Flask, jsonify
from foursqurconn import findVenue 
import os
app =FlaskAPI(__name__)

@app.route('/foursquare', methods = ['POST'])
def foursquare():
	if request.headers['Content-Type'] == 'application/json':
		cityState= request.json
		print(findVenue(cityState['city'], cityState['state']))
		return jsonify(findVenue(cityState["city"],cityState["state"])) 

if __name__ == '__main__':
	app.run(port=80, threaded=True)

