from flask_api import FlaskAPI
from flask import request, json
from apptconn import findApt

app =FlaskAPI(__name__)

@app.route('/airbnb', methods = ['POST'])
def airbnb():
    if request.headers['Content-Type'] == 'application/json':
        cityState= request.json
        print(cityState)

        return findApt(cityState["city"],cityState["state"]) 
        
    
if __name__ == '__main__':
    app.run()
