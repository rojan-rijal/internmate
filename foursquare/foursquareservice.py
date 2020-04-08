from flask_api import FlaskAPI
from flask import request, json
from foursqurconn import findVenue 

app =FlaskAPI(__name__)

@app.route('/foursquare', methods = ['POST'])
def foursquare():
    if request.headers['Content-Type'] == 'application/json':
        cityState= request.json
        print(cityState)

        return findVenue(cityState["city"],cityState["state"]) 
        
    
if __name__ == '__main__':
    app.run()

