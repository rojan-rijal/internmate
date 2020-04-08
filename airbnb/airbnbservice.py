from flask_api import FlaskAPI
from flask import request, json
from apptconn import findapt

app =FlaskAPI(__name__)

@app.route('/airbnb', methods = ['POST'])
def airbnb():
    if request.headers['Content-Type'] == 'application/json':
        citystate= request.json
        print(citystate)

        return findapt(citystate["city"],citystate["state"]) 
        
    
if __name__ == '__main__':
    app.run()
