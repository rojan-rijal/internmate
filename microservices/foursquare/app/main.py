from flask_api import FlaskAPI
from flask import request, json, Flask, jsonify
from foursqurconn import findVenue 
from flask_cors import CORS
import os
app =FlaskAPI(__name__)
CORS(app)
@app.route('/foursquare', methods = ['POST'])
def foursquare():
	if request.headers['Content-Type'] == 'application/json':
		cityState= request.json
		return jsonify(findVenue(cityState["city"],cityState["state"], cityState['offset'])) 

if __name__ == '__main__':
	app.run(port=80, threaded=True)

