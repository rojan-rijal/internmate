from flask_api import FlaskAPI
from flask import request, json
from foursqurconn import findVenue 

app =FlaskAPI(__name__)

@app.route('/foursquare', methods = ['POST'])
def foursquare():
    if request.headers['Content-Type'] == 'application/json':
        citystate= request.json
        print(citystate)

        return findVenue(citystate["city"],citystate["state"]) 
        
    
if __name__ == '__main__':
    app.run()

