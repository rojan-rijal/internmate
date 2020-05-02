#Module Name:           Airbnb Flask API
#Date of Code:          4/14/20
#Programmer(s) Name:    Janeen Yamak, Brittany Kraemer, Rojan Rijal 
#Brief Description:     This file is a Fask API for the airbnb API. Given a curl post request this file shall return a json object of appartment near the given area
#Data Structure:        input: city, state, offset in a dictionary object output: should return a json object of apartments
#Algorithm:             No algorithm is being used expect a json object should be return at the end of this file

from flask_api import FlaskAPI
from flask import request, json
from apptconn import findApt
from flask_cors import CORS

app =FlaskAPI(__name__)
CORS(app)

#Creating the API endpoint
@app.route('/airbnb', methods = ['POST'])
def airbnb():
    #if the header content-type is equal to application/json
    if request.headers['Content-Type'] == 'application/json':
        cityState= request.json #data being passed in through curl request
        print(cityState)

        return findApt(cityState["city"],cityState["state"]) #return a json object of appartments
        
    
if __name__ == '__main__':
    app.run(port=80, threaded=True)
