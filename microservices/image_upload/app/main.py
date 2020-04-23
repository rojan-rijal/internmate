from flask_api import FlaskAPI
from flask import request, json, Flask, jsonify
from foursqurconn import findVenue 
import os
app =FlaskAPI(__name__)

@app.route('/imageupload', methods = ['POST'])
def image_upload():
	return jsonify({"success":"Image uploaded"})

@app.route('/getimages')
def get_images():
	return jsonify({"success":"Images received"})

if __name__ == '__main__':
	app.run(port=80, threaded=True)

